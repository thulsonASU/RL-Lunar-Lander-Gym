from gym.envs.registration import register

register(
    id='Checkers-Tyler',
    entry_point='checkers:CheckersEnv'
)