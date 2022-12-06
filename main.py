import pickle
import struct
import classes
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect("localhost", 99998)

def send(_class):
    with open("ClassBytes", "rb") as f:
        byts: dict = pickle.load(f)
        print(byts)
    for i in byts:
        if byts[i] == _class.__class__:
            s.sendall()
            break

        #     # sdt = struct.pack(_class.format, _class.values())

send(classes.Request.HandShake())