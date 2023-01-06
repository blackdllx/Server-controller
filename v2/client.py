import socket
import logging
import pickle

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


if __name__ == '__main__':
    ConnectSocket()
    print(send(classes.ServersInfo.Request("1234")).__dict__)



