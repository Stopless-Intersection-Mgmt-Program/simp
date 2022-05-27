import sys
import json

sys.path.append('../../backend')
import Intersection
import TrafficLight

intersection = None

while True:
    if sys.stdin != None:
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break

            # Read In
            dicIn = json.loads(line) # read the json into a dictionary
            if intersection is None:
                if "once" not in dicIn: exit() # exit if there is no intersection data
                onceProps = dicIn["once"]
                algorithm = onceProps["algorithm"] # extract algorithm
                if algorithm == "First Come First Served": intersection = Intersection.Intersection(0, 0)
                elif algorithm == "Traffic Light": intersection = TrafficLight.TrafficLight(0, 0)
                elif algorithm == "Round Robin (Beta)": intersection = Intersection.Intersection(0, 0)
                else: exit() # terminate if algorithm is not one of these
                intersection.layout = onceProps["layout"] # set layout
            
            if "continuous" not in dicIn: exit() # there should be continuous data each tick
            continuousProps = dicIn["continuous"] # read data into dictionary and assign values
            playSpeed = continuousProps["playSpeed"]
            intersection.spawn = continuousProps["spawnRate"]
            intersection.speed = continuousProps["speedLimit"]
            intersection.buffer = continuousProps["buffer"]
            
            # Write Out
            intersection.tick(20 * playSpeed) # tick the intersection
            dicOut = intersection.render() # get render values
            print(json.dumps(dicOut))

        print("Done", file=sys.stdout, flush=True)