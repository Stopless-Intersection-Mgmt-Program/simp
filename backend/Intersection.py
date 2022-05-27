import math
import random
import Car

class Intersection:
    def __init__(self, buffer, spawn = 0):
        self.size = 40 # length (m) of one side of the intersection
        self.speed = 30 # speed (m/s) of cars entering and exiting the intersection
        self.radius = 301 # distance (m) at which cars get spawned and despawned
        self.buffer = buffer # gap (s) added between cars travelling through intersection

        self.time = 0 # clock to track time (s) elapsed
        self.cars = [] # list of cars monitored by the intersection
        self.last = [None] * 8 # last car in each lane

        self.spawn = spawn # average cars per second for spawner
        random.seed(0) # seed the spawner for testing consistency
        self.distribution = [0.1, 0.2] # probability of a U turn and right turn

        # if self.spawn != 0: self.speed = 60 / (self.spawn + 1) # adjust speed for traffic


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        vt, dt, lane = self.turnSpeed(car), self.turnLength(car.path), self.turnLanes(car.path)[0]

        # loop through other cars and set car to arrive after each
        ta = max(self.earliestArrival(car, other) for other in self.cars) if len(self.cars) > 0 else 0

        # if self.last[lane] != None:
        #     if self.last[lane].path != car.path or self.last[lane].course[-2][1] < self.time: df = 0
        #     else: df = self.last[lane].atTime(self.last[lane].course[-2][1])[0] - 10
        #     car.followTo(self.last[lane], df, ta - (0 - df) / vt, vt)
        # else: car.setCourse(0, ta, vt)
        
        car.followTo(self.last[lane], 0, ta, vt)

        # set car to accelerate to intersection speed once clear of intersection
        tf, vf = car.atDistance(dt)
        car.course.append([tf, (self.speed - vf) / car.acceleration + tf, car.acceleration])

        # print("Set course:", car.speed, car.path, car.course)
        self.cars.append(car)
        self.last[lane] = car

        # tf, vf = car.atDistance(0)
        # if tf < ta - 1.e-6 or abs(vt - vf) > 1.e-6:
        #     print(ta, tf, vt, vf)
        #     exit()


    def earliestArrival(self, car, other):
        # sets car to arrive at the intersection after other
        overlap, vt, vto = self.overlap(car.path, other.path), self.turnSpeed(car), self.turnSpeed(other)
        if overlap == None or other.course[-1][1] < self.time: return 0 # no overlap or other has already completed its course

        else: (d1, d2), ta = overlap, 0 # if there is a critical section
        if other.distance < d2: # if other has not yet cleared the critical section
            ta = other.atDistance(d2)[0] - d1 / vt

        if self.turnLanes(car.path)[1] == self.turnLanes(other.path)[1] and vt >= vto: # if other ends in the same lane and car is faster
            dt, vf, a = self.turnLength(car.path), self.speed, car.acceleration
            ta = other.course[-1][0] # base time is time other leaves intersection
            ta += (vt - vto) / a - (vt ** 2 - vto ** 2) / (2 * a * vf) - (dt - 10) / vt

        return ta + self.buffer


    def turnLanes(self, path):
        # returns start and end lane of the path
        di, do = path
        return di * 2 + ((do - di) % 4 < 2), do * 2 + ((do - di) % 4 == 1)


    def turnSpeed(self, car):
        # returns the speed (m/s) car can take turn based on radius
        di, do = car.path
        turn = (do - di) % 4
        if turn == 0: return min(self.speed, car.turning * (0.21 * self.size))
        if turn == 1: return min(self.speed, car.turning * (0.625 * self.size))
        if turn == 2: return self.speed
        if turn == 3: return min(self.speed, car.turning * (0.205 * self.size))

    
    def turnLength(self, path):
        # returns the total distance (m) of the path through the intersection
        di, do = path
        turn = (do - di) % 4
        if turn == 0: return math.pi * (0.21 * self.size)
        if turn == 1: return 0.5 * math.pi * (0.625 * self.size)
        if turn == 2: return self.size
        if turn == 3: return 0.5 * math.pi * (0.205 * self.size)


    def overlap(self, path1, path2):
        # returns start distance (m) on path1 and end distance (m) on path2 of critical section
        (di1, do1), (di2, do2) = path1, path2
        turn1, turn2 = (do1 - di1) % 4, (do2 - di2) % 4
        reld = (di2 - di1) % 4 # relative direction of other car

        if reld == 0: # path1 is path2
            if turn1 // 2 == turn2 // 2: return 0, 10 # if paths have same starting lane
            else: return None # if not in same lane, no critical section

        if reld == 1: # path2 is left of path1
            lcritical = [[None, None, (0, 0.5), (0.8, 1)], # U turn
                        [(0.6, 0.7), (0.5, 0.5), (0, 0.7), None], # left turn
                        [None, None, (0.1, 0.9), None], # straight
                        [None, None, (0.3, 1), None]] # right turn
            cs = lcritical[turn1][turn2]

        if reld == 2: # path2 is opposite of path1
            ocritical = [[None, None, (0.6, 1), None], # U turn
                        [None, None, (0.6, 0.5), None], # left turn
                        [(0.8, 1), (0.3, 1), None, None], # straight
                        [None, None, None, None]] # right turn
            cs = ocritical[turn1][turn2]

        if reld == 3: # path2 is right of path1
            rcritical = [[None, (0.3, 0.9), None, None], # U turn
                        [None, (0.2, 0.7), None, None], # left turn
                        [(0.2, 0.9), (0.5, 0.4), (0.6, 0.3), (0.8, 1)], # straight
                        [(0.3, 1), None, None, None]] # right turn
            cs = rcritical[turn1][turn2]
        if cs == None: return None

        # adjust for intersection size
        return cs[0] * self.turnLength(path1), cs[1] * self.turnLength(path2)


    def spawner(self, period):
        # based on the array of distributions for the 4 turns, randomly spawns cars and schedules them    
        for lane in range(8): # loop through each lane
            last, vs = self.last[lane], self.speed
            if last != None and last.distance < -self.radius + 10: continue # wait for last to clear spawn box
            if random.random() > (self.spawn / 8) * (period * 1.e-3): continue # adjust for spawn rate

            if lane % 2 == 1: # left lane
                if random.random() > self.distribution[0]: path = (lane // 2, (lane // 2 + 1) % 4) # 90% chance of left turn
                else: path = (lane // 2, lane // 2) # 10% chance of U turn
            else: # right lane
                if random.random() > self.distribution[1]: path = (lane // 2, (lane // 2 + 2) % 4) # 80% chance of straight
                else: path = (lane // 2, (lane // 2 + 3) % 4) # 20% chance of right turn

            if last != None: # calculate realistic spawn speed given previous car
                dc, vc, a = last.distance, last.speed, last.acceleration
                vs = (vc ** 2 + 2 * (dc + self.radius - (10 + 1.e-6)) * a) ** 0.5 # adjust so car can decelerate in time to keep a 10m gap
                if isinstance(vs, complex): vs = self.speed

            self.schedule(Car.Car(0, -self.radius, min(vs, self.speed), path)) # schedule car and set last spawn and cooldown for lane


    def tick(self, period):
        # updates properties based on period (ms)
        self.time += period * 1.e-3
        if self.spawn > 0: self.spawner(period) # run spawner if active

        for car in self.cars.copy():
            car.tick(period) # tick each car
            if car.distance - self.turnLength(car.path) > self.radius:
                self.cars.remove(car) # remove cars that have cleared the intersection


    def render(self):
        # returns list of car ids, coordinates, and directions
        return [[car.id] + list(car.render(self.size)) + [car.speed] for car in self.cars]


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        canvas.create_text(20, 20, text=round(self.time, 2), anchor="nw", fill="white")
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car