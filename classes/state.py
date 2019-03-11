class State:
    name = None
    is_final = False
    is_start = False

    def __init__(self, name):
        self.name = name

    def set_final(self):
        self.is_final = True

    def set_start(self):
        self.is_start = True

