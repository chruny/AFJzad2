class Transition:
    name = None
    start = None
    end = None
    is_epsilon = False

    def __init__(self, name):
        self.name = name

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end
