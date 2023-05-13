import socket
import numpy as np
from PIL import Image

import typer
import gymnasium

app = typer.Typer()

@app.command()
def run():    
    env = gymnasium.make(
        "ThirdStrike-v0", 
        executable='./.build/Build/Products/Debug/FinalBurn Neo.app/Contents/MacOS/FinalBurn Neo',
        is_player_one=True
    )

    while True:
        observation, info = env.reset()
        run_set(env)
        break

def run_set(env: gymnasium.Env):
    while True:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)

        if reward != 0:
            print(f'💥 reward {reward}')

        if terminated or truncated:
            break
