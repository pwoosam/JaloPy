import io
import sys
import socket
import time
import cv2
import numpy

camera = cv2.VideoCapture(0)
camera.set(3,720)
camera.set(4,480)
while True:
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    __, frame = camera.read()
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    __, frame = cv2.imencode('.jpg', frame, encode_param)
    iofile = io.BytesIO(frame.tobytes())
    try:
        client_socket.connect(('169.231.75.134', 8000))
    except:
        continue
    client_socket.sendfile(iofile)
    client_socket.close()
    time.sleep(1/15)
