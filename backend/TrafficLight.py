import Intersection

# Fix:
# - U turns and right turns

class TrafficLight(Intersection.Intersection):
    def __init__(self, buffer, spawn = 0):
        self.lanes = [[], [], [], [], [], [], [], []] # list of cars waiting in each lane
        self.lights = [0] * 8 # green light cooldowns (s) for each lane
        self.tail = [(None, 0)] * 8 # list of last car to be scheduled in each lane and acceleration distance
        self.current = 0 # lane that is being waited on for next green

        super().__init__(buffer, spawn)
        self.distribution = [0, 0] # no ability to handle U turns and right turns


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        self.cars.append(car)

        lane = self.turnLanes(car.path)[0]
        car.followTo(self.last[lane], -10 * (1 + len(self.lanes[lane])), self.lights[lane] + self.time + 5, 1.e-8) # stop car
        self.lanes[lane].append(car)
        self.last[self.turnLanes(car.path)[0]] = car


    def signal(self, order):
        # determines which lanes should have a green light based on order of lights
        if self.lights[self.current] > 0: # waiting on cars to pass through
            if (self.current // 2) % 2 == (order[self.current] // 2) % 2: # check if next lane is on same road
                self.green(order[self.current])
        
        else: # set increment current and set next light to green
            self.current = order[self.current]
            self.green(self.current)
            self.tail[self.current] = (None, 0)



    def green(self, lane):
        # sets cars in lane to go and sets the cooldown for when the last car clears the intersection
        wait, (last, df) = self.lights[lane], self.tail[lane]
        for i in range(len(self.lanes[lane])): # loop through all cars in lane
            car = self.lanes[lane].pop(0)
            dt, vt = self.turnLength(car.path), self.turnSpeed(car)
            dc, vc, a = car.distance, car.speed, car.acceleration

            if last == None: df, tf = dc + abs(vt ** 2 - vc ** 2) / (2 * a) + 1.e-3, 0 # calculate distance and time to turn speed
            else: df, tf = df - 10, 0 if last.distance > df else last.atDistance(df)[0] # schedule to previous distance to avoid collision
            car.followTo(last, df, tf + self.buffer, vt)

            if car.atDistance(0)[1] > vt: car.followTo(last, 0, tf - df / vt, vt) # ensure turn speed is not exceded

            # set car to accelerate to intersection speed once clear of intersection
            tf = max(car.course[-1][1], car.atDistance(dt)[0])
            car.course.append((tf, (self.speed - vt) / car.acceleration + tf, car.acceleration))

            print("Set course:", car.path, car.course)
            wait, last = car.atDistance(self.turnLength(car.path))[0] - self.time, car
        self.lights[lane], self.tail[lane] = wait, (last, df)
        

    def tick(self, period):
        # updates properties based on period (ms)
        self.lights = [t - (period / 1000) if t > 0 else 0 for t in self.lights]
        self.signal([4, 0, 3, 1, 5, 7, 2, 6]) # left/straight, straight/straight, straight/left
        super().tick(period)


    def render(self):
        # returns list of car ids, coordinates, and directions
        render = super().render()
        return render + ["new stuff"]