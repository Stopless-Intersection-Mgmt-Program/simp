import math
import tkinter as tk


class Car:
    # all values are in SI units (meters, meters per second, etc.)
    def __init__(self, id, x, y, s, d):
        self.id = id

        # render properties
        self.l = 4
        self.w = 2
        self.c = "blue"

        # positional properties
        self.x = x
        self.y = y
        self.s = s
        self.d = math.radians(d)

        # controllable properties
        self.a = 0
        self.t = 0

    def control(self, a, t):
        # the only controllable factors are acceleration and turning radius
        self.a = a
        self.t = t

    def tick(self, period):
        # period is in ms, so adjust time-varying values
        self.s += self.a * (period / 1000)
        self.d += self.s * (period / 1000) / self.t if self.t != 0 else 0
        self.x += self.s * (period / 1000) * math.cos(self.d)
        self.y += self.s * (period / 1000) * math.sin(self.d)

    def render(self, canvas, scale):
        # scale value represents how many pixels per meter
        ps = []
        for sl, sw in [(1, 1), (-1, 1), (-1, -1), (1, -1)]:
            # generate base points
            bx, by = self.x + sl * self.l / 2, self.y + sw * self.w / 2

            # rotate points depending on direction
            px = self.x + math.cos(self.d) * (bx - self.x) - math.sin(self.d) * (by - self.y)
            py = self.y + math.sin(self.d) * (bx - self.x) + math.cos(self.d) * (by - self.y)

            # scale and translate points relative to center
            ps.append(int(canvas.cget("width")) / 2 + px * scale)
            ps.append(int(canvas.cget("height")) / 2 - py * scale)

        return canvas.create_polygon(ps, fill=self.c, width=2, outline=self.c)



# create window and canvas
root = tk.Tk()
root.title("SIMP Simulator")
canvas = tk.Canvas(root, bg="grey15", height=400, width=800)
canvas.pack()

# sample driver code
car = Car(0, -20, -5, 0, 0)
car.control(3.5, 10)
while True:
    canvas.delete("all")
    car.tick(10) # <== this value is the same...
    car.render(canvas, 10)
    canvas.update()
    root.after(10) # <== ...as this value
root.mainloop()