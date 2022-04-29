import tkinter as tk
import Car as c
import Intersection as i
import TrafficLight as tl

# test code
# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=800, width=1600)
canvas.pack()


# # sample intersection and cars
intersection = i.Intersection(0, 40)
intersection = tl.TrafficLight(40)

# spawn cars
car0 = c.Car(0, -200, (1, 3))
car1 = c.Car(1, -240, (1, 3))
car2 = c.Car(2, -200, (7, 1))
car3 = c.Car(3, -250, (1, 3))
car4 = c.Car(4, -220, (5, 7))
car5 = c.Car(5, -240, (7, 1))
car6 = c.Car(6, -250, (5, 7))
car7 = c.Car(7, -260, (1, 3))

# schedule cars
intersection.schedule(car0)
intersection.schedule(car1)
intersection.schedule(car2)
intersection.schedule(car3)
intersection.schedule(car4)
intersection.schedule(car5)
intersection.schedule(car6)
intersection.schedule(car7)


# main loop
while True:
    canvas.delete("all")
    intersection.tick(20)
    intersection.tkrender(canvas, 4)
    canvas.update()
    root.after(20)
root.mainloop()