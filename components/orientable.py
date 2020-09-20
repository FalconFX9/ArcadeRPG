class Orientable:

    def __init__(self, orientation, price):
        self.orientation = orientation
        self.price = price
        self.reload = None

    def stop(self):
        self.reload = None
