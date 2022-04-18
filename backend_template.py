class Car:
    # all values are in SI units (meters, meters per second, etc.)
    def __init__(self, id, distance, path, speed):
        self.id = id
        self.distance = distance # distance relative to the enterance of the intersection (negative means approaching intersection)
        self.path = path # tuple containing starting lane and ending lane
        self.speed = speed
        self.acceleration = 0 # positive means accelerating, negative means braking

    def accelerate(self, distance, time):
        # sets acceleration so that car reaches distance in time (ms)
        self.acceleration = ((distance - self.distance) - self.speed * (time * 1000)) * 2 / (time ** 2)

    def time(self, distance):
        # returns time (ms) until car reaches distance based on acceleration
        if self.acceleration == 0: return (distance - self.distance) / self.speed
        return (-self.speed + (self.speed ** 2 + 2 * self.acceleration * (distance - self.distance)) ** 0.5) / self.acceleration

    def tick(self, period):
        # increments time-varying values adjusted for period length (ms)
        self.speed += self.acceleration * (period / 1000)
        self.distance += self.speed * (period / 1000)

    def render(self):
        # returns coordinates and direction based on path and distance
        return # to be implemented



class Intersection:
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.time = 0 # clock to track behavior (ms)
        self.cars = [] # list of cars monitored by the intersection

    def schedule(self, car):
        # adds new car for intersection to schedule
        self.cars.append(car)
        # based on scheduling algorithm, should assign a car to follow
        return # to be implemented

    def follow(self, car1, car2):
        # sets car1 to pass through intersection immediately after car2
        # if car1 and car2 do not share a critical section, do nothing
        overlap = self.overlap(car1.path, car2.path)
        if overlap == None: return
        car1.accelerate(overlap[0], car2.time(overlap[1]))
        return # to be implemented

    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        # if there is no critical section, returns None
        # can be implemented as a table for each intersection layout
        return # to be implemented

    def tick(self, period):
        # ticks each car and increments the time
        for car in self.cars: car.tick(period)
        self.time = (self.time + period) % (2 ** 63 - 1)
