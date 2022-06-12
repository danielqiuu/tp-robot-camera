import socket, cv2, pickle, struct

ip = '192.168.56.1'
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))
data = b""
payload_size = struct.calcsize("Q")
while True:
    while len(data) < payload_size:
        packet = s.recv(4*1024)
        if not packet:
            break
        data += packet
    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("Q", packed_msg_size)[0]
    while len(data) < msg_size:
        data += s.recv(4*1024)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data)
    cv2.imshow("Recieved", frame)    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
s.close