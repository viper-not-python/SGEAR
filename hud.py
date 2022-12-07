import cv2
import numpy as np
import datetime
import math
#import pyaudio
#import struct
#import RPi.GPIO as GPIO
#from scipy.fftpack import fft
import time

#python setup
#subprocess.run("python serial_read.py", shell=True)

#video setup
width = 1280
height = 660

width = 640
height = 420

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
    sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])    
    frame = cv2.filter2D(frame, ddepth=-1, kernel=sharpen_filter)

    return frame

def get_distance():
    with open("serial/distance.txt", "r") as d:
        dist = d.read()
    return dist

def get_battery():
    with open("serial/voltage.txt", "r") as v:
        bat_stat = v.read()
    return bat_stat
    

while True:
    ret, frame = stream.read()
    frame = cv2.resize(frame, (width, height))

    #with open("sound.txt", "r") as sound:
    #    s = sound.read()
    #    if s == "sound":
    #        soundmeter()
    #    else:
    #        pass

    time_then = time_now

    #if view_pic == True:
    #    try:
    #        pic = cv2.imread("pic/pic.png")
    #        pic = cv2.cvtColor(pic, cv2.COLOR_BGR2BGRA)
    #        pic = cv2.resize(pic, (426, 240))
    #        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    #        frame_h, frame_w, frame_c = frame.shape
    
    #        overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
    #        pic_h, pic_w, pic_c = pic.shape
    #        for i in range(0, pic_h):
    #            for j in range(0, pic_w):
    #                if pic[i,j][3] != 0:
    #                    offset = 10
    #                    h_offset = frame_h - pic_h - offset
    #                    w_offset = frame_w - pic_w - offset
    #                    overlay[h_offset + i, w_offset+ j] = pic[i,j]

    #        cv2.addWeighted(overlay, 1, frame, 0.25, 0, frame)

    #        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
    #    except:
    #        pass

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
    
    with open("serial/xyz.txt", "r") as xyz_:
        xyz = xyz_.read()
        c1 = xyz.find(",")
        c2 = xyz[c1 + 1:].find(",") + c1
        #x = float(xyz[0:c1])
        #y = float(xyz[c1+1:c2+1])
        z = xyz[c2+2:]
        try:
            z = float(z)
            z_ = z * -1
            z = z_+ 180
            draw_line(320, 220, z_, 200, 1, 0, 255, 0)
            draw_line(320, 220, z, 200, 1, 0, 255, 0)
        except:
            pass        

    #with open ("status.txt", "r") as status:
    #    stat = status.read()
    #    if stat == "stream":
    #        view_pic = False
    #    if stat == "pic":
    #        view_pic = True

    

    frame = cv2.resize(frame, (510, 382))
    cv2.imshow("", frame)
    
    if (cv2.waitKey(1)==ord("q")):
        break

stream.release()
cv2.destroyAllWindows()
#GPIO.cleanup()