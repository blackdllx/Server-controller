import logging
import pickle
import select
import socket
import struct
import time

import classes

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 9998))
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.setblocking(0)


def ReadRequesKey(s: socket.socket):
    while True:
        logging.info("RECEIVE - Waiting for data...")
        read, write, error = select.select([s], [s], [], 0.5)
        for i in read:
            logging.info("RECEIVE - Reading key...")
            key = s.recv(2048)
            logging.info(f"RECEIVE - Key = {key}")
            return key


while True:
    try:
        s.listen()
        read, write, error = select.select([s], [s], [], 0.5)
        with open("ClassBytes", "rb") as f:
            byts: dict = pickle.load(f)
        for i in read:
            conn, addr = s.accept()
            logging.info("MAIN - Connected")
            key = ReadRequesKey(conn)
            logging.info(f"MAIN - Requset class = {byts[key]}")
            logging.info("MAIN - Sending response status")
            conn.send(b"OK")

            match byts[key]:

                case classes.Request.Test:
                    if classes.Request.Test().data:
                        logging.info("MAIN - Receiving data..")
                        while True:
                            flag = False
                            read, write, error = select.select([conn], [conn], [], 0.5)
                            logging.info("MAIN - Waiting data..")
                            for i in read:
                                logging.info("MAIN - Reading data")
                                data = struct.unpack(classes.Request.Test().format, conn.recv(5000))
                                logging.info(f"MAIN - Data = {data}")
                                flag = True
                            if flag: break
                    rs = classes.Request.Test(time=time.time())
                    conn.send(struct.pack(rs.format, 85.4))




    except Exception as error:
        print(error)
        if error == KeyboardInterrupt:
            s.close()
            break
