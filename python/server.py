import socket
import numpy as np
from PIL import Image

PORT = 8080
BUFFER_WIDTH = 384
BUFFER_HEIGHT = 224
BUFFER_BBP = 3
BUFFER_SIZE = BUFFER_WIDTH * BUFFER_HEIGHT * BUFFER_BBP

def save_buffer_to_file(buffer: bytes): 
    im = Image.frombytes('RGB', (BUFFER_WIDTH, BUFFER_HEIGHT), buffer)
    im.show()
    pass

sock = socket.socket()
sock.bind(('', PORT))
sock.listen(1)

connection, address = sock.accept()
print(f'Received a connection at address: {address}')

while True:
    data = connection.recv(BUFFER_SIZE)

    if not data:
        break

    save_buffer_to_file(data)
    break

connection.close()
