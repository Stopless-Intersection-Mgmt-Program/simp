import math
import tkinter as tk

class Car:
    def __init__(self, id, distance, path, speed):
        self.id = id
        self.distance = distance # distance (m) relative to the enterance of the intersection (negative means approaching intersection)
        self.path = path # tuple containing starting lane and ending lane
        self.speed = speed # speed (m/s) of car relative to path
        self.acceleration = 0 # acceleration (m/s/s) of car relative to path

        self.following = None # car object to follow
        self.gap = 0 # gap (m or ms) to car being followed
        self.unit = "m" # unit ("m" or "s") to specify type of gap


    def accelerate(self, distance, time):
        # sets acceleration so that car reaches distance in time (s)
        self.acceleration = ((distance - self.distance) - self.speed * time) * 2 / (time ** 2)


    def time(self, distance):
        # returns time (s) until car reaches distance (m) based on acceleration
        if self.acceleration == 0: return (distance - self.distance) / self.speed
        t = (-self.speed + (self.speed ** 2 + 2 * self.acceleration * (distance - self.distance)) ** 0.5) / self.acceleration
        return t if not complex else 1


    def follow(self):
        # adjusts acceleration to keep gap (m or ms) to other car
        # UPDATES: results in very harsh accelerations
        if self.following == None: return
        if self.unit == "m": # gap is distance
            self.accelerate(self.following.distance, self.following.time(self.following.distance + self.gap))
        if self.unit == "s": # gap is time
            self.accelerate(self.following.distance, self.gap)


    def tick(self, period):
        # increments time-varying values adjusted for period length (ms)
        self.follow()
        self.speed += self.acceleration * (period / 1000)
        self.distance += self.speed * (period / 1000)


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
            cut, radius = 1 / 2, 0.21 * size
            arc = cut * (2 * math.pi * radius) # length of turn
            angle = self.distance / radius # angle completed
            if self.distance >= arc: x, y, angle = 0.205 * size, - (self.distance - arc), math.pi # if passed intersection
            else: x, y = 0.415 * size + radius * math.cos(angle), radius * math.sin(angle)
            
        elif turn == 1: # left turn
            cut, radius = 1 / 4, 0.625 * size
            arc = cut * (2 * math.pi * radius)
            angle = self.distance / radius
            if self.distance >= arc: x, y, angle = - (self.distance - arc), 0.625 * size, math.pi / 2
            else: x, y = radius * math.cos(angle), radius * math.sin(angle)

        elif turn == 3: # right turn
            cut, radius = 1 / 4, 0.205 * size
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


    def tkrender(self, size, canvas, scale, color):
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

        return canvas.create_polygon(ps, fill=color, width=2, outline="white")




class Intersection:
    def __init__(self, algorithm, size):
        self.algorithm = algorithm
        self.size = size # length (m) of one side of the intersection
        self.time = 0 # clock to track time (ms) elapsed
        self.cars = [] # list of cars monitored by the intersection


    def schedule(self, car):
        # adds new car for intersection to schedule
        self.cars.append(car)
        # based on scheduling algorithm, should assign a car to follow
        return # to be implemented


    def separate(self, car1, car2):
        # sets car1 to pass through intersection immediately after car2
        # if car1 and car2 do not share a critical section, do nothing
        overlap = self.overlap(car1.path, car2.path)
        if overlap == None: return
        car1.accelerate(overlap[0], car2.time(overlap[1]))
        return # to be implemented


    def overlap(self, path1, path2):
        # returns start distance on path1 and end distance on path2 of critical section
        # if there is no critical section, returns None
        # can be implemented as a table for each intersection layout
        return # to be implemented


    def tick(self, period):
        # ticks each car and increments the time
        for car in self.cars: car.tick(period)
        self.time = (self.time + period) % (2 ** 63 - 1)




# Test Driver Code

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=400, width=800)
canvas.pack()

# sample code
car0 = Car(0, -30, (1, 3), 30) # car going straight starting 100m before intersection going 20 m/s
car1 = Car(0, -50, (7, 1), 30) # same as car0, just 30m behind and opposite side
car2 = Car(0, -40, (1, 3), 30) # same as car0, just 10m behind

car1.following, car1.gap, car1.unit = car0, 3, "m"
car2.following, car2.gap, car2.unit = car0, 17, "m"

cars = [car0, car1, car2]
while True:
    canvas.delete("all")
    for car in cars: car.tick(10)
    for car in cars: car.tkrender(30, canvas, 5, "grey")
    canvas.update()
    root.after(10) # <== ...as this value
root.mainloop()