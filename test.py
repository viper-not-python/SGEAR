from tcping import Ping
ping = Ping('192.168.170.1', 80, 1)
try:
    ping.ping(1)
    status = True
except:
    status = False

print(status)