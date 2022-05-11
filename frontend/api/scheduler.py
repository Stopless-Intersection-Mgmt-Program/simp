import sys
import json

sys.path.append('../../backend')
import Intersection
import Car

intersection = Intersection.Intersection()
car0 = Car.Car(0, -200, (0, 1))
car1 = Car.Car(1, -240, (0, 1))
car2 = Car.Car(2, -200, (3, 0))
car3 = Car.Car(3, -250, (0, 1))
car4 = Car.Car(4, -220, (2, 3))
car5 = Car.Car(5, -240, (3, 0))
car6 = Car.Car(6, -250, (2, 3))
car7 = Car.Car(7, -260, (0, 1))
car8 = Car.Car(8, -260, (3, 3))
car9 = Car.Car(9, -230, (1, 0))

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

#print("Ready for Input!", file=sys.stdout, flush=True)
while True:
    if sys.stdin != None:
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break
            # print(f'Read from stdin: {line}', file=sys.stdout, flush=True)

            # Read In
            dicIn = json.loads(line)
            intersectionProps = dicIn["intersection"]
            
            # Write Out
            intersection.tick(10)
            dicOut = {"cars" : intersection.render()}
            print(json.dumps(dicOut))

        print("Done", file=sys.stdout, flush=True)

