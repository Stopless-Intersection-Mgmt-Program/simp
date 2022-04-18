class Car:
    # all values are in SI units (meters, meters per second, etc.)
    def __init__(self, id, distance, path, speed):
        self.id = id

        # distance relative to the starting edge of the intersection
        self.distance = distance
        
        # tuple containing starting lane and ending lane
        self.path = path

        self.speed = speed

        # list of target speeds scheduled relative to distance
        self.maneuvers = []

    def maneuver(self, speed, distance):
        # adds a new maneuver
        self.maneuvers.append((distance, speed))
        self.maneuvers.sort(reverse=True)

    def acceleration(self):
        # based on maneuvers, calculates acceleration at current distance
        while self.maneuvers[0][0] >= self.distance: self.maneuvers.pop(0)
        distance, speed = self.maneuvers[0]
        return (self.speed ** 2 - speed ** 2) / (2 * (self.distance - distance))

    def overlap(self, path):
        # calculates distance at which car will cross path
        # returns none if there is no overlap, and 0 if paths are the same
        turn = (self.path[1] - self.path[0]) % 8 // 2
        if turn == 0: pass # U turn
        if turn == 1: pass # left turn
        if turn == 2: pass # straight
        if turn == 3: pass # right turn
        return # to be implemented

    def follow(self, car):
        # sets acceleration to pull up behind car, then matches speed each tick
        return # to be implemented

    def tick(self, period):
        # increments time-varying values adjusted for period length in ms
        self.speed += self.acceleration() * (period / 1000)
        self.distance -= self.speed * (period / 1000)



class Intersection:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.time = 0

        # list of periods in ms when each quadrant is unavailable
        self.quadrants = [[], [], [], []]

        # list of cars monitored by the intersection
        self.cars = []

    def path(self, car):
        # calculates time to enter each quadrant and time to exit each quadrant
        return # to be implemented

    def schedule(self, car):
        # allocates time period for car to pass through each quadrant
        # self.cars.sort(key=lambda car: car.distance, reverse=True)
        return # to be implemented

    def monitor(self, car):
        # add new car for intersection to monitor
        self.cars.append(car)

        # for stop sign, bring to a stop at intersection
        if self.algorithm == "STOP":
            car.accelerate(0, car.distance)
        # this assumes no cars in front to avoid collision
        # this can be improved using a maneuver node

    def tick(self, period):
        # determine if any cars need to be accelerated

        # for stop sign, check stopped cars and see if there is room to enter intersection
        for car in self.cars:
            if car.speed == 0:

                car.acceleration = 3

        # increment the time
        self.time = (self.time + period) % (2 ** 63 - 1)


