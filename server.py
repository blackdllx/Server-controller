import json
import logging
import os
import subprocess
import threading
import time
import requests


class interface:
    def __init__(self, name) -> None:
        self.name = name
    
    def run(self):
        with open(f"interfaces/{self.name}/interface.py", "rb") as f:
            exec(f.read())
        exec()

    def __str__(self) -> str:
        return(self.name)

with open("config.json", "rb") as f:
    CFG = json.load(f)
with open("interfaces/interfaces.reg", "rb") as f:
    temp = f.read().decode()
    if temp:
        o=[]
        for i in temp.split("\n"):o.append(interface(i))
        
        print("Interfaces to load: ", end="")
        for i in o: print(str(i)+" ", end="")
        print("")

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
Servers = []
S=None
BASEPATH = os.getcwd()





class Server:
    active = False

    def __init__(self, id):
        print("New server innit")
        self.actions={"start": self.start, "stop": self.stop}
        self.console = None
        self.id = id
        self.dir = f"/Servers/{id}/"
        self.pa = ""
        self.consoleLog = []
        self.properties = {}
        print(os.path.isfile(BASEPATH+self.dir+"/new.chek"))
        if os.path.isfile(BASEPATH+self.dir+"/new.chek"):
            print("init core")
            self.download()
        self.loadProperties()

    def download(self):
        self.start()
        self.stop()
        os.remove(BASEPATH+self.dir+"/new.chek")
        print("end")
    def loadProperties(self):
        if not self.pa == os.getcwd():
            os.chdir(BASEPATH+self.dir)
            self.pa = os.getcwd()
        try:
            with open("./server.properties", "rb") as f:
                data = f.read().decode()
                for i in data.split("\n"):
                    if i != "" and not i[0] == "#":
                        self.properties.update({i.split('=')[0]: i.split("=")[1]})
        except FileNotFoundError:
            time.sleep(5)
            self.loadProperties()

    def GetStats(self):
        pass
    def saveProperties(self):
        if not self.pa == os.getcwd():
            os.chdir(BASEPATH+self.dir)
            self.pa = os.getcwd()
        if self.properties != {}:
            out = ''
            for i in self.properties:
                out = out + f"{i}={self.properties[i]}\n"
            print(out)
            with open("./server.properties", "wb") as f:
                f.write(out.encode())

    def start(self):
        print("starting")
        if not self.pa == os.getcwd():
            os.chdir(BASEPATH+self.dir)
            self.pa = os.getcwd()
        if not self.active:
            self.console = subprocess.Popen(f". ./start.sh", shell=True, stdout=subprocess.PIPE,
                                            stdin=subprocess.PIPE)
            self.active = True
            threading.Thread(target=self.parse).start()
            print("started")

    def stop(self):
        if self.active:
            self.console.stdin.write(b"stop\n")
            self.console.stdin.flush()
            self.active = False

    def parse(self):
        while self.active:
            if not self.console.poll():
                f = self.console.stdout.readline()
                if f != b"":
                    print(f.decode(), end="")
                    self.consoleLog.append(f)

    def send(self, command: str):
        if self.active:
            self.console.stdin.write((command).encode() + b"\n")
            self.console.stdin.flush()

    def exportInfo(self):
        return {"id": self.id, "settings": self.properties}

# def HandShake(request):
#     logging.log(logging.DEBUG, "HandShake response")
#     logging.log(logging.DEBUG, f"Config password: {CFG['password']}, request password: {request.password}")
#     try:
#         if request.password == CFG["password"]:
#             logging.info("Currect password")
#             return classes.HandShake.Response(status=classes.StatusCodes.GOOD)
#         logging.info("Uncurrect password")
#         return classes.HandShake.Response(status=classes.StatusCodes.UNCORECT_PASWORD)
#     except:
#         logging.info("Error")
#         return classes.HandShake.Response(status=classes.StatusCodes.BAD)


def download_file(past ,url):
    local_filename = past
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                if chunk:
                    f.write(chunk)

def ServerInit():
    print("server init")
    if os.path.isdir("Servers"):
        for i in range(CFG["ServerCount"]):
            if os.path.isdir("Servers/" + str(i)):
                pass
            else:
                print("creating server")
                os.mkdir("Servers/" + str(i))
                with open(f"Servers/{i}/start.sh", "w") as f:
                    f.write(f"java -Xmx1024M -Xms1024M -jar server.jar nogui")
                print("Downloading core")
                download_file(f"Servers/{i}/server.jar", "https://meta.fabricmc.net/v2/versions/loader/1.19.3/0.14.13/0.11.1/server/jar")
                print("core downloaded")
                # core = requests.get("https://meta.fabricmc.net/v2/versions/loader/1.19.3/0.14.13/0.11.1/server/jar").content
                # with open(f"Servers/{i}/server.jar", "wb") as f:
                #     f.write(core)
                with open(f"Servers/{i}/eula.txt", "w") as f:
                    f.write("eula=true")
                print("eula created")
                open(f"Servers/{i}/new.chek", "w").close()
                print("Mark created")
                os.mkdir(f"Servers/{i}/mods")
                print("Download Server Plugin")
                download_file(f"Servers/{i}/mods/spark.jar", 'https://mediafilez.forgecdn.net/files/4159/882/spark-1.10.17-fabric.jar')
                print("Download fabric API")
                download_file(f"Servers/{i}/mods/API.jar", 'https://mediafilez.forgecdn.net/files/4373/752/fabric-api-0.73.2%2B1.19.3.jar')
    else:
        os.mkdir("Servers")
        ServerInit()
    for i in range(CFG["ServerCount"]):
        Servers.append(Server(i))


if __name__ == '__main__':
    # ServerInit()
    for i in o:i.run()
