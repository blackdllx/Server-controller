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
SOCKET_TIMEOUT=10

def RecvStatus(s:socket.socket):
    sTime = time.time()
    while time.time()-sTime < SOCKET_TIMEOUT:
        logging.info("RECEIVE(status) - Waiting for response...")
        read, write, error = select.select([s], [], [], 0.5)
        print(read, write, error)
        for i in read:
            status = s.recv(2048)
            logging.info(f"RECEIVE(status) - Response code = {status}")
            return status

    logging.error("RECEIVE(status) - Connection timeout")
    return None
def RecvResponse(s, _class):
    sTime = time.time()
    while time.time() - sTime < SOCKET_TIMEOUT:
        logging.info("RECEIVE(response) - Waiting for response...")
        read, write, error = select.select([s], [], [], 0.5)
        for i in read:
            response = struct.unpack(_class.format, s.recv(5000))
            return response
    return None
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
    if _class.format:
        logging.info(f"SEND - Sending request data... {_class.format, 3.1}")
        s.sendall(struct.pack(_class.format, 12.43))

        logging.info("SEND - Receiving data...")
        dt = RecvResponse(s, _class)
        logging.info(f"SEND - Data = {dt}")
        if not dt:
            return ""


# send(classes.Request.HandShake())
send_v2(s, classes.Request.Test())