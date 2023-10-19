#local host server

import socket
import sys
import hashlib

GOOD = "260 OK\n"
SIG = "270 SIG\n"


def getfile(f):
    file = open(f, "r")
    arr = []
    for line in file:
        arr.append(line.strip())
    file.close()
    return arr

#prints out responses so i dont have to keep typing it
def get(sock):
    res = sock.recv(1024).decode("ASCII").strip()
    print(res)
    return res
#get just one byte
def getByte(sock):
    res = sock.recv(1).decode("ASCII")
    return res

def hash(msg, key):
    hsh = hashlib.sha256(msg.encode("ASCII"))
    hsh.update(key.encode("ASCII"))            
    return hsh.hexdigest()

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
    keyFile = sys.argv[2]
    keys = getfile(keyFile)

    serverPort = int(sys.argv[1])
    ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ss.bind(('', serverPort))

    ss.listen(1)    
    cs, addr = ss.accept()
    res = get(cs)
    #initial hello
    if res != "HELLO":
        print("ERROR")
        cs.close()
        ss.close()
        return
    cs.send(GOOD.encode("ASCII"))
    i = 0
    while True:
        for k in keys:
            cmd = get(cs)
            if cmd == "DATA":
                msg = ""
                dt = getByte(cs)
                while dt != "\n":
                    msg += dt
                    dt = getByte(cs)
                msg = unescape(msg)
                print(msg)
                dt = get(cs)
                hsh = hash(msg,k) 
                cs.send(SIG.encode("ASCII"))
                cs.send(hsh.encode("ASCII"))
                pf = get(cs)
                if pf != "PASS" and pf != "FAIL":
                    print("ERROR")
                    cs.close()
                    break
                cs.send(GOOD.encode("ASCII"))
            else:
                if(cmd != "QUIT"):
                    print("ERROR")
                cs.close()
                ss.close()
                return

if __name__ == "__main__":
    main()