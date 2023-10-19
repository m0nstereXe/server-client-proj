import sys
import hashlib


def hash(msg, key):
    hsh = hashlib.sha256(msg.encode("ASCII"))
    hsh.update(key.encode("ASCII"))            
    return hsh.hexdigest()


def getMessages(messageFile):
    file = open(messageFile, "r")
    arr = []
    for line in file:
        n = int(line.strip())
        msg = ""
        for i in range(n):
            msg += file.read(1)
        arr.append(msg.strip())
    return arr

def getfile(f):
    file = open(f, "r")
    arr = []
    for line in file:
        arr.append(line.strip())
    file.close()
    return arr

#escapes \ and .
def escape(msg):
    msg = msg.replace("\\", "\\\\")
    msg = msg.replace(".", "\\.")
    return msg
def unescape(msg):
    msg = msg.replace("\\.", ".")
    msg = msg.replace("\\\\", "\\")
    return msg

def main():
    msgFile = sys.argv[1]
    sigFile = sys.argv[2]
    keyFile = sys.argv[3]

    messages = getMessages(msgFile)
    signatures = getfile(sigFile)
    keys = getfile(keyFile)

    n = len(messages)

    for i in range(n):
        msg,sig,key = messages[i],signatures[i],keys[i]
        print(msg)
        hsh = hash(msg,key)
        print(hsh)
        print(sig)
        if(hsh != sig):
            print("FAIL")
        else:
            print("PASS")


if __name__ == "__main__":
    main()