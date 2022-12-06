import logging
import pickle
import select
import struct
import classes
import socket
import time

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 9998))
s.setblocking(0)
SOCKET_TIMEOUT=5
def send(_class):
    with open("ClassBytes", "rb") as f:
        byts: dict = pickle.load(f)
        print(byts)
    for i in byts:
        if byts[i] == _class.__class__:
            s.sendall(i)
            break
    sTime = time.time()
    while True:
        if time.time()-sTime < SOCKET_TIMEOUT:
            data=None
            try:data=s.recv(2048)
            except:pass
            print(data)
            if not data:
                continue
        else:
            print("socket timeout")
            return ""
    if data == b"OK":
        print("data received")
    if data == b"ERROR":
        print("unexpected error")
        return ''
    print("server found requested class")
    print(_class.format, *_class.values)
    s.sendall(struct.pack(_class.format, *_class.values))
    while True:
        if time.time()-sTime < SOCKET_TIMEOUT:
            data=s.recv(2048)
            print(data)
            if not data:
                continue
        else:
            print("socket timeout")
            return ""
    if data == b"OK":
        print("data received")
    if data == b"ERROR":
        print("unexpected error")
        return ''
    print("server received data success fully")

def RecvStatus(s:socket.socket):
    sTime = time.time()
    while time.time()-sTime < 5:
        flag = False
        logging.info("RECEIVE(status) - Waiting for response...")
        read, write, errors = select.select([s], [s], [], 0.5)
        for i in read:
            status = s.recv(2048)
            logging.info(f"RECEIVE(status) - Response code = {status}")
            flag=True
        for i in write:
            pass
        for i in errors:
            logging.warn("RECEIVE(status) - Error")
    if not flag:
        logging.error("RECEIVE(status) - Connection timeout")
        return None
    return status
def RecvResponse(s):
    pass
def send_v2(s, _class):
    with open("ClassBytes", "rb") as f:
        logging.info("SEND - Reading byte-keys...")
        byts: dict = pickle.load(f)
        logging.info(f"SEND - Read byte-keys = {byts}")
    for i in byts:
        if byts[i] == _class.__class__:
            logging.info("SEND - Sending request key...")
            s.sendall(i)
            break
    if RecvStatus(s) != b"OK":
        logging.error("SEND - Receive status bad")
        return ''
    # logging.info("SEND - Sending request data...")
    # s.sendall(struct.pack(_class.format, *_class.values))
    # if RecvStatus(s) != b"OK":
    #     logging.error("SEND - Receive status bad")
    #     return ''

# send(classes.Request.HandShake())
send_v2(s, classes.Request.HandShake())