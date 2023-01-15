import socket
import logging
import pickle
import threading
import time

import classes

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
S = None

def ConnectSocket(ip: str = "localhost", port: int = 9999):
    global S
    S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        S.connect((ip, port))
    except Exception as error:
        S.connect((ip, 9998))
        logging.error(error)

def HandShake(password):
    S.sendall(pickle.dumps(classes.HandShake.Request(password=password)))
    response = pickle.loads(S.recv(5048))
    return response.status

def send(protocol):
    S.sendall(pickle.dumps(protocol))
    return pickle.loads(S.recv(8000))

def Status2Text(status):
    match status:
        case classes.StatusCodes.GOOD: return "Good response"
        case classes.StatusCodes.BAD: return "An error ocured in response"
        case classes.StatusCodes.UNCORECT_PASWORD: return "Your password is uncorrect"

def ShowLog():
    lg=[[],[]]
    bf=[b"",b""]
    # while True:
    #     time.sleep(0.3)
    #     log = send(classes.GetLog.Request("1234", 0))
    #     if log.status == classes.StatusCodes.GOOD:
    #         for i in log.log:
    #             if not i in lg:
    #                 lg.append(i)
    #                 print(i.decode(), end="")
    while True:
        time.sleep(0.5)
        for h in range(2):
            log = send(classes.GetLog.Request("1234", h))
            if log.status == classes.StatusCodes.GOOD:
                        for i in log.log:
                            if not i in lg[h]:
                                 lg[h].append(i)
                                 bf[h] = bf[h]+i
                                 print(f"{h} -- " + i.decode(), end="")
                                 with open(f"{h}.log", "wb") as f:
                                     f.write(bf[h])


def UI():
    while True:
        i=input("Actions \n1: HandShake \n2: Start Server \n3: Stop Server \n4: Parce Console \n5: Send Command\n")
        match int(i):
            case 1:
                print(send(classes.HandShake.Request("1234")).__dict__)
            case 2:
                f = input("Select Server \n1: {Server name} \n2: {Server name}")
                print(send(classes.ServerController.Request("1234", f, "start")).__dict__)

            case 3:
                f = input("Select Server \n1: {Server name} \n2: {Server name}")
                print(send(classes.ServerController.Request("1234", f, "stop")).__dict__)

            case 4:
                f = input("Select Server \n1: {Server name} \n2: {Server name}")
                print("console parced")

            case 5:
                f = input("Select Server \n1: {Server name} \n2: {Server name}")
                b = input("Command --> ")
                print(send(classes.ServerCommand.Request("1234", f, b)).__dict__)



if __name__ == '__main__':
    ConnectSocket()
    # threading.Thread(target=ShowLog).start()
    UI()
    # print(send(classes.ServersInfo.Request("1234")).__dict__)
    # print(send(classes.ServerController.Request("1234", 0, "start")).__dict__)
    # print(send(classes.ServerController.Request("1234", 1, "start")).__dict__)

    # # # input()
    # # print(send(classes.ServerCommand.Request("1234", 0, "help")).__dict__)
    # # print(send(classes.GetLog.Request("1234", 0)).__dict__)
    # input()
    # print(send(classes.ServerController.Request("1234", 0, "stop")).__dict__)
    # print(send(classes.ServerController.Request("1234", 1, "stop")).__dict__)

