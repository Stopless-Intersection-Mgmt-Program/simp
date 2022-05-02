import sys
print("Ready for Input!", file=sys.stdout, flush=True)
while True:
    if sys.stdin != None:
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break
            print(f'Read from stdin: {line}', file=sys.stdout, flush=True)
        print("Done", file=sys.stdout, flush=True)

