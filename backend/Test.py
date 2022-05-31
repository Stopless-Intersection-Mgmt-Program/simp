import tkinter as tk
import Intersection
import TrafficLight
import RoundRobin

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1000)
canvas.pack()

# sample intersection
intersection = Intersection.Intersection(0, 1.5)
# intersection = TrafficLight.TrafficLight(0, 1.5)
# intersection = RoundRobin.RoundRobin(0, 1)

# main loop
period, speed = 30, 3
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    print(intersection.render())
    root.after(period)
root.mainloop()