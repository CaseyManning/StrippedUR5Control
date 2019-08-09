# Echo client program
import socket
import time
HOST = "172.16.132.128" # The remote host
PORT = 30002 # The same port as used by the server

print("Starting Program")

count = 0

while (count < 1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    time.sleep(0.5)
    print("sleep finished")

    print("Set output 1 and 2 high")

    s.send(b"set_digital_out(1,True)" + b"\n")
    time.sleep(0.1)

    s.send(b"set_digital_out(2,True)" + b"\n")
    time.sleep(2)

    s.send(b"movel([0.2,0.3,0.5,0,0,3.14], a=1.2, v=0.25, t=0, r=0)" + b"\n")
    time.sleep(10)
    print("finished moving")

    print("Set output 1 and 2 low")

    s.send(b"set_digital_out(1,False)" + b"\n")
    time.sleep(0.1)

    s.send(b"set_digital_out(2,False)" + b"\n")
    time.sleep(0.1)

    count = count + 1
    print("The count is:", count)

    print("Program finish")

    time.sleep(1)
    data = s.recv(1024)

    s.close()
    print("Received", repr(data))

print("Status data received from robot")