import tkinter as tk
import Car
import Intersection
import TrafficLight

# test code
# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=600, width=1000)
canvas.pack()


# sample intersection and cars
intersection = Intersection.Intersection(True)
# intersection = TrafficLight.TrafficLight()

# car0 = Car.Car(0, -320, (2, 2))
# car1 = Car.Car(1, -330, (3, 2))
# car2 = Car.Car(2, -340, (0, 2))
# car3 = Car.Car(3, -350, (0, 3))
# intersection.schedule(car0)
# intersection.schedule(car1)
# intersection.schedule(car2)
# intersection.schedule(car3)

# car0 = Car.Car(0, -300, (0, 2))
# for t in [x * 0.01 for x in range(500, 1000)]:
#     if car0.setCourse(0, t, 50) != None: print(t, car0.atTime(t))
#     else: print(t, None)
# print(car0.courseRanges(0, 50))
# exit()


# main loop
period = 20
while True:
    canvas.delete("all")
    intersection.tick(period)
    intersection.tkrender(canvas, 2)
    canvas.update()
    root.after(period)
root.mainloop()