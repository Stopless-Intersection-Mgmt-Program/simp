import Intersection

# Fix:
# - U turns and right turns
# - cars scheduled during simulatenous don't slow down

class TrafficLight(Intersection.Intersection):
    def __init__(self, buffer, spawn = 0):
        self.lanes = [[], [], [], [], [], [], [], []] # list of cars waiting in each lane
        self.lights = [0, 0, 0, 0, 0, 0, 0, 0] # green light cooldowns (s) for each lane
        self.current = 0 # lane that is being waited on for next green

        super().__init__(buffer, spawn)
        self.distribution = [0, 0]


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        self.cars.append(car)

        li, lo = car.path
        if (lo - li) % 4 < 2: lane = li * 2 + 1 # left turn lane
        else: lane = li * 2
        car.setCourse(-8 * (1 + len(self.lanes[lane])), 0, 1.e-8) # stop car
        self.lanes[lane].append(car)


    def signal(self, order):
        # determines which lanes should have a green light based on order of lights
        if self.lights[self.current] > 0: # waiting on cars to pass through
            if (self.current // 2) % 2 == (order[self.current] // 2) % 2: # check if next lane is on same road
                self.lights[order[self.current]] = self.green(order[self.current])
        
        else: # set increment current and set next light to green
            self.current = order[self.current]
            self.lights[self.current] = self.green(self.current)  


    def green(self, lane):
        # sets cars in lane to go and returns the time (s) when the last car clears the intersection
        wait, prev = self.lights[lane], None
        for i in range(len(self.lanes[lane])): # loop through all cars in lane
            car = self.lanes[lane].pop(0)
            dt, vt = self.turnLength(car.path), self.turnSpeed(car)
            dc, vc, a = car.distance, car.speed, car.acceleration

            if i == 0: df, tf = max(0, dc + abs(vt ** 2 - vc ** 2) / (2 * a) + 1.e-3), 0 # calculate distance and time to turn speed
            else: df, tf = max(0, df - 8), prev.atDistance(df)[0] + 10 / vt # schedule to previous distance to avoid collision
            car.setCourse(df, tf + self.buffer, vt)

            if car.atDistance(0)[1] > vt: car.setCourse(0, tf - df / vt, vt) # ensure turn speed is not exceded

            # set car to accelerate to intersection speed once clear of intersection
            tf = max(car.course[-1][1], car.atDistance(dt)[0])
            car.course.append((tf, (self.speed - vt) / car.acceleration + tf, car.acceleration))

            print("Set course:", car.path, car.course)
            wait, prev = car.atDistance(self.turnLength(car.path))[0] - self.time, car
        return wait
        

    def tick(self, period):
        # updates properties based on period (ms)
        self.lights = [t - (period / 1000) if t > 0 else 0 for t in self.lights]
        self.signal([4, 0, 3, 1, 5, 7, 2, 6]) # left/straight, straight/straight, straight/left
        super().tick(period)