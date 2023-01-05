import os
import pickle

import classes

classe = [classes.HandShake, classes.Test, classes.Command, classes.StartServer, classes.StopServer, classes.GetLog, classes.GetServers]
output = {}
for i in classe:
    key = b"\x04" + os.urandom(4) + b"\x04"
    output.update({key: i})
with open("ClassBytes", "wb") as f:
    pickle.dump(output, f)
