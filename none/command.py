import asyncio
import re
from datetime import datetime
from typing import (
    Tuple, Union, Callable, Iterable, Dict, Any, Optional, Sequence
)

from aiocqhttp.message import Message

from . import NoneBot, permission as perm
from .log import logger
from .expression import render
from .helpers import context_id, send_expr
from .session import BaseSession

# Key: str (one segment of command name)
# Value: subtree or a leaf Command object
_registry = {}

# Key: str
# Value: tuple that identifies a command
_aliases = {}

# Key: context id
# Value: CommandSession object
_sessions = {}


class Command:
    __slots__ = ('name', 'func', 'permission',
                 'only_to_me', 'args_parser_func')

    def __init__(self, *, name: Tuple[str], func: Callable, permission: int,
                 only_to_me: bool):
        self.name = name
        self.func = func
        self.permission = permission
        self.only_to_me = only_to_me
        self.args_parser_func = None

    async def run(self, session, *,
                  check_perm: bool = True,
                  dry: bool = False) -> bool:
        """
        Run the command in a given session.

        :param session: CommandSession object
        :param check_perm: should check permission before running
        :param dry: just check any prerequisite, without actually running
        :return: the command is finished (or can be run, given dry == True)
        """
        has_perm = await self._check_perm(session) if check_perm else True
        if self.func and has_perm:
            if dry:
                return True
            if self.args_parser_func:
                await self.args_parser_func(session)
            await self.func(session)
            return True
        return False

    async def _check_perm(self, session) -> bool:
        """
        Check if the session has sufficient permission to
        call the command.

        :param session: CommandSession object
        :return: the session has the permission
        """
        return await perm.check_permission(session.bot, session.ctx,
                                           self.permission)


def on_command(name: Union[str, Tuple[str]], *,
               aliases: Iterable = (),
               permission: int = perm.EVERYBODY,
               only_to_me: bool = True) -> Callable:
    """
    Decorator to register a function as a command.

    :param name: command name (e.g. 'echo' or ('random', 'number'))
    :param aliases: aliases of command name, for convenient access
    :param permission: permission required by the command
    :param only_to_me: only handle messages to me
    """

    def deco(func: Callable) -> Callable:
        if not isinstance(name, (str, tuple)):
            raise TypeError('the name of a command must be a str or tuple')
        if not name:
            raise ValueError('the name of a command must not be empty')

        cmd_name = (name,) if isinstance(name, str) else name
        current_parent = _registry
        for parent_key in cmd_name[:-1]:
            current_parent[parent_key] = current_parent.get(parent_key) or {}
            current_parent = current_parent[parent_key]
        cmd = Command(name=cmd_name, func=func, permission=permission,
                      only_to_me=only_to_me)
        current_parent[cmd_name[-1]] = cmd
        for alias in aliases:
            _aliases[alias] = cmd_name

        def args_parser_deco(parser_func: Callable):
            cmd.args_parser_func = parser_func
            return parser_func

        func.args_parser = args_parser_deco
        return func

    return deco


class CommandGroup:
    """
    Group a set of commands with same name prefix.
    """
    __slots__ = ('basename', 'permission', 'only_to_me')

    def __init__(self, name: Union[str, Tuple[str]],
                 permission: Optional[int] = None, *,
                 only_to_me: Optional[bool] = None):
        self.basename = (name,) if isinstance(name, str) else name
        self.permission = permission
        self.only_to_me = only_to_me

    def command(self, name: Union[str, Tuple[str]], *,
                aliases: Optional[Iterable] = None,
                permission: Optional[int] = None,
                only_to_me: Optional[bool] = None) -> Callable:
        sub_name = (name,) if isinstance(name, str) else name
        name = self.basename + sub_name

        kwargs = {}
        if aliases is not None:
            kwargs['aliases'] = aliases
        if permission is not None:
            kwargs['permission'] = permission
        elif self.permission is not None:
            kwargs['permission'] = self.permission
        if only_to_me is not None:
            kwargs['only_to_me'] = only_to_me
        elif self.only_to_me is not None:
            kwargs['only_to_me'] = self.only_to_me
        return on_command(name, **kwargs)


