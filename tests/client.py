import socket, cv2, pickle, struct, time
import numpy as np

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '192.168.170.208' # paste your server ip address here
port = 9999
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
    try:
        while len(data) < payload_size:
            packet = client_socket.recv(4*1024) # 4K
            if not packet: break
            data+=packet
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q",packed_msg_size)[0]
        
        while len(data) < msg_size:
            data += client_socket.recv(4*1024)
        frame_data = data[:msg_size]
        data  = data[msg_size:]
        frame = pickle.loads(frame_data)
        frame = cv2.resize(frame, (680, 383))
        sharpen_filter = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])    
        frame = cv2.filter2D(frame, ddepth=-1, kernel=sharpen_filter)
        cv2.imshow("FEED",frame)
    except:
        time.sleep(1)
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        host_ip = '192.168.170.36' # paste your server ip address here
        port = 9999
        client_socket.connect((host_ip,port)) # a tuple
        data = b""
        payload_size = struct.calcsize("Q")
    key = cv2.waitKey(1) & 0xFF
    if key  == ord('q'):
        break
client_socket.close()