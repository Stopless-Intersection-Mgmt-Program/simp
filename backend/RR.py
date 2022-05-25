import Intersection

# not finish: doesn't back to intersection speed when out
# this is not really round robin, but each lane wouldn't occupy the order for more than two cars if there's other lane's car need to go
# if the schedule radius (acceleration allowed need to be bigger) can be smaller, it should be more effecient

class RR(Intersection.Intersection):
    def __init__(self, buffer, spawn = 0):
        super(RR, self).__init__(buffer, spawn)
        self.laneCount = [0, 0, 0, 0, 0, 0, 0, 0] # number of car in each lane
        self.waiting = [] # waiting to be schedule, -30 <= d < 0
        self.finish = [] # distance >= 0
        self.startSchedule = -301
        self.endSchedule = -150
    
    def schedule(self, car):
        # adds car for intersection to handle
        car.time = self.time # synchronize clocks
        vt, dt = self.turnSpeed(car), self.turnLength(car.path)

        # loop through other cars and set car to arrive after each
        car.setCourse(0, 0, vt)
        for other in self.cars:
            if other.path[0] == car.path[0]: self.arriveAfter(car, other)
            # if other.path[1] == car.path[1]: self.arriveAfter(car, other)
        for other in self.waiting:
            if other.path[0] == car.path[0]: self.arriveAfter(car, other)
            # if other.path[1] == car.path[1]: self.arriveAfter(car, other)
        for other in self.finish:
            if other.path[0] == car.path[0]: self.arriveAfter(car, other)
            # if other.path[1] == car.path[1]: self.arriveAfter(car, other)

        tf = car.atDistance(dt)[0]
        car.course.append((tf, (self.speed - vt) / car.acceleration + tf, car.acceleration))
        
        self.waiting.append(car)

    def tick(self, period):
        # updates properties based on period (ms)
        self.time += period / 1000
        for car in self.waiting:
            if car.distance >= self.startSchedule: # now really schedule it
                self.laneCount[car.path[0]] += 1
                rr = [0, 0, 0, 0, 0, 0, 0, 0]
                i = 0
                count = 0
                while i < len(self.cars):
                    if car.path[0] != self.cars[i].path[0]:
                        if rr[self.cars[i].path[0]] <= self.laneCount[car.path[0]]:
                            self.arriveAfter(car, self.cars[i])
                            rr[self.cars[i].path[0]] += 1
                        else:
                            # if count >= self.laneCount[car.path[0]] - 1: 
                            #     print(self.laneCount, [p.path for p in self.cars], i+1,car.path)
                            break
                    else:
                        count += 1
                        self.arriveAfter(car, self.cars[i])
                    i += 1
                self.cars.insert(i, car)
                for j in range(i + 1, len(self.cars)):
                    for k in range (i, j):
                        self.arriveAfter(self.cars[j], self.cars[k])
                for other in self.finish: self.arriveAfter(car, other)
                tf = car.atDistance(self.turnLength(car.path))[0]
                car.course.append((tf, (self.speed - self.turnSpeed(car)) / car.acceleration + tf, car.acceleration))
        for i in range(len(self.waiting) - 1, -1, -1):
            if self.waiting[i].distance >= self.startSchedule:
                del self.waiting[i]
        for i in range(len(self.cars) - 1, -1, -1):
            if self.cars[i].distance >= self.endSchedule:
                self.finish.append(self.cars[i])
                tf = self.cars[i].atDistance(self.turnLength(self.cars[i].path))[0]
                # self.cars[i].course.append((tf, (self.speed - self.turnSpeed(self.cars[i])) / self.cars[i].acceleration + tf, self.cars[i].acceleration))
                tf = self.cars[i].atDistance(self.turnLength(self.cars[i].path))
                self.cars[i].course = [self.cars[i].course[0], (tf[0], (self.speed - tf[1]) / self.cars[i].acceleration + tf[0], self.cars[i].acceleration)]
                self.laneCount[self.cars[i].path[0]] -= 1
                del self.cars[i]
        for car in self.waiting:
            car.tick(period)
        for car in self.cars:
            car.tick(period)
        for car in self.finish:
            car.tick(period)
            if car.distance > self.radius: self.finish.remove(car)

        if self.spawn > 0: self.spawner(period)

    def render(self):
        # returns list of car ids, coordinates, and directions
        return [(car.id) + car.render(self.size) + (car.speed) for car in self.waiting] + [(car.id) + car.render(self.size) + (car.speed) for car in self.cars] +\
            [(car.id) + car.render(self.size) + (car.speed) for car in self.finish]


    def tkrender(self, canvas, scale):
        # renders intersection and each car on canvas
        x0, y0 = int(canvas.cget("width")) / 2 + self.size / 2 * scale, int(canvas.cget("height")) / 2 - self.size / 2 * scale
        x1, y1 = int(canvas.cget("width")) / 2 - self.size / 2 * scale, int(canvas.cget("height")) / 2 + self.size / 2 * scale
        canvas.create_rectangle(x0, y0, x1, y1, fill="", width=2, outline="grey12")

        for car in self.waiting: car.tkrender(self.size, canvas, scale)
        for car in self.cars: car.tkrender(self.size, canvas, scale) # render each car
        for car in self.finish: car.tkrender(self.size, canvas, scale)