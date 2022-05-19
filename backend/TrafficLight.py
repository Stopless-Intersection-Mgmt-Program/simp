import math
import Intersection

class TrafficLight(Intersection.Intersection):
    def __init__(self, buffer, spawn = 0):
        self.lanes = [[], [], [], [], [], [], [], []] # list of cars waiting in each lane
        self.lights = [0, 0, 0, 0, 0, 0, 0, 0] # green light cooldowns (s) for each lane
        self.current = 0 # lane that is being waited on for next green

        super().__init__(buffer, spawn)


    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        self.cars.append(car)

        li, lo = car.path
        if (lo - li) % 4 < 2: lane = li * 2 + 1 # left turn lane
        else: lane = li * 2
        car.setCourse(-4 - 8 * len(self.lanes[lane]), 0, 1.e-8)
        # self.stop(car, -8 * (1 + len(self.lanes[lane]))) # stop car
        self.lanes[lane].append(car)


    def signal(self, order):
        # determines which lanes should have a green light based on order of lights
        if self.lights[self.current] > 0: # waiting on cars to pass through
            if (self.current // 2) % 2 == (order[self.current] // 2) % 2: # check if next lane is on same road
                self.lights[order[self.current]] = max(self.green(order[self.current]), self.lights[order[self.current]])
        
        else: # set increment current and set next light to green
            self.current = order[self.current]
            self.lights[self.current] = max(self.green(self.current), self.lights[self.current])     


    def green(self, lane):
        # sets cars in lane to go and returns the time (s) when the last car clears the intersection
        wait, prev = 0, None
        for i in range(len(self.lanes[lane])):
            car = self.lanes[lane].pop(0)
            dt, vt = self.turnLength(car.path), self.turnSpeed(car)
            dc, vc, a = car.distance, car.speed, car.acceleration
            
            if i == 0: df, tf = max(0, dc + abs(vt ** 2 - vc ** 2) / (2 * a) + 1.e-3), 0 # calculate distance and time to turn speed
            else: df, tf = max(0, df - 8), prev.atDistance(df)[0] + 0.5 # schedule to previous distance to avoid collision
            car.setCourse(df, tf + self.buffer, vt)

            tf = max(car.course[-1][1], car.atDistance(dt)[0])
            car.course.append((tf, (self.speed - vt) / car.acceleration + tf, car.acceleration))
            print("Set course:", car.path, car.course)

            wait, prev = car.atDistance(self.turnLength(car.path))[0] - self.time, car
        return wait


    # def stop(self, car, distance):
    #     dc, df, tc, vc, a = car.distance, distance, car.time, car.speed, car.acceleration
    #     # sets course of car to stop at distance
    #     ds = df - vc ** 2 / (2 * a) # calculate stopping distance
    #     ts = tc + (ds - dc) / vc # calculate time at which to start decelerating
    #     car.course = [[ts, 2 * (df - ds) / vc + ts, -a]]


    # def go(self, car, speed):
    #     # appends course of car to accelerate to speed (m/s) after delay
    #     tc, vc, vf, a = car.time, car.speed, speed, car.acceleration
    #     car.course = [(tc, abs(vf - vc) / a + tc, math.copysign(a, vf - vc))]

        # tc, dt, vt, vf = self.time, self.turnLength(car.path), self.turnSpeed(car), self.speed

        # d = abs(vt ** 2 - vc ** 2) / (2 * a) # calculate distance to turn speed
        # if dc < dt - d: # can reach turning speed by end of intersection
        #     if dc < 0 - d: car.setCourse(0, tc, vt) # reaching turning speed by start of intersection
        #     else: car.course = [(tc, tc + (vt - vc) / a, a)] # reaching turning speed by end of intersection
        #     tf = car.atDistance(dt)[0]
        #     car.course.append((tf, (vf - vt) / a + tf, a))
        # else: car.course = [(tc, tc + (vf - vc) / a, a)]

    # def go(self, car, prev):
    #     # sets course of car to follow prev through intersection
    #     dc, vc, a = car.distance, car.speed, car.acceleration
    #     tc, dt, vt, vf = self.time, self.turnLength(car.path), self.turnSpeed(car), self.speed

    #     ta, va, vd = 0, min((vc ** 2 - 2 * a * dc) ** 0.5 - 1.e-3, vt), min((vc ** 2 + 2 * a * (dt - dc)) ** 0.5 - 1.e-3, vt)
    #     if prev != None: # if there is a car to follow
    #         (tap, vap), ap = prev.atDistance(0), prev.acceleration
    #         ta = tap + (va - vap) / ap - ((vf ** 2 - vap ** 2) / (2 * ap) - (vf ** 2 - va ** 2) / (2 * a)) / vf + 10 / va
    #         if car.rangeTo(0, va)[1] < ta: ta, va = tap + 10 / vap, min(vap, vt)

    #     car.setCourse(0, ta, va)
    #     ta = car.atDistance(0)[0]
    #     car.course.append((ta, (vd - va) / a + ta, a))
    #     tf = car.atDistance(dt)[0]
    #     car.course.append((tf, (vf - vd) / a + tf, a))
    #     print(car.course)

        # va2, vd2 = car2.atDistance(0), car2.atDistance(dt)
        # if car.path == car2.path and va < va2:


        # d = abs(vt ** 2 - vc ** 2) / (2 * a1) # calculate distance to turn speed
        # if dc < dt - d: # can reach turning speed by end of intersection
        #     if dc < 0 - d: # reaching turning speed by start of intersection
        #         ta = 0 # default is to arrive as soon as possible
        #         if car2 != None: # adjust for other car
        #             ta, va = car2.atDistance(0)
        #             if car2.path == car1.path: ta += (vt - va) / car2.acceleration
        #             print(ta, va)
        #         car1.setCourse(0, ta, vt)
        #         print(car1.course, car1.atDistance(0))
        #     else: # reaching turning speed by end of intersection
        #         car1.course = [(tc, tc + (vt - vc) / a1, a1)]
        #     tf = car1.atDistance(dt)[0]
        #     car1.course.append((tf, (vf - vt) / a1 + tf, a1))
        # else: car1.course = [(tc, tc + (vf - vc) / a1, a1)]




    def tick(self, period):
        # updates properties based on period (ms)
        self.lights = [t - (period / 1000) if t > 0 else 0 for t in self.lights]
        self.signal([4, 0, 3, 1, 5, 7, 2, 6]) # left/straight, straight/straight, straight/left
        super().tick(period)


# def go(car, speed, delay):
#     # sets course so car accelerates to speed (m/s) after delay (s)
#     tc, d, vc, vf, a = car.time, delay, car.speed, speed, car.acceleration
#     tf = (vf - vc) / a + tc + d
#     car.course = [(tc + d, tf, a)]