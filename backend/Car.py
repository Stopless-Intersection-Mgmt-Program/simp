import math

class Car:
    def __init__(self, id, distance, path, speed):
        self.id = id
        self.path = path # tuple containing starting lane and ending lane
        self.top = 100 # top speed (m/s) of car relative to path
        self.acceleration = 5 # acceleration (m/s/s) of car relative to path

        self.time = 0 # time (s) used by intersection to synchronize behavior
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.speed = speed # speed (m/s) of car relative to path
        self.periods = (0, 0, 0), (0, 0, 0) # tuple of tuples containg start and end time (s) markers and magnitude for acceleration periods


    def course(self, distance, time, speed):
        # sets time markers for the two acceleration periods so that car reaches distance (m) at speed (m/s) at time (ms)
        dc, df, vc, vf, tc, tf, a = self.distance, distance, self.speed, speed, self.time, time, self.acceleration

        a, d, t = self.acceleration, -self.acceleration, tf - tc
        rad = ((2 * a ** 2 * d - 2 * a * d ** 2) * df + (2 * a * d ** 2 - 2 * a ** 2 * d) * dc + a * d * vc ** 2 + 
              (2 * a * d ** 2 * t - 2 * a * d * vf) * vc + a ** 2 * d ** 2 * t ** 2 - 2 * a ** 2 * d * vf * t + a * d * vf ** 2) ** 0.5
        vi = (-rad + a * vc + a * d * t - a * vf) / (d - a) # calculate intermediate speed
        print(vi)

        if vi >= vc:
            p0 = (tc, tc + (vi - vc) / a, a) # accelerate to intermediate speed
            p1 = (tf - (vf - vi) / d, tf, d) # decelerate to final speed
        if vi <= vc:
            p0 = (tc, tc + (vi - vc) / d, d) # decelerate to intermediate speed
            p1 = (tf - (vf - vi) / a, tf, a) # accelerate to final speed
        print(p0, p1)
        if p0[1] > p1[0]: p0, p1 = (p0[0], p1[0], p0[2]), (p0[1], p1[1], p1[2])
        print(p0, p1)
        self.periods = p0, p1




    def stats(self, distance):
        # returns time (s) and speed (m/s) when car will reach distance (m) based on the two acceleration periods
        dc, df, vc, tc, a, d = self.distance, distance, self.speed, self.time, self.acceleration, self.deceleration



    def synchronize(self, time):
        # sets internal time to match time (s)
        self.time = time


    def tick(self, time):
        # increments distance and speed to match new time (s) based on the two acceleration periods
        tc, tf, (p0, p1) = self.time, time, self.periods

        if tc < p0[0]: # before first acceleration period
            t = (min(tf, p0[0]) - tc) # relative time (s)
            self.distance += self.speed * t

        if tf >= p0[0] and tc <= p0[1]: # first acceleration period
            t = (min(tf, p0[1]) - max(tc, p0[0])) # relative time (s)
            self.distance += 0.5 * p0[2] * t ** 2 + self.speed * t
            self.speed += p0[2] * t

        if tf > p0[1] and tc < p1[0]: # in between acceleration periods
            t = (min(tf, p1[0]) - max(tc, p0[1])) # relative time (s)
            #self.distance += self.speed * t

        if tf >= p1[0] and tc <= p1[1]: # second acceleration period
            t = (min(tf, p1[1]) - max(tc, p1[0])) # relative time (s)
            self.distance += 0.5 * p1[2] * t ** 2 + self.speed * t
            self.speed += p1[2] * t

        if tf > p1[1]: # after second acceleration period
            t = (tf - max(tc, p1[1])) # relative time (s)
            self.distance += self.speed * t

        self.time = time # synchronize


    def render(self, size):
        # returns coordinates (m) and angle (rad) realtive to center based on path and distance
        x, y, angle = 0, 0, 0 # relative to the bottom left of starting lane
        lin, lout = self.path
        turn = (lout - lin) % 8 // 2 # calculate the modulo difference

        if self.distance <= 0 or turn == 2: # if car is before intersection
            if turn == 0 or turn == 1: x, y, angle = 0.625 * size, self.distance, 0 # left turn lane
            else: x, y, angle = 0.795 * size, self.distance, 0

        elif turn == 0: # U turn
            cut, radius = 0.5, 0.21 * size
            arc = cut * (2 * math.pi * radius) # length of turn
            angle = self.distance / radius # angle completed
            if self.distance >= arc: x, y, angle = 0.205 * size, - (self.distance - arc), math.pi # if passed intersection
            else: x, y = 0.415 * size + radius * math.cos(angle), radius * math.sin(angle)
            
        elif turn == 1: # left turn
            cut, radius = 0.25, 0.625 * size
            arc = cut * (2 * math.pi * radius)
            angle = self.distance / radius
            if self.distance >= arc: x, y, angle = - (self.distance - arc), 0.625 * size, math.pi / 2
            else: x, y = radius * math.cos(angle), radius * math.sin(angle)

        elif turn == 3: # right turn
            cut, radius = 0.25, 0.205 * size
            arc = cut * (2 * math.pi * radius)
            angle = -self.distance / radius
            if self.distance >= arc: x, y, angle = size + (self.distance - arc), 0.205 * size, -math.pi / 2
            else: x, y = size - radius * math.cos(-angle), radius * math.sin(-angle)

        # calculate absolute position
        if lin == 1: return y - size / 2, size - x - size / 2, angle
        if lin == 3: return size - x - size / 2, size - y - size / 2, angle - math.pi / 2
        if lin == 5: return size - y - size / 2, x - size / 2, angle + math.pi
        if lin == 7: return x - size / 2, y - size / 2, angle + math.pi / 2

        return 0, 0, 0 # lane not yet implemented


    def tkrender(self, size, canvas, scale):
        # draws and returns polygon on tkinter canvas in accordance to scale (pixels / m)
        ps = []
        l, w = 4, 2 # size of rectangle
        x, y, direction = self.render(size)
        for sl, sw in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
            # generate base points
            bx, by = x + sl * l / 2, y + sw * w / 2

            # rotate points depending on direction
            px = x + math.cos(direction) * (bx - x) - math.sin(direction) * (by - y)
            py = y + math.sin(direction) * (bx - x) + math.cos(direction) * (by - y)

            # scale and translate points relative to center
            ps.append(int(canvas.cget("width")) / 2 + px * scale)
            ps.append(int(canvas.cget("height")) / 2 - py * scale)

        return canvas.create_polygon(ps, fill="grey", width=2, outline="white") # draw polygon