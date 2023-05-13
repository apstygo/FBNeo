from gymnasium.envs.registration import register

register(
    id="ThirdStrike-v0",
    entry_point="third_strike_ai.envs:ThirdStrikeEnv"
)
