import numpy as np
import multiprocessing as mp
import math
import time
import pickle

x_cords = 5000    #setting amount x cords
y_cords = 5000    #setting amount y cords
l = 0
i = 0

start = time.time()
cord = [[0 for x_ in range(x_cords)] for y_ in range(y_cords)]    #creating array
end = time.time()
t0 = end-start
print(f"array created after: {t0}seconds")

while True:
    with open("matrix/xyo.txt", "r") as xy:
        c = xy.read()
        cmr = c.find(",")
        cmr1 = c[cmr+1:].find(",") + cmr + 1
        x = int(c[0:cmr])
        y = int(c[cmr+1:cmr1])
        o = int(c[cmr1+1:])
        cord[x][y] = o
    with open("matrix/map.txt", "wb") as map_:
        try:
            pickle.dump(cord, map_)
        except:
            pass
    time.sleep(1)







#start = time.time()
#for xx in range(0, x_cords):
#    for yy in range(0, y_cords):
#        cord[xx][yy] = 1


#    end = time.time()
#    t1 = end-start
#    print(f"{i}: {t1}")
#    print(f"l: {l}")