def _find_command(name: Union[str, Tuple[str]]) -> Optional[Command]:
    cmd_name = (name,) if isinstance(name, str) else name
    if not cmd_name:
        return None

    cmd_tree = _registry
    for part in cmd_name[:-1]:
        if part not in cmd_tree:
            return None
        cmd_tree = cmd_tree[part]

    return cmd_tree.get(cmd_name[-1])


class _FurtherInteractionNeeded(Exception):
    """
    Raised by session.pause() indicating that the command should
    enter interactive mode to ask the user for some arguments.
    """
    pass


class _FinishException(Exception):
    """
    Raised by session.finish() indicating that the command session
    should be stopped and removed.
    """

    def __init__(self, result: bool = True):
        """
        :param result: succeeded to call the command
        """
        self.result = result


class SwitchException(Exception):
    """
    Raised by session.switch() indicating that the command session
    should be stopped and replaced with a new one (going through
    handle_message() again).

    Since the new context message will go through handle_message()
    again, the later function should be notified. So this exception
    is designed to be propagated to handle_message().
    """

    def __init__(self, new_ctx_message: Message):
        """
        :param new_ctx_message: new message which should be placed in context
        """
        self.new_ctx_message = new_ctx_message


class CommandSession(BaseSession):
    __slots__ = ('cmd', 'current_key', 'current_arg', 'current_arg_text',
                 'current_arg_images', 'args', '_last_interaction', '_running')

    def __init__(self, bot: NoneBot, ctx: Dict[str, Any], cmd: Command, *,
                 current_arg: str = '', args: Optional[Dict[str, Any]] = None):
        super().__init__(bot, ctx)
        self.cmd = cmd  # Command object
        self.current_key = None  # current key that the command handler needs
        self.current_arg = None  # current argument (with potential CQ codes)
        self.current_arg_text = None  # current argument without any CQ codes
        self.current_arg_images = None  # image urls in current argument
        self.refresh(ctx, current_arg=current_arg)
        self.args = args or {}
        self._last_interaction = None  # last interaction time of this session
        self._running = False

    @property
    def running(self):
        return self._running

    @running.setter
    def running(self, value):
        if self._running is True and value is False:
            # change status from running to not running, record the time
            self._last_interaction = datetime.now()
        self._running = value

    @property
    def is_first_run(self):
        return self._last_interaction is None

    def refresh(self, ctx: Dict[str, Any], *, current_arg: str = '') -> None:
        """
        Refill the session with a new message context.

        :param ctx: new message context
        :param current_arg: new command argument as a string
        """
        self.ctx = ctx
        self.current_arg = current_arg
        current_arg_as_msg = Message(current_arg)
        self.current_arg_text = current_arg_as_msg.extract_plain_text()
        self.current_arg_images = [s.data['url'] for s in current_arg_as_msg
                                   if s.type == 'image' and 'url' in s.data]

    @property
    def is_valid(self) -> bool:
        """Check if the session is expired or not."""
        if self._last_interaction and \
                datetime.now() - self._last_interaction > \
                self.bot.config.SESSION_EXPIRE_TIMEOUT:
            return False
        return True

    def get(self, key: str, *, prompt: str = None,
            prompt_expr: Union[str, Sequence[str], Callable] = None) -> Any:
        """
        Get an argument with a given key.

        If the argument does not exist in the current session,
        a FurtherInteractionNeeded exception will be raised,
        and the caller of the command will know it should keep
        the session for further interaction with the user.

        :param key: argument key
        :param prompt: prompt to ask the user
        :param prompt_expr: prompt expression to ask the user
        :return: the argument value
        :raise FurtherInteractionNeeded: further interaction is needed
        """
        value = self.get_optional(key)
        if value is not None:
            return value

        self.current_key = key
        # ask the user for more information
        if prompt_expr is not None:
            prompt = render(prompt_expr, key=key)
        self.pause(prompt)

    def get_optional(self, key: str,
                     default: Optional[Any] = None) -> Optional[Any]:
        """Simply get a argument with given key."""
        return self.args.get(key, default)

    def pause(self, message=None) -> None:
        """Pause the session for further interaction."""
        if message:
            asyncio.ensure_future(self.send(message))
        raise _FurtherInteractionNeeded

    def finish(self, message=None) -> None:
        """Finish the session."""
        if message:
            asyncio.ensure_future(self.send(message))
        raise _FinishException

    # noinspection PyMethodMayBeStatic
    def switch(self, new_ctx_message: Any) -> None:
        """
        Finish the session and switch to a new (fake) message context.

        The user may send another command (or another intention as natural
        language) when interacting with the current session. In this case,
        the session may not understand what the user is saying, so it
        should call this method and pass in that message, then NoneBot will
        handle the situation properly.
        """
        if self.is_first_run:
            # if calling this method during first run,
            # we think the command is not handled
            raise _FinishException(result=False)

        if not isinstance(new_ctx_message, Message):
            new_ctx_message = Message(new_ctx_message)
        raise SwitchException(new_ctx_message)


