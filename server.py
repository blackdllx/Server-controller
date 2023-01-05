import logging
import pickle
import select
import socket
import struct
import time
import netstruct
import subprocess

import classes

PASSWORD="1234".encode()


logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 9999))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(0)


def ReadRequesKey(s: socket.socket):
    while True:
        logging.info("RECEIVE - Waiting for data...")
        read, write, error = select.select([s], [s], [], 0.5)

        for i in read:
            logging.info("RECEIVE - Reading key...")
            key = s.recv(2048)
            if key == b'':break
            logging.info(f"RECEIVE - Key = {key}")
            return key
    ReadRequesKey(s)

def StartServer(id):
    cmd = subprocess.Popen(f". {id}/start.sh", shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
    servers.append([id, cmd])

def StopServer(id):
    servers[id].stdin.write("stop")
    servers.remove(id)

def GetLogs(id):
    with open(f"{id}/logs/latest.log")as f:
        return f.read(3352)

servers = []

while True:
        s.listen()
        read, write, error = select.select([s], [s], [], 0.5)
        with open("ClassBytes", "rb") as f:
            byts: dict = pickle.load(f)
        for i in read:
            conn, addr = s.accept()
            while True:

                logging.info("MAIN - Connected")
                key = ReadRequesKey(conn)
                if key == b'':
                    continue
                logging.info(f"MAIN - Requset class = {byts[key]}")
                logging.info("MAIN - Sending response status")
                conn.send(b"OK")


                match byts[key]:

                    case classes.HandShake:
                        # logging.info("MAIN - Running command..")
                        while True:
                            flag = False
                            read, write, error = select.select([conn], [conn], [], 0.5)
                            logging.info("MAIN - Waiting data..")
                            for i in read:
                                logging.info("MAIN - Reading data")
                                data = netstruct.unpack(classes.HandShake(''.encode()).format, conn.recv(5000))
                                logging.info(f"MAIN - Data = {data}")
                                flag = True
                            if flag: break
                        if data[-1] == PASSWORD:
                            conn.send(netstruct.pack(classes.HandShake(b'').format, *classes.HandShake(b'GOOD').values))
                        conn.send(netstruct.pack(classes.HandShake(b'').format, *classes.HandShake(b'BAD').values))

                    case classes.GetServers:
                        logging.info("MAIN - Sending server list..")
                        while True:
                            flag = False
                            read, write, error = select.select([conn], [conn], [conn], 0.5)
                            logging.info("MAIN - Waiting data..")
                            for i in read:
                                logging.info("MAIN - Reading data")
                                data = netstruct.unpack(classes.GetServers('', 0).format, conn.recv(5000))
                                logging.info(f"MAIN - Data = {data}")
                                flag = True
                            if flag: break
                        if data[-1] == PASSWORD:
                            conn.sendall(netstruct.pack(classes.GetServers.fortmat, *classes.GetServers(len(servers), b'')))


                    case classes.Command:
                        logging.info("MAIN - Running command..")
                        while True:
                            flag = False
                            read, write, error = select.select([conn], [conn], [], 0.5)
                            logging.info("MAIN - Waiting data..")
                            for i in read:
                                logging.info("MAIN - Reading data")
                                data = netstruct.unpack(classes.Command('', 0).format, conn.recv(5000))
                                logging.info(f"MAIN - Data = {data}")
                                flag = True
                            if flag: break
                        if data[-1] == PASSWORD:
                            if servers:
                                servers[data[1]].stdin.write(data[0])
                        continue

                    case classes.StartServer:
                        logging.info("MAIN - Running command..")
                        while True:
                            flag = False
                            read, write, error = select.select([conn], [conn], [], 0.5)
                            logging.info("MAIN - Waiting data..")
                            for i in read:
                                logging.info("MAIN - Reading data")
                                data = netstruct.unpack(classes.StartServer(0).format, conn.recv(5000))
                                logging.info(f"MAIN - Data = {data}")
                                flag = True
                            if flag: break
                        if data[-1] == PASSWORD:
                            logging.info("Starting server")
                            StartServer(data[0])
                            logging.info(f"Server started {servers}")
                        continue

                    case classes.GetLog:
                        logging.info("MAIN - Running command..")
                        while True:
                            flag = False
                            read, write, error = select.select([conn], [conn], [], 0.5)
                            logging.info("MAIN - Waiting data..")
                            for i in read:
                                logging.info("MAIN - Reading data")
                                data = netstruct.unpack(b"ib$", conn.recv(5000))
                                logging.info(f"MAIN - Data = {data}")
                                flag = True
                            if flag: break
                        if data[-1] == PASSWORD:
                            if servers:
                                conn.send(GetLogs(data[0]).encode())
                        continue
