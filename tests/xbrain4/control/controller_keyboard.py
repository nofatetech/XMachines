import socket
import json
import sys
import termios
import tty
import time

# TARGET = ("192.168.1.50", 9999)  # machine IP
TARGET = ("0.0.0.0", 9999)  # machine IP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

linear = 0.0
angular = 0.0
STEP = 0.1

def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

print("W/S = forward/back | A/D = turn | X = stop | Q = quit")

while True:
    key = get_key()

    if key == "w":
        linear += STEP
    elif key == "s":
        linear -= STEP
    elif key == "a":
        angular += STEP
    elif key == "d":
        angular -= STEP
    elif key == "x":
        linear = angular = 0.0
    elif key == "q":
        break

    linear = max(-1.0, min(1.0, linear))
    angular = max(-1.0, min(1.0, angular))

    msg = {"linear": linear, "angular": angular}
    sock.sendto(json.dumps(msg).encode(), TARGET)

    print(f"\rlinear={linear:.2f} angular={angular:.2f}", end="")
