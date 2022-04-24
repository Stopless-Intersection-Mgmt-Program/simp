import math
import tkinter as tk

class Car:
    def __init__(self, id, distance, path, speed):
        self.id = id
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.path = path # tuple containing starting lane and ending lane
        self.speed = speed # speed (m/s) of car relative to path

        self.acceleration = 0 # acceleration (m/s/s) of car relative to path
        self.jerk = 0 # jerk (m/s/s/s) of car relative to path (change in acceleration)


    def course(self, distance, time, speed):
        # sets acceleration (m/s/s) and jerk (m/s/s/s) so that car reaches distance (m) at speed (m/s) in time (s)
        dc, df, vc, vf, t = self.distance, distance, self.speed, speed, time

        # these equations are based on a rather complicated solution to a system
        self.acceleration = -2 * (vf ** 2 * (2 * vc * t - df + 3 * dc) + vf ** 3 * t - 2 * df * vc * vf) / (vf ** 2 * t ** 2 - 2 * df * vf * t + df ** 2)
        self.jerk = 6 * (vf ** 3 * (vc * t - df + 2 * dc) + vf ** 4 * t - df * vc * vf ** 2) / (vf ** 3 * t ** 3 - 3 * df * vf ** 2 * t ** 2 + 3 * df ** 2 * vf * t - df ** 3)


    def stats(self, distance):
        # returns time (s) until car reaches distance (m) and speed (m/s) based on acceleration (m/s/s) and jerk (m/s/s/s)
        dc, df, v, a, j = self.distance, distance, self.speed, self.acceleration, self.jerk 
        if j == 0 and a == 0: return (df - dc) / v, v # if no jerk and acceleration, then speed is constant

        # the solution to the position equation yields three roots, t0, t1, and t2, which can be complex
        rad = (((8 * j * v ** 3 - 3 * a ** 2 * v ** 2 - 18 * a * dc * j * v + 9 * dc ** 2 * j ** 2 + 6 * a ** 3 * dc) ** 0.5 + 3 * a * v - 3 * dc * j) / (j ** 2) - a ** 3 / j ** 3) ** (1 / 3)
        t0 = (rad - (2 * v / j - a ** 2 / j ** 2) / rad - (a / j))
        t1 = ((-1 - (-3) ** 0.5) / 2 * rad - ((-3) ** 0.5 - 1) / 2 * (2 * v / j - a ** 2 / j ** 2) / rad - (a / j))
        t2 = (((-3) ** 0.5 - 1) / 2 * rad - (-1 - (-3) ** 0.5) / 2 * (2 * v / j - a ** 2 / j ** 2) / rad - (a / j))
        t = min(t.real for t in [t0, t1, t2] if t.real > 0 and abs(t.imag) < 0.001) # choose the first positive real solution

        return t + df / (0.5 * j * t ** 2 + a * t + v), 0.5 * j * t ** 2 + a * t + v # calculate total time and final speed


    def tick(self, period):
        # increments time-varying values adjusted for period length (ms)
        d, v, a, j, t = self.distance, self.speed, self.acceleration, self.jerk, period / 1000
        if d >= 0: self.distance = v * t + d # if passed intersection, speed is constant

        else: # if before intersection consider jerk and acceleration
            df = 1 / 6 * j * t ** 3 + 0.5 * a * t ** 2 + v * t + d
            if df < 0: self.distance, self.speed, self.acceleration = df, 0.5 * j * t ** 2 + a * t + v, j * t + a
            else: # this is the period where we cross into the intersection
                ti, vf = self.stats(0)
                self.distance, self.speed = 1 / 6 * j * ti ** 3 + 0.5 * a * ti ** 2 + v * ti + vf * (t - ti) + d, vf


    def render(self, size):
        # returns coordinates (m) and angle (rad) realtive to center based on path and distance
        # UPDATES: currently only handles a 1, 3, 5, 7 intersection
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

        return canvas.create_polygon(ps, fill="grey", width=2, outline="white")




class Intersection:
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size # length (m) of one side of the intersection
        self.time = 0 # clock to track time (ms) elapsed
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds new car for intersection to schedule
        # based on scheduling algorithm, should assign a car to follow
        if len(self.cars) > 0: self.follow(car, self.cars[-1]) # FIFO
        self.cars.append(car)
        return # to be implemented


    def follow(self, car1, car2):
        # sets car1 to pass through intersection immediately after car2
        # if car1 and car2 do not share a critical section, do nothing
        # UPDATES: needs to consider other cars along path
        overlap = self.overlap(car1.path, car2.path)
        if overlap == None: return
        stats = car2.stats(overlap[1])
        car1.course(overlap[0], stats[0], stats[1])
        return # to be implemented


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        # if there is no critical section, returns None
        # can be implemented as a table for each intersection layout
        arc = 2 * math.pi * (0.625 * self.size)
        if path1 == path2: return 0, 8
        if path1 == (7, 1) and path2 == (1, 3): return arc / 8, arc / 8
        if path1 == (1, 3) and path2 == (7, 1): return arc / 16, arc / 6
        if path1 == (5, 7) and path2 == (7, 1): return arc / 8, arc / 8
        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time
        for car in self.cars: car.tick(period)
        self.time = (self.time + period) % (2 ** 63 - 1)

    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        # render cars
        for car in self.cars: car.tkrender(self.size, canvas, scale)




# Test Driver Code

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=400, width=800)
canvas.pack()

# sample code
intersection = Intersection(0, 40)

car0 = Car(0, -50, (1, 3), 30)
car1 = Car(1, -40, (7, 1), 30)
car2 = Car(2, -90, (1, 3), 30)
car3 = Car(2, -50, (7, 1), 30)
car4 = Car(2, -60, (5, 7), 30)

intersection.schedule(car0)
intersection.schedule(car1)
intersection.schedule(car2)
intersection.schedule(car3)
intersection.schedule(car4)

while True:
    canvas.delete("all")
    intersection.tick(10)
    intersection.tkrender(canvas, 5)
    canvas.update()
    root.after(10)
root.mainloop()