import serial

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


while True:
    if ser == True:
            try:
                try_voltage()            
                try_distance()                        
            except:
                ser = False


    else:
        tries = tries + 1
        if tries == 11:
            print("disconnected")
            break
        print(f"trying again {tries} / 10")
        ser = True
        
