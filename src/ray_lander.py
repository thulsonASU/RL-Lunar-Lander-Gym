import gymnasium as gym
from ray.rllib.algorithms.dqn import DQNConfig
import os
import csv
import collections
import pandas as pd

class trainDQN():
    def __init__(self,env_name="LunarLander-v2"):
        self.env_name = env_name
        self.algo = DQNConfig().environment(self.env_name).build()
        self.env = gym.make(self.env_name)
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.terminated = self.truncated = False
        self.observations, self.info = self.env.reset()
        self.firstRow = True
            
    def flatten_dict(self,d, parent_key='', sep='_'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, collections.abc.MutableMapping):
                items.extend(self.flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    def train(self,iters=10):
        with open(self.path + 'trainingResults.csv', 'w', newline='') as csvfile:
            csvfile.close()
        results = []
        for i in range(iters):
            result = self.algo.train()
            print("Iteration:", i)
            print("Episode reward max:", result["episode_reward_max"])
            print("Episode reward min:", result["episode_reward_min"])
            print("Episode reward mean:", result["episode_reward_mean"])
            print()
            results.append(self.flatten_dict(result))
            
            # Write the results to a CSV file every 10 iterations
            if (i + 1) % 10 == 0:
                print("Writing results to CSV file?")
                df = pd.DataFrame(results)
                df.to_csv(self.path + 'results.csv', mode='a', index=False)
                self.save()
            
        return print("Training complete")

    def save(self):
        # Save the model
        checkpoint = self.algo.save(self.path + "/models")
        return print("model saved at", checkpoint)
    
    def load(self,checkpoint):
        checkpoint_path = self.path + "/models/" + checkpoint
        self.algo.restore(checkpoint_path)
        
    def play(self,iterOut):
        with open(self.path + 'rewards.csv', 'w', newline='') as csvfile:
            csvfile.close()
        attempt = 1
        i = 0
        rewards = []
        attempts = []
        self.env = gym.make(self.env_name, render_mode="human")
        self.env.reset()
        print("Attempt:", attempt)
        try:
            while attempt < iterOut:
                # self.env.render()
                action = self.algo.compute_single_action(self.observations)
                self.observations, self.reward, self.terminated, self.truncated, self.info = self.env.step(action)
                print("Reward:", self.reward)
                print("Observation:", self.observations)
                rewards.append(self.reward)
                attempts.append(attempt)
                
                if self.terminated or self.truncated:
                    attempt+=1
                    print("Attempt:", attempt)
                    self.observations, self.info = self.env.reset()
            
            # Store rewards
            # Write the rewards to a CSV file
            with open(self.path + 'rewards.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Attempt","Reward"])
                for attempt, reward in zip(attempts, rewards):
                    writer.writerow([attempt, reward])

        except KeyboardInterrupt:
            print("Training interrupted")
            self.env.close()
            pass   
                    
if __name__ == "__main__":
    # available envs
    # https://github.com/qgallouedec/panda-gym/
    # https://gymnasium.farama.org/environments/classic_control/
    
    # 1 to train
    # 2 to play
    choice = 2
    
    if choice is 1:
        agent = trainDQN() # takes some time to init
        # train a model to a set number of iterations/generations
        agent.train(iters=1000)
        agent.save()
    elif choice is 2:
        agent = trainDQN() # takes some time to init
        # load the model you want to play
        agent.load(checkpoint="checkpoint_001000")
        agent.play(iterOut=10) # iterOut = how many times do you want the model to run through the environment
    else:
        print("Invalid Choice, Choose between 1 or 2")