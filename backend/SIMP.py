import math
import tkinter as tk

class Car:
    def __init__(self, id, distance, path, speed):
        self.id = id
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.path = path # tuple containing starting lane and ending lane
        self.speed = speed # speed (m/s) of car relative to path
        self.acceleration = 0 # acceleration (m/s/s) of car relative to path, must be 0 while in intersection
        self.critical = 0 # distance at which car clears critical section


    def accelerate(self, distance, time):
        # sets acceleration so that car reaches distance in time (s). Note that acceleration is 0 while in intersection
        dc, df, v, t = self.distance, distance, self.speed, time
        radical = -(4 * dc ** 2 - 4 * dc * (df - v * t) + (df + v * t) ** 2) ** 0.5
        self.acceleration = (-2 * dc * (radical - 2 * df + 2 * v * t) + (df - v * t) * (radical - df - v * t) - 4 * dc ** 2) / (4 * dc * t ** 2)


    def time(self, distance):
        # returns time (s) until car reaches distance (m) based on acceleration. Note that acceleration is 0 while in intersection
        dc, df, v, a = self.distance, distance, self.speed, self.acceleration
        return (df - dc) / v if a == 0 else (-v + (v ** 2 - 2 * a * dc) ** 0.5) / a + df / (v ** 2 - 2 * a * dc) ** 0.5


    def tick(self, period):
        # increments time-varying values adjusted for period length (ms)
        # UPDATES: needs to adjust acceleration after clearing intersection
        self.speed += self.acceleration * (period / 1000)
        self.distance += self.speed * (period / 1000)
        if self.distance >= 0: self.acceleration = 0 # no acceleration in intersection


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
        car1.accelerate(overlap[0], car2.time(overlap[1])) # what if car2 will not make it to overlap[1] given current acceleration?
        return # to be implemented


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        # if there is no critical section, returns None
        # can be implemented as a table for each intersection layout
        arc = 2 * math.pi * (0.625 * self.size)
        if path1 == (7, 1) and path2 == (1, 3): return arc / 8, arc / 8
        if path1 == (1, 3) and path2 == (7, 1): return arc / 12, arc / 6
        if path1 == (5, 7) and path2 == (7, 1): return arc / 8, arc / 8
        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time
        for car in self.cars: car.tick(period)
        self.time = (self.time + period) % (2 ** 63 - 1)

    def tkrender(self, canvas, scale):
        for car in self.cars: car.tkrender(self.size, canvas, scale)




# Test Driver Code

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=400, width=800)
canvas.pack()

# sample code
intersection = Intersection(0, 40)

car0 = Car(0, -20, (1, 3), 30)
car1 = Car(1, -40, (7, 1), 30)
car2 = Car(2, -60, (5, 7), 30)

intersection.schedule(car0)
intersection.schedule(car1)
intersection.schedule(car2)

while True:
    canvas.delete("all")
    intersection.tick(10)
    intersection.tkrender(canvas, 5)
    canvas.update()
    root.after(10)
root.mainloop()