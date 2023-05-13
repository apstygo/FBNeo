import socket
import numpy as np
from PIL import Image
from third_strike_ai import constants as const


def process_image(buffer: bytes) -> list[bool]:
    im = Image.frombytes('RGB', (const.BUFFER_WIDTH, const.BUFFER_HEIGHT), buffer)
    inputs = [False] * 29
    inputs[5] = True
    return inputs

def loop():
    sock = socket.socket()
    sock.bind(('', const.PORT))
    sock.listen(1)

    connection, address = sock.accept()
    print(f'Received a connection at address: {address}')

    while True:
        buffer = connection.recv(const.BUFFER_SIZE, socket.MSG_WAITALL)

        if not buffer:
            break

        inputs = process_image(buffer)
        connection.send(bytearray(inputs))

    connection.close()

if __name__ == '__main__':
    loop()
