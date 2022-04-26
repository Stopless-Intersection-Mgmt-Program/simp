import tkinter as tk
import Car as c
import Intersection as i


# test code
# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=400, width=800)
canvas.pack()

# sample intersection and cars
intersection = i.Intersection(0, 40)

# # spawn cars
# car0 = c.Car(0, -50, (1, 3), 50)
# car1 = c.Car(1, -40, (7, 1), 50)
# car2 = c.Car(2, -90, (1, 3), 50)
# car3 = c.Car(2, -50, (7, 1), 50)
# car4 = c.Car(2, -60, (5, 7), 50)

# # schedule cars
# intersection.schedule(car0)
# intersection.schedule(car1)
# intersection.schedule(car2)
# intersection.schedule(car3)
# intersection.schedule(car4)

car0 = c.Car(0, -200, (1, 3), 40)
car0.course(0, 5)
intersection.schedule(car0)

# main loop
while True:
    canvas.delete("all")
    intersection.tick(10)
    intersection.tkrender(canvas, 2)
    canvas.update()
    print(intersection.time, car0.speed, car0.distance)
    root.after(10)
root.mainloop()


# w, z, v, f, a, d, t, tf, tc = dc, df, vc, vf, a, d, tf, tf, self.time
# x1 = ((2 * d * v + 2 * a * d * t - 2 * a * f) * rad + (2 * a ** 2 * d - 2 * a * d ** 2) * z + (4 * a * d ** 2 - 6 * a ** 2 * d + 2 * a ** 3) * w + (3 * a * d - a ** 2) * v ** 2 + (4 * a * d ** 2 * t - 4 * a * d * f) * v + 2 * a ** 2 * d ** 2 * t ** 2 - 4 * a ** 2 * d * f * t + (a * d + a ** 2) * f ** 2) / (2 * a * d ** 2 - 4 * a ** 2 * d + 2 * a ** 3)
# x2 = ((2 * d * v + 2 * a * d * t - 2 * a * f) * rad + (2 * d ** 3 - 6 * a * d ** 2 + 4 * a ** 2 * d) * z + (2 * a * d ** 2 - 2 * a ** 2 * d) * w + (d ** 2 + a * d) * v ** 2 + (4 * a * d ** 2 * t - 4 * a * d * f) * v + 2 * a ** 2 * d ** 2 * t ** 2 - 4 * a ** 2 * d * f * t + (3 * a * d - d ** 2) * f ** 2) / (2 * d ** 3 - 4 * a * d ** 2 + 2 * a ** 2 * d)
# return (dc, x1), (x2, df)

# def course(self, distance, time, speed):
#         # sets time markers for the two acceleration periods so that car reaches distance (m) at speed (m/s) at time (ms)
#         dc, df, vc, vf, tc, tf = self.distance, distance, self.speed, speed, self.time, time

#         t = (tf - tc) # system of constraining equations uses relative time (s)
        
#         a0, a1 = self.acceleration, self.deceleration
#         a0, a1 = a1, a0

#         rad = ((2 * a0 ** 2 * a1 - 2 * a0 * a1 ** 2) * df + (2 * a0 * a1 ** 2 - 2 * a0 ** 2 * a1) * dc + a0 * a1 * vc ** 2 + 
#               (2 * a0 * a1 ** 2 * t - 2 * a0 * a1 * vf) * vc + a0 ** 2 * a1 ** 2 * t ** 2 - 2 * a0 ** 2 * a1 * vf * t + a0 * a1 * vf ** 2) ** 0.5 
#         t0 = (rad + a0 * vc + a0 * a1 * t - a0 * vf) / (a0 * a1 - a0 ** 2)
#         t1 = (-rad + a1 * vc + a0 * a1 * t - a1 * vf) / (a1 ** 2 - a0 * a1)

#         print(t0, t1)
#         if t0 * a0 + vc > self.top: pass # if car goes too fast
#         if t0 * a0 + vc < 0: pass # if car goes too slow

#         self.periods = (tc, tc + t0, a0), (tf - t1, tf, a1) # set acceleration periods
#         print(self.periods)


#         a, d, t = self.acceleration, -self.acceleration, tf - tc
#         rad = ((2 * a ** 2 * d - 2 * a * d ** 2) * df + (2 * a * d ** 2 - 2 * a ** 2 * d) * dc + a * d * vc ** 2 + 
#               (2 * a * d ** 2 * t - 2 * a * d * vf) * vc + a ** 2 * d ** 2 * t ** 2 - 2 * a ** 2 * d * vf * t + a * d * vf ** 2) ** 0.5
#         vi = (-rad + a * vc + a * d * t - a * vf) / (d - a) # calculate intermediate speed
#         print(vi)

#         if vi >= vc:
#             p0 = (tc, tc + (vi - vc) / a, a) # accelerate to intermediate speed
#             p1 = (tf - (vf - vi) / d, tf, d) # decelerate to final speed
#         if vi <= vc:
#             p0 = (tc, tc + (vi - vc) / d, d) # decelerate to intermediate speed
#             p1 = (tf - (vf - vi) / a, tf, a) # accelerate to final speed
#         print(p0, p1)
#         if p0[1] > p1[0]: p0, p1 = (p0[0], p1[0], p0[2]), (p0[1], p1[1], p1[2])
#         print(p0, p1)
#         self.periods = p0, p1

        # t, a = tf - tc, a
        # ti = ((4 * a * dc - 4 * a * df + a ** 2 * t ** 2 + 4 * a * vc * t) ** 0.5 + a * t) / (2 * a)