import typer
import gymnasium

app = typer.Typer()

@app.command()
def run(executable: str):
    env = gymnasium.make(
        "ThirdStrike-v0", 
        executable=executable,
        is_player_one=True
    )

    while True:
        observation, info = env.reset()
        run_set(env)

def run_set(env: gymnasium.Env):
    while True:
        action = env.action_space.sample()
        observation, reward, terminated, truncated, info = env.step(action)

        if reward != 0:
            print(f'💥 reward {reward}')

        if terminated or truncated:
            break
