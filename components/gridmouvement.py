class GridMovement:

    def __init__(self, cost):
        self.cost = cost
        self.sx = None
        self.sy = None
        self.cx = None
        self.cy = None
        self.speed = 1
        self.reload = None
        self.reload_drawing = None

    def stop(self):
        self.sx = self.sy = self.cx = self.cy = None
        self.reload = None
