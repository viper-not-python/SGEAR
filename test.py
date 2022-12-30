import subprocess

try:
    subprocess.check_output(["ping", "-c", "1", "192.168.170.1"])
    status = True
except:
    status = False

print(status)