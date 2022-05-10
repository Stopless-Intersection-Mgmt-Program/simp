import math

# THINGS TO FIX:
# - setCourse should not result in courses that have the car backup, instead car should stop and wait

class Car:
    def __init__(self, id, distance, path):
        self.id = id
        self.path = path # tuple containing starting lane and ending lane
        self.acceleration = 5 # acceleration (m/s/s) of car relative to path
        self.turning = 1 # coefficient of turning (1/s)

        self.time = 0 # time (s) used by intersection to synchronize behavior
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.speed = 40 # speed (m/s) of car relative to path
        self.course = [] # list of tuples containing a start time, end time, and acceleration


    def setCourse(self, distance, time, speed):
        # sets course to reach distance (m) at time (s) with speed (m/s)
        dc, df, tc, tf, vc, vf = self.distance, distance, self.time, time, self.speed, speed
        if vf == vc: # no change in speed
            a = 4 * ((df - dc) - (tf - tc) * vf) / (tf - tc) ** 2
            t = (tf + tc) / 2

        else: # change in speed
            sign = 1 if (vf + vc) / 2 * (tf - tc) < df - dc else -1 # determine sign of radical
            rad = sign * (2 * (2 * (df ** 2 + ((tc - tf) * (vf + vc) - 2 * dc) * df + (tf - tc) * (vf + vc) * dc + dc ** 2) + (tf ** 2 - 2 * tc * tf + tc ** 2) * (vf ** 2 + vc ** 2))) ** 0.5
            a = (rad + 2 * df - 2 * dc + (tc - tf) * (vf + vc)) / (tf ** 2 - 2 * tc * tf + tc ** 2)
            t = (rad - 2 * df + 2 * dc + (2 * tf - 2 * tc) * vf) / (2 * vf - 2 * vc)
        
        # assign course
        self.course = [(tc, tc + t, a), (tc + t, tf, -a)]


    def stop(self, distance):
        # sets course so car stops at distance (m)
        dc, df, tc, v = self.distance, distance, self.time, self.speed
        a, tf = v ** 2 / (-2 * (df - dc)), 2 * (df - dc) / v + tc
        self.course = [(tc, tf, a)]


    def go(self, speed, delay):
        # sets course so car accelerates to speed (m/s) after delay (s)
        tc, d, vc, vf, a = self.time, delay, self.speed, speed, self.acceleration
        tf = (vf - vc) / a + tc + d
        self.course = [(tc + d, tf, a)]


    def accelerate(self, speed, time):
        # adds course so car changes speed (m/s) at time (s)
        ts, v, a = time, speed, self.acceleration
        tf = v / a + ts
        self.course.append((ts, tf, a))


    def atDistance(self, distance):
        # returns time (s) and speed (m/s) when car is at distance (m)
        dc, df, tc, v = self.distance, distance, self.time, self.speed
        if self.course == []: # no course
            return (df - dc) / v, v
        for course in self.course: # loop through course nodes
            cs, ce, ca = course

            if tc < cs: # before acceleration period
                t, d = cs - tc, v * (cs - tc) # relative time and distance
                if dc + d > df: return tc + (df - dc) / v, v # will finish in this section
                tc, dc = tc + t, dc + d

            if tc < ce: # during acceleration period
                t, d = ce - tc, 0.5 * ca * (ce - tc) ** 2 + v * (ce - tc)
                if dc + d > df: return tc + ((2 * ca * (df - dc) + v ** 2) ** 0.5 - v) / ca, (v ** 2 + 2 * ca * (df - dc)) ** 0.5
                tc, dc, v = tc + t, dc + d, v + ca * t

        if tc >= ce: # after acceleration period
            return tc + (df - dc) / v


    def atTime(self, time):
        # returns distance (m) and speed (m/s) of car at time (s)
        dc, tc, tf, v = self.distance, self.time, time, self.speed
        if self.course == []: # no course
            return dc + (tf - tc) * v, v

        for course in self.course: # loop through course nodes
            cs, ce, ca = course

            if tc < cs: # before acceleration period
                t = (min(tf, cs) - tc) # relative time
                tc, dc = tc + t, dc + t * v

            if tf >= cs and tc <= ce: # during acceleration period
                t = (min(tf, ce) - max(tc, cs))
                tc, dc, v = tc + t, dc + 0.5 * ca * t ** 2 + v * t, v + ca * t
        
        if tf > ce: # after acceleration period
            t = (tf - max(tc, ce))
            dc = dc + t * v
        return dc, v


    def rangeTo(self, distance, speed):
        # returns interval of times (s) that car could arrive at distance (m) with speed (m/s)
        dc, df, tc, vc, vf, a = self.distance, distance, self.time, self.speed, speed, self.acceleration
        ts = ((4 * a * (df - dc) + 2 * vf ** 2 + 2 * vc ** 2 - a ** 2 * tc ** 2) ** 0.5 - vf - vc) / a
        tl = ((4 * a * (dc - df) + 2 * vf ** 2 + 2 * vc ** 2 + a ** 2 * tc ** 2) ** 0.5 - vf - vc) / -a
        if isinstance(tl, complex): tl = 100
        return (ts, tl)
        

    def tick(self, time):
        # updates properties to match new time (s)
        self.distance, self.speed = self.atTime(time)
        self.time = time # synchronize


    def render(self, size):
        # returns coordinates (m) and angle (rad) realtive to center based on path and distance
        dc, (li, lo) = self.distance, self.path
        turn = (lo - li) % 4 # calculate the modulo difference

        # calculate relative to the bottom left of starting lane
        if dc <= 0 or turn == 2: # if car is before intersection or going straight
            if turn == 0 or turn == 1: x, y, angle = 0.625 * size, dc, 0 # left turn lane
            else: x, y, angle = 0.795 * size, dc, 0

        elif turn == 0: # U turn
            r = 0.21 * size
            arc, angle = 0.5 * (2 * math.pi * r), dc / r  # length of turn and angle completed
            if dc >= arc: x, y, angle = 0.205 * size, -(dc - arc), math.pi # if passed intersection
            else: x, y = 0.415 * size + r * math.cos(angle), r * math.sin(angle)
            
        elif turn == 1: # left turn
            r = 0.625 * size
            arc, angle = 0.25 * (2 * math.pi * r), dc / r
            if dc >= arc: x, y, angle = -(dc - arc), 0.625 * size, math.pi / 2
            else: x, y = r * math.cos(angle), r * math.sin(angle)

        elif turn == 3: # right turn
            r = 0.205 * size
            arc, angle = 0.25 * (2 * math.pi * r), -dc / r
            if dc >= arc: x, y, angle = size + (dc - arc), 0.205 * size, -math.pi / 2
            else: x, y = size - r * math.cos(-angle), r * math.sin(-angle)

        # calculate absolute position
        if li == 0: return self.id, y - size / 2, size - x - size / 2, angle
        if li == 1: return self.id, size - x - size / 2, size - y - size / 2, angle - math.pi / 2
        if li == 2: return self.id, size - y - size / 2, x - size / 2, angle + math.pi
        if li == 3: return self.id, x - size / 2, y - size / 2, angle + math.pi / 2


    def tkrender(self, size, canvas, scale):
        # draws and returns polygon on tkinter canvas in accordance to scale (pixels / m)
        ps = []
        l, w = 4, 2 # size of rectangle
        id, x, y, angle = self.render(size)
        for sl, sw in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
            # generate base points
            bx, by = x + sl * l / 2, y + sw * w / 2

            # rotate points depending on direction
            px = x + math.cos(angle) * (bx - x) - math.sin(angle) * (by - y)
            py = y + math.sin(angle) * (bx - x) + math.cos(angle) * (by - y)

            # scale and translate points relative to center
            ps.append(int(canvas.cget("width")) / 2 + px * scale)
            ps.append(int(canvas.cget("height")) / 2 - py * scale)

        return canvas.create_polygon(ps, fill="grey", width=2, outline="white") # draw polygon