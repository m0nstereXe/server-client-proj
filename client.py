import socket 
import sys



def getMessages(messageFile):
    file = open(messageFile, "r")
    arr = []
    for line in file:
        n = int(line.strip())
        msg = file.read(n)
        arr.append(msg)
    return arr

def getfile(f):
    file = open(f, "r")
    arr = []
    for line in file:
        arr.append(line.strip())
    file.close()
    return arr 

GOOD = "260 OK"
SIG = "270 SIG"

def get(sock):
    res = sock.recv(1024).decode("ASCII").strip()
    print(res)
    return res

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
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    messageFile = sys.argv[3]
    signatureFile = sys.argv[4]

    messages = getMessages(messageFile)
    signatures = getfile(signatureFile)
    n = len(messages)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverName, serverPort))
    s.send("HELLO\n".encode("ASCII"))

    res = get(s)
    if res != GOOD:
        print("ERROR")
        s.close()
        return
    for i in range(n):
        msg,sig = messages[i],signatures[i]
        msg = msg + "\n.\n"
        s.send("DATA\n".encode("ASCII"))
        s.send(msg.encode("ASCII"))
        res = get(s)
        if res != SIG:
            print("ERROR")
            s.close()
            return
        res = get(s)
        if res != sig:
            s.send("FAIL\n".encode("ASCII"))
        else:
            s.send("PASS\n".encode("ASCII"))
    
        res = get(s)
        if res != GOOD:
            print("ERROR")
            s.close()
            return
    
    s.send("QUIT".encode("ASCII"))
    s.close()
if __name__ == "__main__":
    main()