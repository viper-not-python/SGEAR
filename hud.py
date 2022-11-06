from pickle import FRAME
from xml.dom import INDEX_SIZE_ERR
import cv2
import numpy as np
import datetime
import math

#video setup
stream = cv2.VideoCapture(0)
width = 1280
height = 720

fontsize = 1

view_pic = False

init = True

#audio setup
CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, output = True, frames_per_buffer = CHUNK)

#methods
def get_master_text():
    try:
        with open ("master_text.txt", "r") as ms:
            text = ms.read()

    except:
        print("permission denied 1")

    try:
        with open ("master_text1.txt", "r") as ms1:
            text1 = ms1.read()
    except:
        print("permission denied 2")

    try:
        with open ("master_text2.txt", "r") as ms2:
            text2 = ms2.read()
    except:
        print("permission denied 3")

    try:
        with open ("master_text3.txt", "r") as ms3:
            text3 = ms3.read()
    except:
        print("permission denied 4")

    l = len(text)
    
    paragraphs = math.ceil(l / 24)

    for i in range(0, paragraphs):
        index = text[25 * (i + 1) :].find(" ")
        index = index + 25 * (i +1)
        index = index +1
        index_short = text[25 * i :].find(" ")
        index_short = index_short + 25 * i
        index_short = index_short +1
        cv2.putText(frame, text[index_short : index], (0, 75 + i * 25), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    cv2.putText(frame, text1, (0, 696), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    cv2.putText(frame, text2, (930, 24), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)
    cv2.putText(frame, text3, (930, 696), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)


def battery_voltage():
    voltage = 11.4
    return voltage

def sharpen(frame):
    sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])    
    frame = cv2.filter2D(frame, ddepth=-1, kernel=sharpen_filter)

    return frame


while True:
    _,frame = stream.read()
    cv2.circle(frame, (320, 950), 500, (0, 155, 0), 2)
    cv2.circle(frame, (320, -470), 500, (0, 155, 0), 2)


    if view_pic == True:
        try:
            pic = cv2.imread("pic/pic.png")
            pic = cv2.cvtColor(pic, cv2.COLOR_BGR2BGRA)
            pic = cv2.resize(pic, (426, 240))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
            frame_h, frame_w, frame_c = frame.shape
    
            overlay = np.zeros((frame_h, frame_w, 4), dtype='uint8')
            pic_h, pic_w, pic_c = pic.shape
            for i in range(0, pic_h):
                for j in range(0, pic_w):
                    if pic[i,j][3] != 0:
                        offset = 10
                        h_offset = frame_h - pic_h - offset
                        w_offset = frame_w - pic_w - offset
                        overlay[h_offset + i, w_offset+ j] = pic[i,j]

            cv2.addWeighted(overlay, 1, frame, 0.25, 0, frame)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        except:
            pass

    frame = cv2.resize(frame, (width, height))

    frame = sharpen(frame)
    
    time = str(datetime.datetime.now())
    time = time[11:22]
    
    cv2.putText(frame, time, (0, 24), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)   #time

    voltage = str(battery_voltage())
    battery_status = voltage + " V"
    cv2.putText(frame, battery_status, (0,50), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 255, 0), 1)   #battery_percentage
    if battery_voltage() <= 10:
        battery_warning = "LOW BATTERY VOLTAGE!"
        cv2.putText(frame, battery_warning, (80,50), cv2.FONT_HERSHEY_SIMPLEX, fontsize, (0, 0, 255), 1)   #battery_percentage_warning

    get_master_text()   #text from hud_master.py
    
    with open ("status.txt", "r") as status:
        stat = status.read()
        if stat == "stream":
            view_pic = False
        if stat == "pic":
            view_pic = True

    cv2.imshow("", frame)
    
    if (cv2.waitKey(1)==ord("q")):
        break

stream.release()
cv2.destroyAllWindows()