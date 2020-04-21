import sys

def getUserInput(message, dtype=str):
    print(message, end=" > ", flush=True)
    reply = sys.stdin.readline().strip()
    try:
        reply = dtype(reply)
        return reply
    except ValueError as e:
        ddve = DDValueError(e)
        ddve.warn()

def getUserSelection(message, choiceslist, default=None):
    for x in range(len(choiceslist) ):
        print("%i : %s" % (x+1, choiceslist[x]))

    if default != None:
        choice = int(default)
    else:
        choice = getUserInput(message, dtype=int)-1

    return choiceslist[choice]
