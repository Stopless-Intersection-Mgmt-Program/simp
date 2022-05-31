import sys
sys.path.append('..')

import tkinter as tk
import Car
import Intersection
import TrafficLight

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1000)
canvas.pack()

# sample intersection
intersection = TrafficLight.TrafficLight(0, 0)

# traffic light work for right turn and straight, so the following test should work, but it failed.
for i in range(4):
    for j in range(4):
        if (i - j + 4) % 4 != 1 and i != j:
            intersection.schedule(Car.Car(0, -300 - j * 10, 30, (i, j)))

# main loop
period, speed = 30, 3
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()