import sys
import json

sys.path.append('../../backend')
import Intersection
import Car
import TrafficLight

def xyToDist(interLength, x, y, inRoad, layout):
    # this would depend on the layout of road, will we have road other than origin one?
    # if layout == ...
    if inRoad == 0: return x - interLength / 2
    if inRoad == 1: return y - interLength / 2
    if inRoad == 2: return - x - interLength / 2
    if inRoad == 3: return -y - interLength / 2
    return # to be implement

print("Ready for Input!", file=sys.stdout, flush=True)
intersectionProps = ""
pause = False
while True:
    if sys.stdin != None:
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break
            # print(f'Read from stdin: {line}', file=sys.stdout, flush=True)

            # Read In
            dicIn = json.loads(line)
            if "intersection" in dicIn and dicIn["intersection"] != intersectionProps:
                intersectionProps = dicIn["intersection"] 
                if intersectionProps[3] == "trafficlight":
                    intersection = TrafficLight.TrafficLight()
                else:
                    intersection = Intersection.Intersection()
            if "cars" in dicIn:
                cars = dicIn["cars"]
                for car in cars:
                    carNew = Car.car(car[0], xyToDist(intersectionProps[0], car[1], car[2], car[3], intersectionProps[1]), (car[3], car[4])) # ipc format need transfer xy to dist
                    # carNew = Car.Car(car[0], car[1], (car[2], car[3]))
                    intersection.schedule(carNew)
            
            if "pause" in dicIn:
                pause = dicIn["pause"]

            # Write Out
            if not pause:
                intersection.tick(10)
                if intersectionProps[3] == "trafficlight":
                    stop = []
                    clear = []
                    for i in range(len(intersection.lights)):
                        if intersection.lights[i] > 0: clear.append(i)
                        else: stop.append(i)
                    dicOut = {"cars" : intersection.render(), "statistics": [], "intersection": [stop, clear]}
                else:
                    dicOut = {"cars" : intersection.render(), "statistics": []} # do it need car's speed here? (ipc format)
                print(json.dumps(dicOut))

        print("Done", file=sys.stdout, flush=True)


# below is signal version, don't use
# import sys
# import json

# sys.path.append('../../backend')
# import Intersection
# import Car

# import time
# import sys
# from select import select

# # intersection = Intersection.Intersection()
# # car0 = Car.Car(0, -200, (2, 2))
# # car0.setCourse(0, 10, 30)
# # car1 = Car.Car(1, -200, (0, 1))
# # car1.setCourse(0, 8, 30)
# # intersection.cars.append(car0)
# # intersection.cars.append(car1)

# def xyToDist(interLength, x, y, inRoad, layout):
#     # this would depend on the layout of road, will we have road other than origin one?
#     # if layout == ...

#     return # to be implement

# print("Ready for Input!", file=sys.stdout, flush=True)
# intersectionProps = ""
# timeout = 0.5
# intersection = Intersection.Intersection()
# pause = False

# while True:
#     rlist, _, _ = select([sys.stdin], [], [], timeout)
#     if rlist:
#         line = sys.stdin.readline()
#         if 'Exit' == line.rstrip():
#             break
#         # print(f'Read from stdin: {line}', file=sys.stdout, flush=True)

#         # Read In
#         dicIn = json.loads(line)
#         if "intersection" in dicIn and dicIn["intersection"] != intersectionProps:
#             intersectionProps = dicIn["intersection"] # if scenario == "trafficlight": ...
#             intersection = Intersection.Intersection()
#         if "cars" in dicIn:
#             cars = dicIn["cars"]
#             for car in cars:
#                 # carNew = Car.car(car[0], xyToDist(intersectionProps[0], car[1], car[2], car[3], intersectionProps["layout"]), (car[3], car[4])) # ipc format need transfer xy to dist
#                 carNew = Car.Car(car[0], car[1], (car[2], car[3]))
#                 intersection.schedule(carNew)

        
#         if "pause" in dicIn and dicIn[pause] == True:
#             pause = True

#         # Write Out
#         if not pause:
#             intersection.tick(10)
#             dicOut = {"cars" : intersection.render(), "statistics": []} # do it need car's speed here? (ipc format)
#             print(json.dumps(dicOut))
#     else:
#         if not pause:
#             intersection.tick(10)
#             dicOut = {"cars" : intersection.render(), "statistics": []} # do it need car's speed here? (ipc format)
#             print(json.dumps(dicOut))








# # https://www.cnblogs.com/iamlehaha/articles/6790700.html
# # https://www.zhihu.com/question/41737790
# # https://stackoverflow.com/questions/3471461/raw-input-and-timeout