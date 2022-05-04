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
# car0 = Car.Car(0, -200, (0, 1))
# car1 = Car.Car(1, -240, (0, 1))
# car2 = Car.Car(2, -200, (3, 0))
# car3 = Car.Car(3, -250, (0, 1))
# car4 = Car.Car(4, -220, (2, 3))
# car5 = Car.Car(5, -240, (3, 0))
# car6 = Car.Car(6, -250, (2, 3))
# car7 = Car.Car(7, -260, (0, 1))
# car8 = Car.Car(8, -260, (3, 3))
# car9 = Car.Car(9, -230, (1, 3))

# # schedule cars
# intersection.schedule(car0)
# intersection.schedule(car1)
# intersection.schedule(car2)
# intersection.schedule(car3)
# intersection.schedule(car4)
# intersection.schedule(car5)
# intersection.schedule(car6)
# intersection.schedule(car7)
# intersection.schedule(car8)
# intersection.schedule(car9)


car0 = Car.Car(0, -200, (0, 1))
car0.setCourse(0, 3, 30)
print(car0.course)
intersection.cars.append(car0)



# main loop
while True:
    canvas.delete("all")
    intersection.tick(20)
    intersection.tkrender(canvas, 3)
    canvas.update()
    root.after(20)
root.mainloop()