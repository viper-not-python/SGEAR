import serial

try:
    SerialIn = serial.Serial("/dev/ttyUSB0",9600)
    ser = True
except:
    ser = False

def get_data(type_):
    data = SerialIn.readline()
    data = data.decode()
    
    if type_ == "str":
        return data
    if type_ == "int":
        data = int(data)
        return data

while True:
    if ser == True:
            try:
                voltage = get_data("str")[0:4]
                voltage = voltage[0:2] + "." + voltage [2:4]
                battery_status = voltage + " V"
                with open("serial/voltage.txt", "w") as v:    #battery_voltage
                    v.write(battery_status)
            except:
                ser = False

            try:
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
            except:
                ser = False
    else:
        try:
            SerialIn = serial.Serial("/dev/ttyUSB0",9600)
            ser = True
        except:
            ser = False
