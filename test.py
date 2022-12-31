import cv2
import time

while True:
    try:
        frame = cv2.imread("stream.jpg")
        cv2.imshow("1", frame)
    except:
        pass
    time.sleep(0.01)
    if (cv2.waitKey(1)==ord("q")):
        break