def parse_command(bot: NoneBot,
                  cmd_string: str) -> Tuple[Optional[Command], Optional[str]]:
    """
    Parse a command string (typically from a message).

    :param bot: NoneBot instance
    :param cmd_string: command string
    :return: (Command object, current arg string)
    """
    logger.debug(f'Parsing command: {cmd_string}')

    matched_start = None
    for start in bot.config.COMMAND_START:
        # loop through COMMAND_START to find the longest matched start
        curr_matched_start = None
        if isinstance(start, type(re.compile(''))):
            m = start.search(cmd_string)
            if m and m.start(0) == 0:
                curr_matched_start = m.group(0)
        elif isinstance(start, str):
            if cmd_string.startswith(start):
                curr_matched_start = start

        if curr_matched_start is not None and \
                (matched_start is None or
                 len(curr_matched_start) > len(matched_start)):
            # a longer start, use it
            matched_start = curr_matched_start

    if matched_start is None:
        # it's not a command
        logger.debug('It\'s not a command')
        return None, None

    logger.debug(f'Matched command start: '
                 f'{matched_start}{"(space)" if not matched_start else ""}')
    full_command = cmd_string[len(matched_start):].lstrip()

    if not full_command:
        # command is empty
        return None, None

    cmd_name_text, *cmd_remained = full_command.split(maxsplit=1)
    cmd_name = _aliases.get(cmd_name_text)

    if not cmd_name:
        for sep in bot.config.COMMAND_SEP:
            # loop through COMMAND_SEP to find the most optimized split
            curr_cmd_name = None
            if isinstance(sep, type(re.compile(''))):
                curr_cmd_name = tuple(sep.split(cmd_name_text))
            elif isinstance(sep, str):
                curr_cmd_name = tuple(cmd_name_text.split(sep))

            if curr_cmd_name is not None and \
                    (not cmd_name or len(curr_cmd_name) > len(cmd_name)):
                # a more optimized split, use it
                cmd_name = curr_cmd_name

        if not cmd_name:
            cmd_name = (cmd_name_text,)

    logger.debug(f'Split command name: {cmd_name}')
    cmd = _find_command(cmd_name)
    if not cmd:
        logger.debug(f'Command {cmd_name} not found')
        return None, None

    logger.debug(f'Command {cmd.name} found, function: {cmd.func}')
    return cmd, ''.join(cmd_remained)


