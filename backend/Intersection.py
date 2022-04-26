import math

class Intersection:
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size # length (m) of one side of the intersection
        self.time = 0 # clock to track time (ms) elapsed
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds new car for intersection to schedule
        # based on scheduling algorithm, should assign a car to follow

        # TEMPORARY CODE FOR TESTING
        if len(self.cars) > 0: self.follow(car, self.cars[-1]) # FIFO
        self.cars.append(car)

        return # to be implemented


    def follow(self, car1, car2):
        # sets car1 to pass through intersection immediately after car2
        # if car1 and car2 do not share a critical section, do nothing

        # TEMPORARY CODE FOR TESTING
        overlap = self.overlap(car1.path, car2.path)
        if overlap == None: return
        stats = car2.stats(overlap[1])
        car1.course(overlap[0], stats[0], stats[1])

        return # to be implemented


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        # if there is no critical section, returns None
        # can be implemented as a table for each intersection layout

        # TEMPORARY CODE FOR TESTING
        arc = 2 * math.pi * (0.625 * self.size)
        if path1 == path2: return 0, 8
        if path1 == (7, 1) and path2 == (1, 3): return arc / 8, arc / 8
        if path1 == (1, 3) and path2 == (7, 1): return arc / 16, arc / 6
        if path1 == (5, 7) and path2 == (7, 1): return arc / 8, arc / 8

        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time
        self.time = (self.time + period) % (2 ** 63 - 1)
        for car in self.cars: car.tick(self.time / 1000)


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render cars