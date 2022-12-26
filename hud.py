import cv2
import numpy as np
import datetime
import math
#import pyaudio
import struct
#import RPi.GPIO as GPIO 
#from scipy.fftpack import fft
import time
import os
import socket
import pickle
import imutils
from threading import Thread
import requests

#python setup

#subprocess.run("python serial_read.py", shell=True)
#os.system("python serial_read.py &")

#video setup
width = 947
height = 546

stream = cv2.VideoCapture(0)

fontsize = 1

#view_pic = False

##audio setup

#CHUNK = 1024 * 2
#FORMAT = pyaudio.paInt16
#CHANNELS = 1
#RATE = 44100

#p = pyaudio.PyAudio()

#stream_aud = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)

#functions setup
#ch_amount = 128
#ch = CHUNK * 2
#ch_parts = math.floor(ch / ch_amount)
#avrg=[]
#for i in range(0, ch_amount):
#    avrg.append(0)


time_now = str(datetime.datetime.now())
time_now = time_now[11:22]
time_then = None

a = datetime.datetime.now()
time.sleep(0.001)

moved = False

pic = False

c_s = 0

socket_initialized = False
internet = False
checking_internet = False

sending = False

w_custom = 500


#methods
def draw_line(x, y, direction, length, thickness, blue, green, red):
    direction = direction *-1

    alpha = (direction / 180) * math.pi 
    beta = (direction / 180) * math.pi
    cos = math.cos(alpha)
    sin = math.sin(beta)

    cos = round(cos * length)
    sin = round(sin * length)

    cv2.line(frame, (x,y), (cos + x, sin + y), (blue, green, red), thickness)

#def soundmeter():
#    data = stream_aud.read(CHUNK, exception_on_overflow=False)
#    data_int = struct.unpack(str(2 * CHUNK) + 'B', data)
    
#    #y_fft = fft(data_int)
#    #y_fft = np.abs(y_fft[0:CHUNK])
#    #for i in range(0, len(y_fft)):
#    #    with open ("spectrum.log", "a") as sp:
#    #        out = str(f"{i}  :   {y_fft[i]}    ")
#    #        sp.write(out)640
#    #input()

#    if time_now != time_then:
#        for i in range(1, ch_amount+1):
#            avrg[i-1] = round(sum(data_int[(i-1) * ch_parts : i * ch_parts]) / ch_parts)
#            x = 128
#            y = 400
#            multiplier = 0.2
#            length = avrg[i-1] * multiplier
#            draw_line(x + i*3, y, 90, length, 1, 0, 255, 0)

