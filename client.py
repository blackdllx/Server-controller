import logging
import pickle
import select
import socket
import struct
import time
import netstruct
import minestat

import classes

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

PORTS = [25565, 25566, 25567]


def getServers(host):
    servers = []
    ips = ["pvp.thearchon.net", "play.extremecraft.net"]
    ports = [25565, 25565]
    for i in range(2):
        serv = minestat.MineStat(ips[i], ports[i], query_protocol=minestat.SlpProtocols.JSON)
        servers.append([i, serv])

    return servers

def connectSocket(ip,port: int):
    global s, SOCKET_TIMEOUT
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("localhost", 9999))
    s.setblocking(0)
    SOCKET_TIMEOUT = 5


def RecvStatus(s: socket.socket):
    sTime = time.time()
    while time.time() - sTime < SOCKET_TIMEOUT:
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
            if _class.__class__ == classes.GetLog:
                response = s.recv(5000).decode()
                return response
            response = netstruct.unpack(_class.format, s.recv(5000))
            return response
    return None


def send_v2(_class):
    with open("ClassBytes", "rb") as f:
        logging.info("SEND - Reading byte-keys...")
        byts: dict = pickle.load(f)
        logging.info(f"SEND - Read byte-keys = {byts}")
    for i in byts:
        if byts[i] == _class.__class__:
            logging.info("SEND - Sending request key...")
            logging.info(f"SEND - class = {_class.__class__}")
            s.sendall(i)
            break
    if RecvStatus(s) != b"OK":
        logging.error("SEND - Receive status bad")
        return ''
    if _class.format:
        # logging.info(f"SEND - Sending request data... {netstruct.pack(_class.format, *_class.values)}")
        if _class.__class__ == classes.Command or _class.__class__ == classes.GetLog or _class.__class__ == classes.HandShake:
            s.sendall(netstruct.pack(_class.format, *_class.values))
        else:
            s.sendall(struct.pack(_class.format, *_class.values))
        if _class.response:
            logging.info("SEND - Receiving data...")
            dt = RecvResponse(s, _class)
            if not dt:
                return ""
            logging.info(f"SEND - Data = {dt}")
            return dt
