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

intersection.schedule(Car.Car(0, -300, 30, (0, 3)))

# main loop
period, speed = 30, 3
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()