class HandShake:
    def __init__(self):
        self.format = None
        self.values = []
        self.response = False


class StartServer:
    def __init__(self, id):
        self.format = "i"
        self.values = [id]
        self.data = True
        self.response = False

class GetLog:
    def __init__(self, id, log):
        self.format = b"i3349b$"
        self.values=[id, log]
        self.response = True
class StopServer:
    def __init__(self, id):
        self.format = "i"
        self.values = [id]
        self.data = True
        self.response = False
class Command:
    def __init__(self, command, id):
        self.format = b"b$i"
        self.values = [command, id]
        self.data = True
        self.response = False


class Test:
    def __init__(self, time=0):
        self.format = "f"
        self.values = [time]
        self.data = True
        self.response = True

