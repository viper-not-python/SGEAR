from pythonping import ping

#if 'Reply' in ping('192.168.170.1', timeout=1):
#    status = True
#else:
#    status = False


try:
    response_list = ping('args.spdns.org', count = 1)

    if response_list.rtt_avg_ms > 800:
        status = False
    else:
        status = True
except:
    status = False

print(status)