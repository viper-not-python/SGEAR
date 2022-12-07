import multiprocessing as mp
import math
import time

ra = []
rb = []
rc = []

def cal_one(numbers):
    for number in numbers:
        ra.append(math.sqrt(number ** 3))

def cal_two(numbers):
    for number in numbers:
        rb.append(math.sqrt(number ** 4))

def cal_three(numbers):
    for number in numbers:
        rc.append(math.sqrt(number ** 5))

if __name__ == '__main__':
    
    number_list = list(range(50000000))
    
    p1 = mp.Process(target=cal_one, args=(number_list,))
    p2 = mp.Process(target=cal_two, args=(number_list,))
    p3 = mp.Process(target=cal_three, args=(number_list,))
    start = time.time()
    p1.start()
    p2.start()
    p3.start()
    end = time.time()
    t1 = end-start
    print(t1)

    start = time.time()
    cal_one(number_list)
    cal_two(number_list)
    cal_three(number_list)
    end = time.time()
    t2 = end-start
    print(t2)
    print(t2/t1)