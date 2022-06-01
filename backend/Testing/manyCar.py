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
intersection = Intersection.Intersection(0, 0)

# this test fail because of known bug
for i in range(4):
    for k in range(20):
        for j in range(2):
            intersection.schedule(Car.Car(0, -300 - j * 10 - k * 20, 30, (i, (i + j) % 4)))
            intersection.schedule(Car.Car(0, -300 - j * 10 - k * 20 - 5, 30, (i, (i + j + 2) % 4)))

# main loop
period, speed = 30, 3
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()