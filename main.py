import requests
import subprocess
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
        self.active=False
        
        self.CreateServer()
        self.DownloadServer(core, version)
        self.InnitServer()


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
        threading.Thread(target=self.Logging).run()
        
    def Logging(self):
        print("Logging started")
        while self.active:
            temp = self.process.stdout.read()
            self.log = self.log + temp
            time.sleep(0.2)
            print(self.log)
            
                    


class Cord:
    def __init__(self) -> None:
        pass

Server("Standart name", version="1.18.2", _id=0)
