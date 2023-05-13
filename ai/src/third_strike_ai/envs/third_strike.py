from subprocess import Popen
import socket
from dataclasses import dataclass
import os

import numpy as np
import gymnasium as gym
from PIL import Image
from third_strike_ai import constants as const


@dataclass
class Connection:
    process: Popen[bytes]
    socket: socket.socket

class ThirdStrikeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, executable: str, render_mode: str | None = None):
        self.executable = executable
        self.connection: Connection | None = None 

        # Observations are frames
        self.observation_space = gym.spaces.Box(
            low=0, 
            high=255, 
            shape=(const.BUFFER_HEIGHT, const.BUFFER_WIDTH, 3),
            dtype=np.uint8
        )

        # Actions are button presses
        self.action_space = gym.spaces.MultiBinary(10)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def step(self, action):
        return super().step(action)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._close_connection()

        # start process
        env = dict(os.environ, pauseWhenInactive="false")
        process = Popen([self.executable], env=env)
        
        # open socket
        sock = socket.socket()
        sock.bind(('', const.PORT))
        sock.listen(1)

        sock, address = sock.accept()
        print(f'Received a connection at address: {address}')

        # store connection
        self.connection = Connection(process, sock)

        # receive observation
        observation = self._receive_frame()
        info = dict()

        return (observation, info)

    def render(self):
        # TODO: Implement
        return super().render()

    def close(self):
        self._close_connection()

    def _receive_frame(self):
        if self.connection is None:
            return None

        buffer = self.connection.socket.recv(const.BUFFER_SIZE, socket.MSG_WAITALL)
        image = Image.frombytes('RGB', (const.BUFFER_WIDTH, const.BUFFER_HEIGHT), buffer)
        return np.asarray(image)

    def _close_connection(self):
        if self.connection is not None:
            self.connection.process.terminate()
            self.connection.socket.close()
            self.connection = None
