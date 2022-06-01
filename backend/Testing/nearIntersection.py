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

# this test will fail because the car is spawned at position larger than -150, which our algorithm doesn't support
# yet, although the initial speed of it allows it to pass without collision.
for i in range(4):
    for j in range(4):
        for k in range(3):
            intersection.schedule(Car.Car(0, -30 - k * 10 - j * 30, 1, (i, j)))

# main loop
period, speed = 30, 3
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()