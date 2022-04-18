class TrafficLight:
    def __init__(self, size):
        self.time = 0 # clock to track behavior (ms)
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds new car for intersection to schedule
        self.cars.append(car)
        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time
        for car in self.cars: car.tick(period)
        self.time = (self.time + period) % (2 ** 63 - 1)