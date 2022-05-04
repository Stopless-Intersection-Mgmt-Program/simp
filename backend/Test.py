import tkinter as tk
import Car
import Intersection
import TrafficLight

# test code
# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1200)
canvas.pack()


# sample intersection and cars
intersection = Intersection.Intersection(0)
# intersection = TrafficLight.TrafficLight()

# spawn cars
car0 = Car.Car(0, -200, (1, 3))
car1 = Car.Car(1, -240, (1, 3))
car2 = Car.Car(2, -200, (7, 1))
car3 = Car.Car(3, -250, (1, 3))
car4 = Car.Car(4, -220, (5, 7))
car5 = Car.Car(5, -240, (7, 1))
car6 = Car.Car(6, -250, (5, 7))
car7 = Car.Car(7, -260, (1, 3))
car8 = Car.Car(8, -260, (7, 7))
car9 = Car.Car(9, -230, (3, 7))

# schedule cars
intersection.schedule(car0)
intersection.schedule(car1)
intersection.schedule(car2)
intersection.schedule(car3)
intersection.schedule(car4)
intersection.schedule(car5)
intersection.schedule(car6)
intersection.schedule(car7)
intersection.schedule(car8)
intersection.schedule(car9)


# main loop
while True:
    canvas.delete("all")
    intersection.tick(20)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(20)
root.mainloop()