import math

# THINGS TO FIX:
# - green method needs a way to verify that car does not exceed turn speed

class TrafficLight:
    def __init__(self):
        self.size = 40 # length (m) of one side of the intersection
        self.time = 0 # clock to track time (ms) elapsed
        self.cars = [] # list of cars monitored by the intersection
        self.lanes = [[], [], [], [], [], [], [], []] # list of cars waiting in each lane
        
        self.lights = [0, 0, 0, 0, 0, 0, 0, 0] # list of times (s) until lanes are no longer green
        self.current = 1 # lane that is being waited on for next green


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        self.cars.append(car)

        li, lo = car.path
        if (lo - li) % 4 < 2: lane = li * 2 + 1 # left turn lane
        else: lane = li * 2
        car.stop(-4 - 8 * len(self.lanes[lane])) # stop car
        self.lanes[lane].append(car)


    def signal(self, order):
        # determines which lanes should have a green light based on order of lights
        if self.lights[self.current] > self.time: # waiting on cars to pass through
            if (self.current // 2) % 2 == (order[self.current] // 2) % 2: # check if next lane is on same road
                self.lights[order[self.current]] = self.green(order[self.current])
        
        else: # set increment current and set next light to green
            self.current = order[self.current]
            self.lights[self.current] = self.green(self.current)


    def green(self, lane):
        # sets cars in lane to go and returns the time (s) when the last car clears the intersection
        if len(self.lanes[lane]) == 0: return 0 # no wait time if no cars in lane
        for i in range(len(self.lanes[lane])):
            car = self.lanes[lane].pop(0)
            t = (40 - car.speed) / car.acceleration + self.time # time car will reach final speed
            delay = 0 if i == 0 else max(i * 0.5, tp - t) # set delay to avoid hitting previous car
            car.go(40, delay)
            tp = t + delay
        return car.timeTo(60) # a distance of 60 will clear any other cars


    def tick(self, period):
        # ticks each car and increments the time for period (ms)
        self.signal([4, 0, 3, 1, 5, 7, 2, 6]) # left/straight, straight/straight, straight/left
        self.time = self.time + period / 1000

        for car in self.cars: car.tick(self.time) # tick each car


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car