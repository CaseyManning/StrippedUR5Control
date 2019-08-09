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

    print("Robot starts Moving to 3 positions based on joint positions")

    s.send(b"movej([-1.95, -1.58, 1.16, -1.15, -1.55, 1.18], a=1.0, v=0.1)" + b"\n")
    time.sleep(10)
    print("reached 1")

    s.send(b"movej([-1.95, -1.66, 1.71, -1.62, -1.56, 1.19], a=1.0, v=0.1)" + b"\n")
    time.sleep(10)
    print("reached2")

    s.send(b"movej([-1.96, -1.53, 2.08, -2.12, -1.56, 1.19], a=1.0, v=0.1)" + b"\n")
    time.sleep(10)
    print("reached 3")

    print("Robot starts Moving to 3 positions based on pose positions")

    s.send(b"movej(p[0.00, 0.3, 0.4, 2.22, -2.22, 0.00], a=1.0, v=0.1)" + b"\n")
    time.sleep(10)
    print("reached 1")

    s.send(b"movej(p[0.00, 0.3, 0.3, 2.22, -2.22, 0.00], a=1.0, v=0.1)" + b"\n")
    time.sleep(10)
    print("reached 2")

    s.send(b"movej(p[0.00, 0.3, 0.2, 2.22, -2.22, 0.00], a=1.0, v=0.1)" + b"\n")
    time.sleep(10)
    print("reached 3")

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