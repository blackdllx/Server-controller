
class Request:
    class HandShake:
        def __init__(self):
            self.format=None
            self.values=[]

    class Test:
        def __init__(self, time=None):
            self.format=None
            if time: self.format="l"
            self.values=[time]


class Response:
    class got:
        pass

    class HandShake:
        def __init__(self):
            pass
