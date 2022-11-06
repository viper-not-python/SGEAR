import datetime
time_then = None


while True:
    time_now = str(datetime.datetime.now())
    time_now = time_now[11:22]
    #print(time_now)
    if time_now[:-1] != time_then:
        print(time_now)

    time_then = time_now[:-1]