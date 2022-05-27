import sys
import json

sys.path.append('../../backend')
import Intersection

intersection = Intersection.Intersection(0,1)
intersectionProps = None

while True:
    if sys.stdin != None:
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break
            # Read In
            dicIn = json.loads(line)
            if intersectionProps is None:
                intersectionProps = dicIn["intersection"]
            
            # Write Out
            intersection.tick(35)
            dicOut = {"cars" : intersection.render()}
            print(json.dumps(dicOut))

        print("Done", file=sys.stdout, flush=True)

