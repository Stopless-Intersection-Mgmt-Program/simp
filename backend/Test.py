import tkinter as tk
import Car
import Intersection
import TrafficLight
import RR

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1000)
canvas.pack()

# sample intersection
intersection = RR.RR(0, 10)
# intersection = Intersection.Intersection(0, 10)

# 29.999999999999538 (1, 3) 
# 31.639999999999503 (1, 3)
# 31.959999999999496 (2, 0)
# 32.11999999999949 (3, 0)
# 32.83999999999948 (1, 2)
# 32.919999999999476 (1, 3)
# 34.15999999999945 (3, 3)
# 34.95999999999943 (2, 3)
# 35.15999999999943 (0, 3)

# intersection.schedule(Car.Car(0, -intersection.radius, intersection.speed, (1, 3)))
# for i in range(40):
#     intersection.tick(40)
# intersection.schedule(Car.Car(1, -intersection.radius, intersection.speed, (1,3)))
# for i in range(9):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (2,0)))
# for i in range(6):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (3,0)))
# for i in range(18):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (1,2)))
# for i in range(2):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (1,3)))
# for i in range(31):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (3,3)))
# for i in range(20):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (2,3)))
# for i in range(5):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (0,3)))
# for i in range(3):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (0,1)))
# for i in range(24):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (2,0)))
# for i in range(7):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (3,1)))
# for i in range(54):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (3,1)))
# for i in range(44):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (3,0)))
# for i in range(16):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (1,3)))
# for i in range(7):
#     intersection.tick(40)
# intersection.schedule(Car.Car(2, -intersection.radius, intersection.speed, (3,0)))
# intersection = TrafficLight.TrafficLight()

# main loop
period, speed = 20, 2
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()