async def handle_command(bot: NoneBot, ctx: Dict[str, Any]) -> bool:
    """
    Handle a message as a command.

    This function is typically called by "handle_message".

    :param bot: NoneBot instance
    :param ctx: message context
    :return: the message is handled as a command
    """
    ctx_id = context_id(ctx)

    # wait for 1.5 seconds (at most) if the current session is running
    retry = 5
    while retry > 0 and _sessions.get(ctx_id) and _sessions[ctx_id].running:
        retry -= 1
        await asyncio.sleep(0.3)

    check_perm = True
    session = _sessions.get(ctx_id)
    if session:
        if session.running:
            logger.warning(f'There is a session of command '
                           f'{session.cmd.name} running, notify the user')
            asyncio.ensure_future(
                send_expr(bot, ctx, bot.config.SESSION_RUNNING_EXPRESSION))
            # pretend we are successful, so that NLP won't handle it
            return True

        if session.is_valid:
            logger.debug(f'Session of command {session.cmd.name} exists')
            session.refresh(ctx, current_arg=str(ctx['message']))
            # there is no need to check permission for existing session
            check_perm = False
        else:
            # the session is expired, remove it
            logger.debug(f'Session of command {session.cmd.name} is expired')
            if ctx_id in _sessions:
                del _sessions[ctx_id]
            session = None

    if not session:
        cmd, current_arg = parse_command(bot, str(ctx['message']).lstrip())
        if not cmd:
            logger.debug('Not a known command, ignored')
            return False
        if cmd.only_to_me and not ctx['to_me']:
            logger.debug('Not to me, ignored')
            return False
        session = CommandSession(bot, ctx, cmd, current_arg=current_arg)
        logger.debug(f'New session of command {session.cmd.name} created')

    return await _real_run_command(session, ctx_id, check_perm=check_perm)


async def call_command(bot: NoneBot, ctx: Dict[str, Any],
                       name: Union[str, Tuple[str]], *,
                       current_arg: str = '',
                       args: Optional[Dict[str, Any]] = None,
                       check_perm: bool = True,
                       disable_interaction: bool = False) -> bool:
    """
    Call a command internally.

    This function is typically called by some other commands
    or "handle_natural_language" when handling NLPResult object.

    Note: If disable_interaction is not True, after calling this function,
    any previous command session will be overridden, even if the command
    being called here does not need further interaction (a.k.a asking
    the user for more info).

    :param bot: NoneBot instance
    :param ctx: message context
    :param name: command name
    :param current_arg: command current argument string
    :param args: command args
    :param check_perm: should check permission before running command
    :param disable_interaction: disable the command's further interaction
    :return: the command is successfully called
    """
    cmd = _find_command(name)
    if not cmd:
        return False
    session = CommandSession(bot, ctx, cmd, current_arg=current_arg, args=args)
    return await _real_run_command(session, context_id(session.ctx),
                                   check_perm=check_perm,
                                   disable_interaction=disable_interaction)


async def _real_run_command(session: CommandSession,
                            ctx_id: str,
                            disable_interaction: bool = False,
                            **kwargs) -> bool:
    if not disable_interaction:
        # override session only when interaction is not disabled
        _sessions[ctx_id] = session
    try:
        logger.debug(f'Running command {session.cmd.name}')
        session.running = True
        res = await session.cmd.run(session, **kwargs)
        raise _FinishException(res)
    except _FurtherInteractionNeeded:
        session.running = False
        if disable_interaction:
            # if the command needs further interaction, we view it as failed
            return False
        logger.debug(f'Further interaction needed for '
                     f'command {session.cmd.name}')
        # return True because this step of the session is successful
        return True
    except (_FinishException, SwitchException) as e:
        session.running = False
        logger.debug(f'Session of command {session.cmd.name} finished')
        if not disable_interaction and ctx_id in _sessions:
            # the command is finished, remove the session,
            # but if interaction is disabled during this command call,
            # we leave the _sessions untouched.
            del _sessions[ctx_id]

        if isinstance(e, _FinishException):
            return e.result
        elif isinstance(e, SwitchException):
            # we are guaranteed that the session is not first run here,
            # which means interaction is definitely enabled,
            # so we can safely touch _sessions here.
            if ctx_id in _sessions:
                # make sure there is no session waiting
                del _sessions[ctx_id]
            logger.debug(f'Session of command {session.cmd.name} switching, '
                         f'new context message: {e.new_ctx_message}')
            raise e  # this is intended to be propagated to handle_message()
