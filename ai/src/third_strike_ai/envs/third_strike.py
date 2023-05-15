import subprocess
import socket
from dataclasses import dataclass
import os
from typing import Any

import numpy as np
import gymnasium as gym
from PIL import Image, ImageOps
from third_strike_ai import constants as const


@dataclass
class Connection:
    process: subprocess.Popen[bytes]
    socket: socket.socket

@dataclass
class FightState:
    engaged: bool = False
    agent_hp: int = const.HP_MAX
    opponent_hp: int = const.HP_MAX
    agent_points: int = 0
    opponent_points: int = 0

class ThirdStrikeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(
        self, 
        executable: str,
        is_player_one: bool = True,
        damage_weights: tuple[float, float] = (1, 1),
        skipped_frames: int = 0,
        enable_sound: bool = False,
        render_mode: str | None = None
    ):
        self.executable = executable
        self.is_player_one = is_player_one
        self.damage_weights = damage_weights
        self.skipped_frames = skipped_frames
        self.enable_sound = enable_sound
        self.fight_state = FightState()
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
        if self.connection is None:
            raise RuntimeError('Cannot step while not connected to emulator.')

        # send inputs
        inputs = self._action_to_inputs(action)
        self.connection.socket.send(bytes((0,))) # 0 is the inputs header
        self.connection.socket.send(bytes(inputs))

        # get state
        observation, info = self._get_state()

        agent_hp = info['agent_hp']
        opponent_hp = info['opponent_hp']

        # calculate reward and stop conditions
        reward = 0

        if not self.fight_state.engaged and agent_hp == const.HP_MAX and opponent_hp == const.HP_MAX:
            # engage once HP is reset
            self.fight_state.engaged = True

        if self.fight_state.engaged:
            # calculate reward based on damage
            opponent_damage = self.fight_state.opponent_hp - opponent_hp
            agent_damage = self.fight_state.agent_hp - agent_hp
            reward = opponent_damage * self.damage_weights[0] - agent_damage * self.damage_weights[1]

            # handle round end
            if agent_hp == 0:
                self.fight_state.opponent_points += 1
                self.fight_state.engaged = False

            if opponent_hp == 0:
                self.fight_state.agent_points += 1
                self.fight_state.engaged = False

        self.fight_state.agent_hp = agent_hp
        self.fight_state.opponent_hp = opponent_hp

        terminated = self.fight_state.agent_points == 2 or self.fight_state.opponent_points == 2

        return observation, reward, terminated, False, info

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        # reset
        self._reset_connection()
        self.fight_state = FightState()

        if self.connection is None:
            # start process
            args: list[str] = [self.executable]

            if self.render_mode != 'human':
                args.append('--headless')

            if self.skipped_frames > 0:
                args.extend(('--skipped-frames', str(self.skipped_frames)))

            if not self.enable_sound:
                args.append('--disable-sound')

            process = subprocess.Popen(
                args, 
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            print(f'Started process with args: {process.args}')
            
            # open socket
            sock = socket.socket()
            sock.bind(('', const.PORT))
            sock.listen(1)

            sock, address = sock.accept()
            print(f'Received a connection at address: {address}')

            # store connection
            self.connection = Connection(process, sock)

        # get and return state
        return self._get_state()

    def render(self):
        # TODO: Implement
        return super().render()

    def close(self):
        self._close_connection()

    def _get_state(self):
        if self.connection is None:
            raise RuntimeError('Cannot get state while not connected to emulator.')

        frame = self._receive_frame(self.connection)
        observation = np.asarray(frame)
        info = self._get_info(frame)

        return observation, info

    def _receive_frame(self, connection: Connection) -> Image.Image:
        buffer = connection.socket.recv(const.BUFFER_SIZE, socket.MSG_WAITALL)
        return Image.frombytes('RGB', (const.BUFFER_WIDTH, const.BUFFER_HEIGHT), buffer)

    def _get_info(self, frame: Image.Image) -> dict[str, Any]:
        p1_bar = ImageOps.mirror(frame.crop(const.P1_HP_BAR_REGION))
        p2_bar = frame.crop(const.P2_HP_BAR_REGION)

        p1_hp = self._calculate_hp(p1_bar)
        p2_hp = self._calculate_hp(p2_bar)

        return {
            'agent_hp': p1_hp if self.is_player_one else p2_hp,
            'opponent_hp': p2_hp if self.is_player_one else p1_hp
        }

    def _calculate_hp(self, hp_bar: Image.Image) -> int:
        hp = 1
        reference = hp_bar.getpixel((0, 0))

        if reference not in const.HP_COLORS:
            return 0

        for i in range(1, hp_bar.size[0]):
            pixel = hp_bar.getpixel((i, 0))
            
            if pixel == reference:
                hp += 1
            else:
                break

        return hp

    def _action_to_inputs(self, action):
        inputs = np.zeros(29, dtype=np.int8)
        
        if self.is_player_one:
            inputs[2:12] = action
        else:
            inputs[14:24] = action

        return inputs

    def _reset_connection(self):
        if self.connection is None:
            return

        self.connection.socket.send(bytes((1,))) # 1 is the reset header

    def _close_connection(self):
        if self.connection is not None:
            self.connection.process.terminate()
            self.connection.socket.close()
            self.connection = None
