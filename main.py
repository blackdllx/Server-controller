import mctools
import requests
import subprocess
import random2
import re
import os
import threading
import time


from utils import *


class Server:
    def __init__(self, name: str, _id=None, core: str = "vanilla", version: str = "1.19.2", pirate: bool = False) -> None:
        self.name = name
        self.id = _id
        self.config = {
            "memory": "1024M"
        }
        self.log=b""
        self.errors=[]
        self.active=False
        self.running=False
        self.pipe=None
        self.properties={}
        self.password=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(N))

        self.CreateServer()
        self.DownloadServer(core, version)
        self.InnitServer()
        self.PropertiesParce()


    def CreateServer(self) -> None:

        if not os.path.isdir("Servers1"):
            os.makedirs("Servers1")

        if self.id == None:
            temp = call("ls Servers1/").stdout.read()

            if temp == b"":
                self.id = 0
            else:
                self.id = int(max(temp.decode().split("\n"))) + 1

            del temp
        
        if not os.path.isdir(f"Servers1/{self.id}"):
            os.makedirs(f"Servers1/{self.id}")
    
    def DownloadServer(self, core, version) -> None:
        if os.path.isfile(f"Servers1/{self.id}/Server.jar"):return
        match core:
            case "vanilla":
                temp = requests.get(f"https://mcversions.net/download/{version}").content.decode()
                temp = re.search(r'"([^"]*server\.jar[^"]*)"', temp)
                if not temp:
                    print("Incorrect version")
                    return
                
                temp = temp.group(1)
                download_file(temp, f"Servers1/{self.id}/Server.jar")

                del temp
            
            case "fabric":
                download_file(f"https://meta.fabricmc.net/v2/versions/loader/1.18.2/0.14.19/0.11.2/server/jar", f"Servers1/{self.id}/Server.jar")

    def InnitServer(self):
        with open(f"./Servers1/{self.id}/eula.txt", "w") as f:f.write("eula=true")
        self.process = subprocess.Popen(f"java -jar -Xmx{self.config['memory']} -Xms{self.config['memory']} Server.jar -nogui", shell=True, 
                                        cwd=f"./Servers1/{self.id}/", stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.active = True
        print("Start logging")
        threading.Thread(target=self.EventsHandler).start()
        threading.Thread(target=self.Logging).start()
        
        
    def Logging(self):
        print("Logging started")
        while self.active:
            temp = self.process.stdout.readline()
            if temp != b"":
                self.log = self.log + temp
                print(temp.decode(), end="")
            time.sleep(0.2)

    def EventsHandler(self):
        print("Handle events")
        def ErrorHandler(self):
            for i in self.log.decode().split("\n"):
                if re.search(r'.*\/ERROR\]', i):
                    if not i in self.errors:
                        print("Error found")
                        self.errors.append(i)
                        print(self.errors)

        while self.active:
            time.sleep(0.2)
            if re.search(r"\[Server thread\/INFO\]: Done", self.log.decode()) and not self.running:
                print('Done found')
                self.running = True

            ErrorHandler(self)
    
    def PropertiesParce(self):
        with open(f"Servers1/{self.id}/server.properties", "rb") as f:
            for i in f.read().decode().split("\n"):
                if i[0] != "#":
                    self.properties.update({i.split("=")[0]:i.split("=")[1]})

    def PropertiesSave(self):
        with open(f"Servers1/{self.id}/server.properties", "wb") as f:
            for i in self.properties:
                f.write(f"{i}={self.properties[i]}")

    def CreatePipe(self):
        flag=False
        if self.properties["enable-rcon"] == "false":
            self.properties["enable-rcon"]="true"
            flag=True

        if self.properties["rcon.password"] == "":
            self.properties["rcon.password"] = self.password
        else:
            self.password=self.properties["rcon.password"]
        
        if flag:
            self.process.stdin.write(b"stop") # Add stop event to event Handler
            self.process.stdin.flush()
            self.active=False
            self.running=False
            self.PropertiesSave()
            self.InnitServer()
            while not self.running:
                time.sleep(0.1)
            

        self.pipe = mctools.RCONClient(f"localhost", self.properties["server-port"])
        self.pipe.login(self.password)
        
        if not self.pipe.is_authenticated():
            raise LookupError


            


class Cord:
    def __init__(self) -> None:
        pass

s=Server("Standart name", version="1.18.2", _id=0)
