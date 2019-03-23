class State:
    name = None
    is_final = False
    is_start = False

    def __init__(self, name):
        self.name = name
        self.is_final = False
        self.is_start = False

    def set_final(self):
        self.is_final = True

    def set_start(self):
        self.is_start = True

