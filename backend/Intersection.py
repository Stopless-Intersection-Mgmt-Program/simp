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

        self.spawn = spawn # average time (s) between car spawns per lane
        random.seed(0) # seed the spawner for testing consistency
        self.cooldown = [0, 0, 0, 0, 0, 0, 0, 0] # spawner cooldown (s) for each of the 8 lanes


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        vt, dt = self.turnSpeed(car), self.turnLength(car.path)

        # loop through other cars and set car to arrive after each
        car.setCourse(0, 0, vt)
        for other in self.cars: self.arriveAfter(car, other)

        # set car to accelerate to intersection speed once clear of intersection
        tf = car.atDistance(dt)[0]
        car.course.append((tf, (self.speed - vt) / car.acceleration + tf, car.acceleration))

        print("Set course:", car.path, car.course)
        self.cars.append(car)


    def arriveAfter(self, car1, car2):
        # sets car1 to arrive at the intersection after car2
        overlap, vt1, vt2 = self.overlap(car1.path, car2.path), self.turnSpeed(car1), self.turnSpeed(car2)
        (li1, lo1), (li2, lo2) = self.turnLanes(car1.path), self.turnLanes(car2.path)
        if overlap == None or car2.course[-1][1] < self.time: return # no overlap or car2 has already completed its course

        else: (d1, d2), ta = overlap, 0 # if there is a critical section
        if car2.distance < d2: # if car2 has not yet cleared the critical section
            ta = car2.atDistance(d2)[0] - d1 / vt1
            if ta > car1.atDistance(0)[0]: car1.setCourse(0, ta + self.buffer, vt1)

        if li1 == li2 and vt1 < vt2: # if car2 starts in the same lane and car1 is slower
            a1, a2 = car1.acceleration, car2.acceleration
            tm = car2.course[1][1] + (((a1 * vt2 ** 2 + a2 * vt1 ** 2) / (a1 + a2)) ** 0.5 - vt2) / a2
            tm, (dm, vm) = tm + d2 / vt2, car2.atTime(tm)
            if car1.atTime(tm)[0] > dm:
                car1.setCourse(dm, tm + self.buffer, vm)
                car1.course.append((tm + self.buffer, (vm - vt1) / a1 + tm, -a1))

        if lo1 == lo2 and vt1 > vt2: # if car2 ends in the same lane and car1 is faster
            vf, a1, a2 = self.speed, car1.acceleration, car2.acceleration
            ta = car2.course[-1][0] + (vt1 - vt2) / a2 - ((vf ** 2 - vt2 ** 2) / (2 * a2) - (vf ** 2 - vt1 ** 2) / (2 * a1)) / vf - d1 / vt1
            if ta > car1.atDistance(0)[0]: car1.setCourse(0, ta + self.buffer, vt1)


    def turnLanes(self, path):
        # returns start and end lane of the path
        di, do = path
        return di * 2 + ((do - di) % 4) // 2, do * 2 + ((do - di) % 4 == 1)


    def turnSpeed(self, car):
        # returns the speed (m/s) car can take turn based on radius
        di, do = car.path
        turn = (do - di) % 4
        if turn == 0: return 0.21 * self.size
        if turn == 1: return 0.625 * self.size
        if turn == 2: return self.speed
        if turn == 3: return 0.205 * self.size

    
    def turnLength(self, path):
        # returns the total distance (m) of the path through the intersection
        di, do = path
        turn = (do - di) % 4
        if turn == 0: return math.pi * (0.21 * self.size)
        if turn == 1: return 0.5 * math.pi * (0.625 * self.size)
        if turn == 2: return self.size
        if turn == 3: return 0.5 * math.pi * (0.205 * self.size)


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
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
        self.cooldown = [t - (period / 1000) if t > 0 else 0 for t in self.cooldown]
        for lane in range(8): # loop through each lane
            if self.cooldown[lane] != 0: continue # check if there is a cooldown still in effect
            if random.random() > (period / (self.spawn * 1000)): continue # adjust for spawn rate
            if lane % 2 == 1: # left lane
                if random.random() > 0.1: path = (lane // 2, (lane // 2 + 1) % 4) # 90% chance of left turn
                else: path = (lane // 2, lane // 2) # 10% chance of U turn
            else: # right lane
                if random.random() > 0.2: path = (lane // 2, (lane // 2 + 2) % 4) # 80% chance of straight
                else: path = (lane // 2, (lane // 2 + 3) % 4) # 20% chance of right turn
            self.schedule(Car.Car(0, -self.radius, self.speed, path))
            self.cooldown[lane] = 10 / self.speed + self.buffer # set cooldown for lane


    def tick(self, period):
        # updates properties based on period (ms)
        self.time += period / 1000
        for car in self.cars:
            car.tick(period) # tick each car
            if car.distance > self.radius: self.cars.remove(car) # remove cars that have cleared the intersection
        
        if self.spawn > 0: self.spawner(period) # run spawner if active


    def render(self):
        # returns list of car ids, coordinates, and directions
        return [(car.id) + car.render(self.size) + (car.speed) for car in self.cars]


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car