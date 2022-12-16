import pickle
import time
from matplotlib import pyplot

def close_event():
    pyplot.close()

pyplot.figure(figsize=(5,5))
fig = pyplot.figure(figsize=(5,5))
timer = fig.canvas.new_timer(interval = 3000) #creating a timer object and setting an interval of 3000 milliseconds
timer.add_callback(close_event)


while True:
    try:
        with open("matrix/map.txt", 'rb') as f:
            cord = pickle.load(f)
            pyplot.imshow(cord)
            timer.start()
            pyplot.show()
    except:
        pass  