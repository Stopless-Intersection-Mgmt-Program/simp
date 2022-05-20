import tkinter as tk
import Car
import Intersection
import Traffic
import TrafficLight

# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1000)
canvas.pack()

# sample intersection
# intersection = Intersection.Intersection(0, 1)
intersection = TrafficLight.TrafficLight(0, 1)
# intersection = Traffic.Traffic(0, 1)

# intersection.schedule(Car.Car(0, -300, 30, (3, 2)))
# intersection.schedule(Car.Car(0, -310, 30, (0, 2)))
# intersection.schedule(Car.Car(0, -320, 30, (0, 3)))
# intersection.schedule(Car.Car(0, -330, 30, (0, 2)))
# intersection.schedule(Car.Car(0, -350, 30, (0, 3)))
# intersection.schedule(Car.Car(0, -390, 30, (0, 3)))
# intersection.schedule(Car.Car(0, -400, 30, (0, 2)))



# main loop
period, speed = 20, 5
while True:
    canvas.delete("all")
    intersection.tick(period * speed)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(period)
root.mainloop()