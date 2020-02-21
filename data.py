from json import load, dump
import atexit
with open("rawData.json", 'r') as f:
    data = load(f)
class Facts():
    train = data[0]
    planet = data[1]
    medical = data[2]
@atexit.register
def onExit():
    print("Saving..")
    with open("rawData.json", 'w') as f:
        dump(data, f, indent=4, sort_keys=True)
@atexit.register
def sortData():
    for i in range(len(data)):
        data[i] = sorted(data[i], key = lambda i: i["score"],reverse=True)