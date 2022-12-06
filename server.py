import socket
import pickle
import struct
import time

import classes
import logging
import select

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)
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
            if byts[key].format:
                logging.info("MAIN - Receiving data..")
                while True:
                    read, write, error = select.select([conn], [conn], [], 0.5)
                    logging.info("MAIN - Waiting data..")
                    for i in read:
                        logging.info("MAIN - Reading data")
                        data = struct.unpack(byts[key].format, conn.recv(5000))
                        logging.info(f"MAIN - Data = {data}")

            match byts[key]:

                case classes.Request.Test:
                    while True:
                        read, write, error = select.select([], [conn], [], 0.5)
                        for i in write:
                            rs = classes.Request.Test(time.time())
                            conn.send(struct.pack(rs.format, *rs.values))

                case _:
                    pass




        # s.listen(2)
        # conn, addr = s.accept()
        # print(conn, addr)
        # while True:
        #     data=None
        #     try: data = s.recv(2048)
        #     except:pass
        #     with open("ClassBytes", "rb") as f:
        #         byts: dict = pickle.load(f)
        #         print(byts)
        #     if not data:
        #         continue
        #     match byts[data]:
        #         case classes.Request.HandShake:
        #             print("Handshake")
        #             s.sendall(b"OK")

    except Exception as error:

        print(error)
        if error == KeyboardInterrupt:
            s.close()
            break

