import socket
import numpy as np
from PIL import Image
from third_strike_ai import constants as const

import typer
import gymnasium

app = typer.Typer()

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

@app.command()
def run():    
    env = gymnasium.make(
        "ThirdStrike-v0", 
        executable='./.build/Build/Products/Debug/FinalBurn Neo.app/Contents/MacOS/FinalBurn Neo'
    )

    observation, info = env.reset()
    image = Image.fromarray(observation)
    image.show()
    print(info)
