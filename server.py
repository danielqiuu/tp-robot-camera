import socket, cv2, pickle, struct


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = 12345

ip = socket.gethostbyname(socket.gethostname())
host_address = (ip, port)
s.bind(host_address)
s.listen(5)
print("Socket is listening for connections at %s:%s" %(host_address[0], host_address[1]))

while True:
    conn, addr = s.accept() # accept socket connection from client
    print("Received connection from", addr)
    if conn: # if connection is recieved from client
        camera = cv2.VideoCapture(0) # initialize webcam using cv2
        while(camera.isOpened()): # loop while camera is open
            _, frame = camera.read() # camera.read() returns a success flag and the video frame
            a = pickle.dumps(frame) # converts video frame to byte stream
            message = struct.pack("Q", len(a)) + a # return 8 byte object 
            conn.sendall(message)
            cv2.imshow('Transmitting Video', frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                conn.close()
    