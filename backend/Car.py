import math

class Car:
    def __init__(self, id, distance, path):
        self.id = id
        self.path = path # tuple containing starting lane and ending lane
        self.acceleration = 5 # acceleration (m/s/s) of car relative to path

        self.time = 0 # time (s) used by intersection to synchronize behavior
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.speed = 40 # speed (m/s) of car relative to path
        self.course = None # tuple containing a start time, switching time, end time, and acceleration


    def setCourse(self, distance, time):
        # sets course to reach distance (m) at time (s) with current speed
        dc, df, tc, tf, v = self.distance, distance, self.time, time, self.speed
        a = 4 * ((df - dc) - (tf - tc) * v) / (tf - tc) ** 2
        self.course = (tc, 0.5 * (tf + tc), tf, a)


    def timeTo(self, distance):
        # returns time (s) when car will reach distance (m)
        dc, df, tc, v = self.distance, distance, self.time, self.speed
        if self.course == None: # no course
            return (df - dc) / v
        cs, cm, ce, ca = self.course

        if tc < cs: # before acceleration period
            t, d = cs - tc, v * (cs - tc) # relative time and distance
            if dc + d > df: return tc + (df - dc) / v # will finish in this section
            tc, dc = tc + t, dc + d

        if tc < cm: # before switching point
            t, d = cm - tc, 0.5 * ca * (cm - tc) ** 2 + v * (cm - tc)
            if dc + d > df: return tc + ((2 * ca * (df - dc) + v ** 2) ** 0.5 - v) / ca
            tc, dc, v = tc + t, dc + d, v + ca * t

        if tc < ce: # after switching point
            t, d = ce - tc, v * (ce - tc) - 0.5 * ca * (ce - tc) ** 2
            if dc + d > df: return tc - ((v ** 2 - 2 * ca * (df - dc)) ** 0.5 - v) / ca
            tc, dc, v = tc + t, dc + d, v - ca * t

        if tc >= ce: # after acceleration period
            return tc + (df - dc) / v


    def rangeTo(self, distance):
        # returns interval of times (s) that car could arrive at distance (m) with current speed
        dc, df, tc, v, a = self.distance, distance, self.time, self.speed, self.acceleration
        if self.course != None: # course already set
            t = self.timeTo(distance)
            return t, t
        ts = 2 * ((a * (df - dc) + v ** 2) ** 0.5 - v) / a + tc
        tl = -2 * ((v ** 2 - a * (df - dc)) ** 0.5 - v) / a + tc
        return ts, (tl if not isinstance(tl, complex) else -1) # -1 if infinite


    def tick(self, time):
        # increments distance to match new time (s)
        dc, tc, tf, v = self.distance, self.time, time, self.speed
        if self.course == None: # no course
            self.distance = dc + (tf - tc) * v
            self.time = tf
            return
        cs, cm, ce, ca = self.course

        if tc < cs: # before acceleration period
            t = (min(tf, cs) - tc) # relative time
            dc = dc + t * v

        if tf >= cs and tc <= cm: # before switching point
            t = (min(tf, cm) - max(tc, cs))
            dc, v = dc + 0.5 * ca * t ** 2 + v * t, v + ca * t
        
        if tf >= cm and tc <= ce: # after switching point
            t = (min(tf, ce) - max(tc, cm))
            dc, v = dc + v * t - 0.5 * ca * t ** 2, v - ca * t
        
        if tf > ce: # after acceleration period
            t = (tf - max(tc, ce))
            dc = dc + t * v
        
        # update properties
        self.speed = v
        self.distance = dc
        self.time = tf # synchronize


    def render(self, size):
        # returns coordinates (m) and angle (rad) realtive to center based on path and distance
        dc, (li, lo) = self.distance, self.path
        turn = (lo - li) % 8 // 2 # calculate the modulo difference

        # calculate relative to the bottom left of starting lane
        if dc <= 0 or turn == 2: # if car is before intersection
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
        if li == 1: return y - size / 2, size - x - size / 2, angle
        if li == 3: return size - x - size / 2, size - y - size / 2, angle - math.pi / 2
        if li == 5: return size - y - size / 2, x - size / 2, angle + math.pi
        if li == 7: return x - size / 2, y - size / 2, angle + math.pi / 2


    def tkrender(self, size, canvas, scale):
        # draws and returns polygon on tkinter canvas in accordance to scale (pixels / m)
        ps = []
        l, w = 4, 2 # size of rectangle
        x, y, angle = self.render(size)
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