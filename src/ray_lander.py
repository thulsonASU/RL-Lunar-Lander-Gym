import gymnasium as gym
from ray.rllib.algorithms.dqn import DQNConfig

# Tyler's Imports
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class trainDQN():
    def __init__(self,env_name="LunarLander-v2"):
        self.algo = DQNConfig().environment("LunarLander-v2").build()
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.env = gym.make(env_name, render_mode="human")
        self.terminated = self.truncated = False
        self.observations, self.info = self.env.reset()

    def train(self,iters=10):
        for i in range(iters):
            result = self.algo.train()
            print("Iteration:", i)
            print("Episode reward max:", result["episode_reward_max"])
            print("Episode reward min:", result["episode_reward_min"])
            print("Episode reward mean:", result["episode_reward_mean"])
            print()
        return print("Training complete")

    def save(self):
        # Save the model
        checkpoint = self.algo.save(self.path + "/models")
        return print("model saved at", checkpoint)
    
    def load(self,checkpoint):
        checkpoint_path = self.path + "/models/" + checkpoint
        self.algo.restore(checkpoint_path)
        
    def play(self):
        attempt = 1
        rewards = []
        fig, ax = plt.subplots()
        def animate(i):
            ax.clear()
            ax.plot(rewards)
        ani = animation.FuncAnimation(fig, animate, interval=1000)
        
        while attempt < 10:
            self.env.render()
            action = self.algo.compute_single_action(self.observations)
            self.observations, self.reward, self.terminated, self.truncated, self.info = self.env.step(action)
            print("Attempt:", attempt)
            print("Reward:", self.reward)
            print("action:", action)
            rewards.append(self.reward)
            plt.draw()
            plt.pause(0.01)

            if self.terminated or self.truncated:
                attempt+=1
                self.observations, self.info = self.env.reset()
            
                
if __name__ == "__main__":
    agent = trainDQN()
    # agent.train()
    # agent.save()
    agent.load(checkpoint="checkpoint_000010")
    agent.play()