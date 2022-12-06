import pickle
import os
import classes

classe = [classes.Request.HandShake, classes.Request.Test]
output={}
for i in classe:
    key = b"\x04"+os.urandom(4)+b"\x04"
    output.update({key:i})
with open("ClassBytes", "wb") as f:
    pickle.dump(output, f)
