import socket
import logging
import classes
import pickle
import json
import os
import subprocess
import threading
import time


logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)


with open("config.json", "rb")as f:
    CFG = json.load(f)
Servers=[]

class Server:
    active=False
    def __init__(self, id):
        self.console = None
        self.id = id
        self.dir = f"Servers/{id}/"
        self.basePath = os.getcwd()
        self.pa = ""
        self.consoleLog=[]

    def sss(self):
        print(self.consoleLog)
    def start(self):
        if not self.pa == os.getcwd():
            os.chdir(self.dir)
            self.pa=os.getcwd()
        if not self.active:
            self.console = subprocess.Popen(f". ./start.sh", shell=True, stdout=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
            self.active=True
            threading.Thread(target=self.parse).start()

    def stop(self):
        if self.active:
            self.console.stdin.write(b"stop")
            self.active=False

    def parse(self):
        while self.active:
            if not self.console.poll():
                f=self.console.stdout.readline()
                if f != b"":
                    print(f.decode())
                    self.consoleLog.append(f)

    def send(self, command: str):
        if self.active:
            self.console.stdin.write((command).encode() + b"\n")
            self.console.stdin.flush()


# out = cmd.communicate()[0].decode() sr=Server(0);sr.start() sr.sss() sr.console.stdout.write(b"help\n")
def HandShake(request):
        logging.log(logging.DEBUG, "HandShake response")
        logging.log(logging.DEBUG, f"Config password: {CFG['password']}, request password: {request.password}")
        try:
            if request.password == CFG["password"]:
                logging.info("Currect password")
                return classes.HandShake.Response(status=classes.StatusCodes.GOOD)
            logging.info("Uncurrect password")
            return classes.HandShake.Response(status=classes.StatusCodes.UNCORECT_PASWORD)
        except:
            logging.info("Error")
            return classes.HandShake.Response(status=classes.StatusCodes.BAD)

def OpenServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("localhost", 9999))
    except:
        s.bind(("localhost", 9998))
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return s
def ConnectionHandler(s: socket.socket):
    s.listen()
    while True:
        conn, addr = s.accept()
        logging.log(logging.DEBUG, "Connection added")
        while True:
            request = pickle.loads(conn.recv(5048))
            logging.log(logging.DEBUG,"New request")
            RequestHandler(conn, request)

def RequestHandler(s: socket.socket, request):
    match request.__class__:
        case classes.HandShake.Request:
            logging.log(logging.DEBUG,"HandShake request")
            s.sendall(pickle.dumps(HandShake(request)))
        case classes.ServersInfo.Request:
            pass
        case classes.ServerController.Request:
            pass
        case classes.ServerCommand.Request:
            pass
        case classes.GetLog.Request:
            pass

def ServerInit():
    if os.path.isdir("Servers"):
        for i in range(CFG["ServerCount"]):
            if os.path.isdir("Servers/" + str(i)):
                pass
            else:
                os.mkdir("Servers/" + str(i))
                with open(f"Servers/{i}/start.sh", "w") as f:
                    f.write(f"java -Xmx1024M -Xms1024M -jar Servers/{i}/server.jar nogui")
    else:
        os.mkdir("Servers")


if __name__ == '__main__':
    ServerInit()
    sr = Server(0)
    sr.start()
    time.sleep(15)
    print("Sending!!!!!!!!!!!!!!!!!!!!!!!!!!")
    sr.send("help")

