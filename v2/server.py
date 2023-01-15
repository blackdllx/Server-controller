import json
import logging
import os
import pickle
import socket
import subprocess
import threading

import classes

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

with open("config.json", "rb") as f:
    CFG = json.load(f)
Servers = []
S=None
BASEPATH = os.getcwd()

class Server:
    active = False

    def __init__(self, id):
        self.actions={"start": self.start, "stop": self.stop}
        self.console = None
        self.id = id
        self.dir = f"/Servers/{id}/"
        self.pa = ""
        self.consoleLog = []
        self.properties = {}
        self.loadProperties()

    def loadProperties(self):
        if not self.pa == os.getcwd():
            os.chdir(BASEPATH+self.dir)
            self.pa = os.getcwd()

        with open("./server.properties", "rb") as f:
            data = f.read().decode()
            for i in data.split("\n"):
                if i != "" and not i[0] == "#":
                    self.properties.update({i.split('=')[0]: i.split("=")[1]})

    def saveProperties(self):
        if not self.pa == os.getcwd():
            os.chdir(BASEPATH+self.dir)
            self.pa = os.getcwd()
        if self.properties != {}:
            out = ''
            for i in self.properties:
                out = out + f"{i}={self.properties[i]}\n"
            print(out)
            with open("./server.properties", "wb") as f:
                f.write(out.encode())

    def start(self):
        print("starting")
        if not self.pa == os.getcwd():
            os.chdir(BASEPATH+self.dir)
            self.pa = os.getcwd()
        if not self.active:
            self.console = subprocess.Popen(f". ./start.sh", shell=True, stdout=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
            self.active = True
            threading.Thread(target=self.parse).start()
            print("started")

    def stop(self):
        if self.active:
            self.console.stdin.write(b"stop\n")
            self.console.stdin.flush()
            self.active = False

    def parse(self):
        while self.active:
            if not self.console.poll():
                f = self.console.stdout.readline()
                if f != b"":
                    print(f.decode(), end="")
                    self.consoleLog.append(f)

    def send(self, command: str):
        if self.active:
            self.console.stdin.write((command).encode() + b"\n")
            self.console.stdin.flush()

    def exportInfo(self):
        return {"id": self.id, "settings": self.properties}

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
    global S
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        S.bind(("localhost", 9999))
    except:
        S.bind(("localhost", 9998))
    S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ConnectionHandler()


def ConnectionHandler():
    S.listen()
    while True:
        conn, addr = S.accept()
        logging.log(logging.DEBUG, "Connection added")
        while True:
            try:
                request = pickle.loads(conn.recv(5048))
            except:break
            logging.log(logging.DEBUG, "New request")
            RequestHandler(conn, request)

def auth(password):
    if password == CFG["password"]:
        logging.info("Currect password")
        return True
    else:
        logging.info("Uncurrect password")
        return False
def RequestHandler(s: socket.socket, request):
    match request.__class__:
        case classes.HandShake.Request:
            logging.log(logging.DEBUG, "HandShake request")
            logging.log(logging.DEBUG, f"Config password: {CFG['password']}, request password: {request.password}")
            try:
                if request.password == CFG["password"]:
                    logging.info("Currect password")
                    s.sendall(pickle.dumps(classes.HandShake.Response(status=classes.StatusCodes.GOOD)))
                else:
                    logging.info("Uncurrect password")
                    s.sendall(pickle.dumps( classes.HandShake.Response(status=classes.StatusCodes.UNCORECT_PASWORD)))
            except:
                logging.info("Error")
                s.sendall(pickle.dumps( classes.HandShake.Response(status=classes.StatusCodes.BAD)))



        case classes.ServersInfo.Request:
            try:
                logging.log(logging.DEBUG, "ServerInfo request")
                if auth(request.password):
                    logging.log(logging.DEBUG, "auth success")
                    h = []
                    for i in Servers:
                        h.append(i.exportInfo())
                    logging.log(logging.DEBUG, "Sending")
                    s.sendall(pickle.dumps(classes.ServersInfo.Response(classes.StatusCodes.GOOD, h)))
                    del h
                else:s.sendall(pickle.dumps(classes.ServersInfo.Response(classes.StatusCodes.UNCORECT_PASWORD)))
            except Exception as er:
                logging.error(er)
                s.sendall(pickle.dumps(classes.ServersInfo.Response(classes.StatusCodes.BAD)))
        case classes.ServerController.Request:
            # try:
                logging.log(logging.DEBUG, "ServerController request")
                if auth(request.password):
                    logging.info(Servers[int(request.id)].actions[request.action])
                    Servers[int(request.id)].actions[request.action]()
                    s.sendall(pickle.dumps(classes.ServerController.Response(classes.StatusCodes.GOOD)))
                else:
                    s.sendall(pickle.dumps(classes.ServerController.Response(classes.StatusCodes.UNCORECT_PASWORD)))
            # except:s.sendall(pickle.dumps(classes.ServerController.Response(classes.StatusCodes.BAD)))
        case classes.ServerCommand.Request:
            # try:
                logging.log(logging.DEBUG, "ServerCommand request")
                if auth(request.password):
                    Servers[int(request.id)].send(request.command)
                    s.sendall(pickle.dumps(classes.ServerCommand.Response(classes.StatusCodes.GOOD)))
                else: s.sendall(pickle.dumps(classes.ServerCommand.Response(classes.StatusCodes.UNCORECT_PASWORD)))
            # except:
            #         s.sendall(pickle.dumps(classes.ServerCommand.Response(classes.StatusCodes.BAD)))
        case classes.GetLog.Request:
            try:
                logging.log(logging.DEBUG, "GetLog request")
                if auth(request.password):
                    s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.GOOD, Servers[request.id].consoleLog[-20:])))
                else: s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.UNCORECT_PASWORD)))
            except:
                s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.BAD)))


def ServerInit():
    if os.path.isdir("Servers"):
        for i in range(CFG["ServerCount"]):
            if os.path.isdir("Servers/" + str(i)):
                pass
            else:
                os.mkdir("Servers/" + str(i))
                with open(f"Servers/{i}/start.sh", "w") as f:
                    f.write(f"java -Xmx1024M -Xms1024M -jar server.jar nogui")
    else:
        os.mkdir("Servers")
        ServerInit()
    for i in range(CFG["ServerCount"]):
        Servers.append(Server(i))


if __name__ == '__main__':
    ServerInit()
    OpenServer()
