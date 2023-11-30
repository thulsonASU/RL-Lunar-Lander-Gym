import checkers as ch
import numpy as np
import gym
from gym.envs.registration import register
import cleanrl

# Register the environment
register(
    id='Checkers-Tyler',
    entry_point='checkers:checkersEnv'
)

# Create a Gym environment
env = gym.make('Checkers-Tyler')

agent = cleanrl.dqn.DQN(env.observation_space, env.action_space)

# Train the agent
for _ in range(300):
    state = env.reset()
    done = False

    while not done:
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        agent.observe(state, action, reward, next_state, done)
        state = next_state

# Close the environment
env.close()