def get_master_text():
    try:
        with open ("cmd/master_text.txt", "r") as ms:
            text = ms.read()

    except:
        print("permission denied 1")

    try:
        with open ("cmd/master_text1.txt", "r") as ms1:
            text1 = ms1.read()
    except:
        print("permission denied 2")

    try:
        with open ("cmd/master_text2.txt", "r") as ms2:
            text2 = ms2.read()
    except:
        print("permission denied 3")

    try:
        with open ("cmd/master_text3.txt", "r") as ms3:
            text3 = ms3.read()
    except:
        print("permission denied 4")

    l = len(text)
    
    paragraphs = math.ceil(l / 14)

    for i in range(0, paragraphs):
        index = text[15 * (i + 1) :].find(" ")
        index = index + 15 * (i +1)
        index = index +1
        index_short = text[15 * i :].find(" ")
        index_short = index_short + 15 * i
        index_short = index_short +1
        cv2.putText(frame, text[index_short : index], (0, 75 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    cv2.putText(frame, text1, (0, 405), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    cv2.putText(frame, text2, (465, 24), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1) #930
    cv2.putText(frame, text3, (465, 405), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)

def sharpen(frame):
    try:
        sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])    
        frame = cv2.filter2D(frame, ddepth=-1, kernel=sharpen_filter)
    except:
        pass

    return frame

def get_distance():
    with open("serial/distance.txt", "r") as d:
        dist = d.read()
    return dist

def get_battery():
    with open("serial/voltage.txt", "r") as v:
        bat_stat = v.read()
    return bat_stat

def mpu():
    #with open("serial/z.txt", "r") as z__:
    #    z = z__.read()
    #    try:
    #        z = float(z)
    #        z_ = z * -1
    #        z = z_+ 180
    #        draw_line(320, 220, z_, 200, 1, 0, 255, 0)
    #        draw_line(320, 220, z, 200, 1, 0, 255, 0)   
    #    except:
    #        pass
    pass
   
def connect():
    global client_socket, addr, connected, trying_to_connect
    client_socket,addr = server_socket.accept()
    connected = True
    trying_to_connect = False

def try_connection():
    global trying_to_connect
    if trying_to_connect == False:
        trying_to_connect = True
        Thread(target=connect).start()
    else:
        pass

def socket_initialize():
    w = int(width / 2)
    h = int(height / 2)
    cv2.putText(frame, "CONNECTING INTERNET", (w,h), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    time.sleep(1)
    global socket_initialized, trying_to_connect, connected, host_name, host_ip, socket_address, port, server_socket
    # Socket Create
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host_name  = socket.gethostname()
    host_ip = '192.168.170.208'

    port = 9999
    socket_address = (host_ip,port)

    # Socket Bind
    server_socket.bind(socket_address)

    # Socket Listen
    server_socket.listen(5)

    connected = False
    trying_to_connect = False
    socket_initialized = True

def is_inet_active(timeout):
    try:
        requests.head("https://google.com", timeout=timeout)
        return True
    except requests.ConnectionError:
        return False


def int_ping():
    global checking_internet, internet

    if is_inet_active(1) == True:
        internet = True
    checking_internet = False

def check_internet():
    global checking_internet
    if checking_internet == False:
        checking_internet == True
        Thread(target=int_ping).start()

#def fps_c(fps, o):
#    fps_change = abs(fps - 10)
#    fps_change = int(0.5 * math.pow(fps_change, 2))
#    #fps_change = 2
#    print(fps, fps_change, o, w_custom)
#    return fps_change


def send():
    global sending, connected, w_custom
    try:
        send_a = datetime.datetime.now()
        client_socket.sendall(message)
        send_b = datetime.datetime.now()
        send_delta = send_b - send_a
        send_delta = float(send_delta.total_seconds())
        if send_delta != 0:
            send_fps = int(1 / send_delta)
            if w_custom < 500:
                if send_fps > 15:
                    w_custom = w_custom + 2
                if send_fps < 15:
                    w_custom = w_custom - 2    
            if w_custom == 500:
                print("reached")
                w_custom = w_custom - 2
        else:
            pass
        
    except:
        connected = False
    sending = False

def thread_send():
    global sending
    sending = True
    Thread(target=send).start()
    

while True:
    ret, frame = stream.read()
    with open ("cmd/status.txt", "r") as status:
        p_status = status.read()
        if p_status == "nopic":
            pic = False
        else:
            pic = True

    if pic == True:
        try:
            frame = cv2.imread(f"/pics/{p_status}.jpg")     #create folder "/pics/" and chmod 777, also samba ==> https://www.youtube.com/watch?v=z2W2jfzIhTI
            try:
                frame = cv2.resize(frame, (640, 420))
            except:
                ret, frame = stream.read()
        except:
            ret, frame = stream.read()
    else:
        frame = cv2.resize(frame, (640, 420))

    #with open("sound.txt", "r") as sound:
    #    s = sound.read()
    #    if s == "sound":
    #        soundmeter()
    #    else:
    #        pass

    time_then = time_now

    with open ("cmd/sharpen.txt", "r") as sharpen_:
        sh = sharpen_.read()
        if sh == "sharpen":
            sharpen_img = False
        if sh == "nosharpen":
            sharpen_img = True
        
    if sharpen_img == True:
        frame = sharpen(frame)
    
    time_now = str(datetime.datetime.now())
    time_now = time_now[11:22]
    
    cv2.putText(frame, time_now, (0, 24), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)   #time

    b = datetime.datetime.now()
    delta = b - a
    delta = float(delta.total_seconds())

    fps = int(1 / delta)
    fps_str = str(fps) + "fps"
    cv2.putText(frame, fps_str, (225,24), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    
    a = datetime.datetime.now()

    battery_status = get_battery()
    distance = get_distance()
    cv2.putText(frame, battery_status, (0,50), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    cv2.putText(frame, distance, (350,24), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)

    
    get_master_text()   #text from hud_master.py
    
    mpu()   
    
    frame = cv2.resize(frame, (width, height))
    cv2.imshow("1", frame)
    cv2.imshow("2", frame)

    if moved == False:
        cv2.moveWindow("1", -250, 100)
        cv2.moveWindow("2", 1280+500, 100)
        moved = True
    else:
        pass
    
    if internet == False:
        check_internet()

    if internet == True and socket_initialized == False:
        socket_initialize()
        socket_initialized = True

    if socket_initialized == True:
        frame = imutils.resize(frame,width=w_custom)
        var_a = pickle.dumps(frame)
        message = struct.pack("Q",len(var_a))+var_a
        if connected == True:
            try:
                if sending == False:
                    thread_send()
            except:
                connected = False
        else:
            try_connection()

    print(w_custom)
    if (cv2.waitKey(1)==ord("q")):
        break

stream.release()
cv2.destroyAllWindows()
#client_socket.close()
#GPIO.cleanup()