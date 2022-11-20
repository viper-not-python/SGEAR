import datetime
i = 0
#while True:
    
#    #fps_time_now = int(str(datetime.datetime.now())[11:23])
#    #fps_time_diff = int(str(datetime.datetime.now())[11:23])
    
    
#    print(type(datetime.datetime.now()))
while i < 5:
    a = datetime.datetime.now()
    b = datetime.datetime.now()
    delta = b - a
    delta = float(delta.total_seconds())

    fps = 1 / delta

    print(f"delta: {delta} fps: {fps}")
    i = i+1