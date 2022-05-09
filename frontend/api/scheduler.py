import sys
import json

sys.path.append('backend')
import Intersection
import Car

intersection = Intersection.Intersection()
car0 = Car.Car(0, -200, (2, 2))
car0.setCourse(0, 10, 30)
car1 = Car.Car(1, -200, (0, 1))
car1.setCourse(0, 8, 30)
intersection.cars.append(car0)
intersection.cars.append(car1)

print("Ready for Input!", file=sys.stdout, flush=True)
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

