
class StatusCodes:
    GOOD=1
    BAD=2
    UNCORECT_PASWORD=3
class HandShake:
    class Request:
        def __init__(self, password):
            self.password = password

    class Response:
        def __init__(self, status):
            self.status=status

class ServersInfo:
    class Request:
        def __init__(self, password):
            self.password = password
    class Response:
        def __init__(self, status, info):
            self.status=status
            self.info =info

class GetLog:
    class Request:
        def __init__(self, password, id):
            self.password = password
            self.id=id
    class Response:
        def __init__(self, status, log):
            self.status=status
            self.log = log

class ServerController:
    class Request:
        def __init__(self, password, id, action):
            self.password = password
            self.id=id
            self.action=action

    class Response:
        def __init__(self, status):
            self.status=status


class ServerCommand:
    class Request:
        def __init__(self, password, id, command):
            self.password = password
            self.id=id
            self.command=command

    class Response:
        def __init__(self, status):
            self.status=status