class Orientable:

    def __init__(self, orientation, cost):
        self.orientation = orientation
        self.cost = cost
        self.reload = None

    def stop(self):
        self.reload = None
