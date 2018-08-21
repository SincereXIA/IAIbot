# -*- coding: utf-8 -*-
import socket
import asyncore
class Receiver(asyncore.dispatcher):
    def __init__(self, conn):
        asyncore.dispatcher.__init__(self, conn)
        self.from_remote_buffer = b''
        self.to_remote_buffer = b''
        self.sender = None
    def handle_connect(self):
        pass
    def handle_read(self):
        read = self.recv(4096)
        # print '%04i -->'%len(read)
        self.from_remote_buffer += read
    def writable(self):
        return len(self.to_remote_buffer) > 0
    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        # print '%04i <--'%sent
        self.to_remote_buffer = self.to_remote_buffer[sent:]
    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()
class Sender(asyncore.dispatcher):
    def __init__(self, receiver, remoteaddr, remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((remoteaddr, remoteport))
    def handle_connect(self):
        pass
    def handle_read(self):
        read = self.recv(4096)
        # print '<-- %04i'%len(read)
        self.receiver.to_remote_buffer += read
    def writable(self):
        return len(self.receiver.from_remote_buffer) > 0
    def handle_write(self):
        sent = self.send(self.receiver.from_remote_buffer)
        # print '--> %04i'%sent
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]
    def handle_close(self):
        self.close()
        self.receiver.close()
class Forwarder(asyncore.dispatcher):
    def __init__(self, ip, port, remoteip, remoteport, backlog=5):
        asyncore.dispatcher.__init__(self)
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((ip, port))
        self.listen(backlog)
    def handle_accept(self):
        conn, addr = self.accept()
        # print '--- Connect --- '
        self.log_info('Connected from %s:%s to %s:%s' % (addr[0], addr[1], self.remoteip, self.remoteport))
        rv =
        s1 = Sender(Receiver(conn), self.remoteip, self.remoteport)
        s2 = Sender(Receiver(conn), '127.0.0.1', 8084)
if __name__ == '__main__':
    f = Forwarder('127.0.0.1', 8083, '127.0.0.1', 8082)
    asyncore.loop()