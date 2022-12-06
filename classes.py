
class Request:
    class HandShake:
        def __init__(self):
            self.format=None
            self.values=[]

    class Test:
        def __init__(self, time=0):
            self.format="f"
            self.values=[time]


class Response:
    class got:
        pass

    class HandShake:
        def __init__(self):
            pass
