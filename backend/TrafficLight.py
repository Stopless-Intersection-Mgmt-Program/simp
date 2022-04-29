import math

class TrafficLight:
    def __init__(self, size):
        self.size = size # length (m) of one side of the intersection
        self.time = 0 # clock to track time (ms) elapsed
        self.cars = [] # list of cars monitored by the intersection
        self.lanes = [[], [], [], [], [], [], [], []] # list of cars waiting in each lane
        
        self.lights = [0, 0, 0, 0, 0, 0, 0, 0] # list of times (s) until lanes are no longer green
        self.current = 1 # lane that is being waited on for next green


    def control(self, order):
        # determines which lanes should have a green light based on order of lights
        if self.lights[self.current] > self.time: # waiting on cars to pass through
            if (self.current // 2) % 2 == (order[self.current] // 2) % 2: # check if next lane is on same road
                self.lights[order[self.current]] = self.green(order[self.current])
        
        else: # set increment current and set next light to green
            self.current = order[self.current]
            self.lights[self.current] = self.green(self.current)


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        self.cars.append(car)

        li, lo = car.path
        if (lo - li) % 8 // 2 < 2: lane = li # left turn lane
        else: lane = li - 1
        self.stop(car, -4 - 8 * (len(self.lanes[lane]))) # stop car
        self.lanes[lane].append(car)


    def green(self, lane):
        # sets cars in lane to go and returns the time (s) when the last car clears the intersection
        t = 0
        for i in range(len(self.lanes[lane])):
            car = self.lanes[lane].pop(0)
            self.go(car, 40, i * 0.2) # CAN RESULT IN COLLISION... NEEDS FIXING
            t = car.timeTo(60) # a distance of 50 will clear any other cars
        return t # will be 0 if no cars in lane


    def stop(self, car, distance):
        # sets course so car stops at distance (m)
        dc, df, tc, v = car.distance, distance, car.time, car.speed
        a, tf = v ** 2 / (-2 * (df - dc)), 2 * (df - dc) / v + tc
        car.course = (tc, tf, tf, a)

    
    def go(self, car, speed, delay):
        # sets course so car accelerates to speed (m/s) after delay (s)
        tc, d, vc, vf, a = car.time, delay, car.speed, speed, car.acceleration
        tf = (vf - vc) / a + tc + d
        car.course = (tc + d, tf, tf, a)


    def tick(self, period):
        # ticks each car and increments the time for period (ms)
        self.control([4, 0, 3, 1, 5, 7, 2, 6]) # left/straight, straight/straight, straight/left
        self.time = self.time + period / 1000

        for car in self.cars: car.tick(self.time) # tick each car


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car