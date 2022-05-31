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

# this test fail because we currently don't support the car speed of zero
intersection.schedule(Car.Car(0, -300, 0, (1, 3)))

# main loop
period, speed = 30, 3
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()