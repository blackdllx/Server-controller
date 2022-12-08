class HandShake:
    def __init__(self, password):
        self.format = b"b$"
        self.values = [password]
        self.response = True


class StartServer:
    def __init__(self, id, password):
        self.format = b"ib$"
        self.values = [id, password]
        self.data = True
        self.response = False

class GetLog:
    def __init__(self, id, log, password):
        self.format = b"ib$b$"
        self.values=[id, log, password]
        self.response = True
class StopServer:
    def __init__(self, id, password):
        self.format = b"ib$"
        self.values = [id, password]
        self.data = True
        self.response = False
class Command:
    def __init__(self, command, id, password):
        self.format = b"b$ib$"
        self.values = [command, id, password]
        self.data = True
        self.response = False


class Test:
    def __init__(self, time=0):
        self.format = "f"
        self.values = [time]
        self.data = True
        self.response = True

