import math

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
        dc, df, tc, tf, vc, vf, a = self.distance, distance, self.time, time, self.speed, speed, self.acceleration
        ranges = self.courseRanges(df, vf)

        # check if in ++ or -- course range
        if tf >= ranges[1] and tf <= ranges[2]:
            if vf < vc: a = -a
            t = (vf ** 2 - 2 * vc * vf + vc ** 2 + 2 * a * (tf - tc) * vc - 2 * a * (df - dc)) / (2 * a * ((vf - vc) - a * (tf - tc)))
            self.course = [(tc, tc + t, a), (tf - ((vf - vc) / a - t), tf, a)]

        # check if in +- or -+ course range
        elif tf >= ranges[0] and tf <= ranges[3]:
            if tf >= ranges[2]: a = -a
            t = (math.copysign(1, -a) * (2 * (vc + a * (tf - tc)) * vf - vf ** 2 + 2 * a * (tf - tc) * vc - vc ** 2 + a ** 2 * (tf ** 2 - 2 * tc * tf + tc ** 2) - 4 * a * (df - dc)) ** 0.5 + (vf - vc) + a * (tf - tc)) / (2 * a)
            self.course = [(tc, tc + t, a), (tf - ((vc - vf) / a + t), tf, -a)]


    def courseRanges(self, distance, speed):
        # returns array of times (s) that car could arrive at distance (m) with speed (m/s) for each course
        dc, df, tc, vc, vf, a = self.distance, distance, self.time, self.speed, speed, self.acceleration
        vl, vh, ranges = min(vf, vc), max(vf, vc), []

        # time range for +- course
        ts = ((2 * (vf ** 2 + vc ** 2 + 2 * a * (df - dc))) ** 0.5 - vf - vc + a * tc) / a
        tl = (vl ** 2 - 2 * vh * vl + vh ** 2 + 2 * a * tc * vh + 2 * a * (df - dc)) / (2 * a * vh)
        ranges += [ts, tl]

        a = -a # switch acceleration sign

        # time range for -+ course
        ts = (vh ** 2 - 2 * vl * vh + vl ** 2 + 2 * a * tc * vl + 2 * a * (df - dc)) / (2 * a * vl)
        tl = ((2 * (vf ** 2 + vc ** 2 + 2 * a * (df - dc))) ** 0.5 - vf - vc + a * tc) / a     
        ranges += [ts, float('inf') if isinstance(tl, complex) else tl]
        return ranges


    def rangeTo(self, distance, speed):
        # returns interval of times (s) that car could arrive at distance (m) with speed (m/s)
        ranges = self.courseRanges(distance, speed)
        return ranges[0], ranges[3]


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
            return tc + (df - dc) / v, v


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
        if li == 0: x, y, angle = y - size / 2, size - x - size / 2, angle
        if li == 1: x, y, angle = size - x - size / 2, size - y - size / 2, angle - math.pi / 2
        if li == 2: x, y, angle = size - y - size / 2, x - size / 2, angle + math.pi
        if li == 3: x, y, angle = x - size / 2, y - size / 2, angle + math.pi / 2
        return self.id, x, y, angle, self.speed


    def tkrender(self, size, canvas, scale):
        # draws and returns polygon on tkinter canvas in accordance to scale (pixels / m)
        ps = []
        l, w = 4, 2 # size of rectangle
        id, x, y, angle, v = self.render(size)
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