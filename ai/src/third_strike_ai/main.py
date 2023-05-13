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

    observation, info = env.reset()
    opponent_hp = 160

    while True:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)

        new_opponent_hp = info['opponent_hp']

        if new_opponent_hp < opponent_hp:
            print(f'💥 {opponent_hp - new_opponent_hp} damage')
            
            if new_opponent_hp == 0:
                print('💀 dead')

        opponent_hp = new_opponent_hp

        if terminated or truncated:
            break
