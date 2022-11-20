import cv2
stream = cv2.VideoCapture(0)

width = 1280
height = 660

while True:
    ret, frame = stream.read()
    frame = cv2.resize(frame, (width, height))

    cv2.imshow("", frame)
    
    if (cv2.waitKey(1)==ord("q")):
        break

stream.release()
cv2.destroyAllWindows()