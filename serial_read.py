import serial
import time
import math


tries = 0

try:
    SerialIn = serial.Serial("/dev/ttyUSB0",9600)
    ser = True
    print("ser = true")
except Exception as e:
    ser = False
    print("ser = false")
    print(e)

def get_data(type_):
    data = SerialIn.readline()
    data = data.decode()
    
    if type_ == "str":
        return data
    if type_ == "int":
        data = int(data)
        return data

def try_voltage():
    voltage = get_data("str")[0:4]
    voltage = voltage[0:2] + "." + voltage [2:4]
    battery_status = voltage + " V"
    with open("serial/voltage.txt", "w") as v:    #battery_voltage
        v.write(battery_status)

def try_distance():
    dta = get_data("str")
    i1 = dta.find("u") + 1
    i2 = dta.find("x")
    distance_str = dta[i1:i2]
    distance = int(distance_str)
    distance_str = distance_str + "cm"
    if distance == 0:
        distance_str = "error"
    with open("serial/distance.txt", "w") as d:    #distance
        d.write(distance_str)

def try_x():
    global x
    dta = get_data("str")
    i1 = dta.find("x") + 1
    i2 = dta.find("y")
    x = dta[i1:i2]

def try_y():
    global y
    dta = get_data("str")
    i1 = dta.find("y") + 1
    i2 = dta.find("z")
    y = dta[i1:i2]

def try_z():
    global z
    dta = get_data("str")
    i1 = dta.find("z") + 1
    i2 = dta.find("X")
    z = dta[i1:i2]

def try_X():
    global X
    dta = get_data("str")
    i1 = dta.find("X") + 1
    i2 = dta.find("Y")
    X = dta[i1:i2]

def try_Y():
    global Y
    dta = get_data("str")
    i1 = dta.find("Y") + 1
    i2 = dta.find("Z")
    Y = dta[i1:i2]

def try_Z():
    global Z
    dta = get_data("str")
    i1 = dta.find("Z") + 1
    i2 = dta.find("e")
    Z = dta[i1:i2]

def xyz(x, y, z):
    with open("serial/z.txt", "w") as z__:    #z
        z__.write(z)

def xyo(x, y, o):
    with open("matrix/xyo.txt", "w") as xyo:    #xyo
        xyo_ = f"{x},{y},{o}"
        xyo.write(xyo_)

while True:
    if ser == True:
            try:
                try_voltage()            
                try_distance()            
                try_x()            
                try_y()            
                try_z()            
                try_X()     #acc            
                try_Y()     #acc
                try_Z()     #acc

                xyz(x, y, z)

                x_ = 1
                y_ = 1
                o = 1
                xyo(x_, y_, o)
            
            except:
                ser = False


    else:
        tries = tries + 1
        if tries == 11:
            print("disconnected")
            break
        print(f"trying again {tries} / 10")
        ser = True
        
