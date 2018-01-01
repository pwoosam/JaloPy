import io
import time
import picamera
import socket
import struct

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 80))
serversocket.listen(0)
connection = serversocket.makefile('wb')


with picamera.PiCamera() as camera:
    camera.resolution = (1920, 1080)
    camera.start_preview()
    time.sleep(2)

    start = time.time()
    stream = io.BytesIO()
    while True:
        camera.capture(stream, 'jpeg')
        connection.write(struct.pack('<L', stream.tell()))
        connection.flush()
        stream.seek(0)
        connection.write(stream.read())
        if time.time() - start > 30:
            break
        stream.seek(0)
        stream.truncate()
    connection.write(struct.pack('<L', 0))

connection.close()
serversocket.close()

