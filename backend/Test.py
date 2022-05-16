import tkinter as tk
import Intersection
import TrafficLight

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1000)
canvas.pack()

# sample intersection
intersection = Intersection.Intersection(0, 10)
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