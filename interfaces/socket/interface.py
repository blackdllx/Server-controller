import socket
import pickle
import logging
from . import classes

# class interface:
#     def __init__(self) -> None:
#         print("RUN")
#         self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         try:
#             self.S.bind(("localhost", 9999))
#         except:
#             self.S.bind(("localhost", 9998))
#         self.S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         self.ConnectionHandler()

#     def ConnectionHandler(self):
#         self.S.listen()
#         while True:
#             conn = S.accept()[0]
            
#             while True:
#                 try:
#                     request = pickle.loads(conn.recv(5048))
#                 except:break
#                 self.RequestHandler(conn, request)

#     def RequestHandler(self):
#         match request.__class__:
#             case classes.HandShake.Request:
#                 logging.log(logging.DEBUG, "HandShake request")
#                 logging.log(logging.DEBUG, f"Config password: {CFG['password']}, request password: {request.password}")
#                 try:
#                     if request.password == CFG["password"]:
#                         logging.info("Currect password")
#                         s.sendall(pickle.dumps(classes.HandShake.Response(status=classes.StatusCodes.GOOD)))
#                     else:
#                         logging.info("Uncurrect password")
#                         s.sendall(pickle.dumps(classes.HandShake.Response(status=classes.StatusCodes.UNCORECT_PASWORD)))
#                 except:
#                     logging.info("Error")
#                     s.sendall(pickle.dumps(classes.HandShake.Response(status=classes.StatusCodes.BAD)))



#             case classes.ServersInfo.Request:
#                 try:
#                     logging.log(logging.DEBUG, "ServerInfo request")
#                     if auth(request.password):
#                         logging.log(logging.DEBUG, "auth success")
#                         h = []
#                         for i in Servers:
#                             h.append(i.exportInfo())
#                         logging.log(logging.DEBUG, "Sending")
#                         s.sendall(pickle.dumps(classes.ServersInfo.Response(classes.StatusCodes.GOOD, h)))
#                         del h
#                     else:s.sendall(pickle.dumps(classes.ServersInfo.Response(classes.StatusCodes.UNCORECT_PASWORD)))
#                 except Exception as er:
#                     logging.error(er)
#                     s.sendall(pickle.dumps(classes.ServersInfo.Response(classes.StatusCodes.BAD)))
#             case classes.ServerController.Request:
#                 # try:
#                     logging.log(logging.DEBUG, "ServerController request")
#                     if auth(request.password):
#                         logging.info(Servers[int(request.id)].actions[request.action])
#                         Servers[int(request.id)].actions[request.action]()
#                         s.sendall(pickle.dumps(classes.ServerController.Response(classes.StatusCodes.GOOD)))
#                     else:
#                         s.sendall(pickle.dumps(classes.ServerController.Response(classes.StatusCodes.UNCORECT_PASWORD)))
#                 # except:s.sendall(pickle.dumps(classes.ServerController.Response(classes.StatusCodes.BAD)))
#             case classes.ServerCommand.Request:
#                 # try:
#                     logging.log(logging.DEBUG, "ServerCommand request")
#                     if auth(request.password):
#                         Servers[int(request.id)].send(request.command)
#                         s.sendall(pickle.dumps(classes.ServerCommand.Response(classes.StatusCodes.GOOD)))
#                     else: s.sendall(pickle.dumps(classes.ServerCommand.Response(classes.StatusCodes.UNCORECT_PASWORD)))
#                 # except:
#                 #         s.sendall(pickle.dumps(classes.ServerCommand.Response(classes.StatusCodes.BAD)))
#             case classes.GetLog.Request:
#                 try:
#                     logging.log(logging.DEBUG, "GetLog request")
#                     if auth(request.password):
#                         s.sendall(pickle.dumps(
#                             classes.GetLog.Response(classes.StatusCodes.GOOD, Servers[request.id].consoleLog[-20:])))
#                     else: s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.UNCORECT_PASWORD)))
#                 except:
#                     s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.BAD)))


# def OpenServer():
#     global S
#     S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     try:
#         S.bind(("localhost", 9999))
#     except:
#         S.bind(("localhost", 9998))
#     S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     ConnectionHandler()

# def ConnectionHandler():
#     S.listen()
#     while True:
#         conn, addr = S.accept()
        
#         while True:
#             try:
#                 request = pickle.loads(conn.recv(5048))
#             except:break
#             RequestHandler(conn, request)


print("RUN")
self.S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    elf.S.bind(("localhost", 9999))
except:
    self.S.bind(("localhost", 9998))
    self.S.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.ConnectionHandler()

def ConnectionHandler(self):
    self.S.listen()
    while True:
        conn = S.accept()[0]
            
        while True:
            try:
                request = pickle.loads(conn.recv(5048))
            except:break
            self.RequestHandler(conn, request)

def RequestHandler(self):
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
                    s.sendall(pickle.dumps(classes.HandShake.Response(status=classes.StatusCodes.UNCORECT_PASWORD)))
            except:
                logging.info("Error")
                s.sendall(pickle.dumps(classes.HandShake.Response(status=classes.StatusCodes.BAD)))



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
                    s.sendall(pickle.dumps(
                        classes.GetLog.Response(classes.StatusCodes.GOOD, Servers[request.id].consoleLog[-20:])))
                else: s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.UNCORECT_PASWORD)))
            except:
                s.sendall(pickle.dumps(classes.GetLog.Response(classes.StatusCodes.BAD)))


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
        
        while True:
            try:
                request = pickle.loads(conn.recv(5048))
            except:break
            RequestHandler(conn, request)


