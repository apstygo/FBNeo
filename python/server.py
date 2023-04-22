import socket
import numpy as np
from PIL import Image

PORT = 8080
BUFFER_WIDTH = 384
BUFFER_HEIGHT = 224
BUFFER_BBP = 3
BUFFER_SIZE = BUFFER_WIDTH * BUFFER_HEIGHT * BUFFER_BBP

def process_image(buffer: bytes) -> list[bool]:
    im = Image.frombytes('RGB', (BUFFER_WIDTH, BUFFER_HEIGHT), buffer)
    inputs = [False] * 29
    inputs[5] = True
    return inputs

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(1)

connection, address = sock.accept()
print(f'Received a connection at address: {address}')

while True:
    buffer = connection.recv(BUFFER_SIZE, socket.MSG_WAITALL)

    if not buffer:
        break

    inputs = process_image(buffer)
    connection.send(bytearray(inputs))

connection.close()
