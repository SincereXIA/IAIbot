def encodenum(num):
    num = str(num)
    line =""
    for c in num:
        line += chr(int(c) + ord('a'))
    return line

def decodenum(line):
    num = ""
    for c in line:
        num += str(ord(c)-ord('a'))
    return num