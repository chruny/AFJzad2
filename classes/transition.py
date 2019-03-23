class Transition:
    name = None
    start = None
    end = None
    is_epsilon = False

    def __init__(self, name):
        self.name = name
        self.start = None
        self.end = None
        self.is_epsilon = False


    def set_start(self, start):
        self.start = start



    def set_end(self, end):
        self.end = end
