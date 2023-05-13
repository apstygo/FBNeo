import numpy as np
import gymnasium as gym
from third_strike_ai import constants as const


class ThirdStrikeEnv(gym.Env):
    metadata = {"render_modes": ["human", "rgb_array"]}

    def __init__(self, render_mode: str | None = None):
        # Observations are frames
        self.observation_space = gym.spaces.Box(
            low=0, 
            high=255, 
            shape=(const.BUFFER_HEIGHT, const.BUFFER_WIDTH, 3),
            dtype=np.int8
        )

        # Actions are button presses
        self.action_space = gym.spaces.MultiBinary(10)

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def step(self, action):
        return super().step(action)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # TODO: Implement

    def render(self):
        # TODO: Implement
        return super().render()

    def close(self):
        # TODO: Implement
        pass
