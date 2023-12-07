import gymnasium as gym
from ray.rllib.algorithms.dqn import DQNConfig
import ray
import os
import csv
import collections
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import imageio
from PIL import Image
# gifsicle is a command-line tool for creating, editing, and getting information about GIF images and animations.
# pygifsicle is a Python wrapper around gifsicle.
# Using it for compressing the gifs
# pip install pygifsicle
from pygifsicle import optimize
import subprocess # Check if gifsicle is installed


class trainDQN():
    def __init__(self,env_name="LunarLander-v2"):
        self.env_name = env_name
        self.algo = DQNConfig().environment(self.env_name).build()
        self.env = gym.make(self.env_name)
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.terminated = self.truncated = False
        self.observations, self.info = self.env.reset()
        self.firstRow = True
        
        # reinitailize the images folder
        # Define the directories
        self.plot_dir = self.path + '/images/plots'
        self.env_dir = self.path + '/images/env'
        
        # Delete all files in the plot directory
        for filename in os.listdir(self.plot_dir):
            os.remove(os.path.join(self.plot_dir, filename))

        # Delete all files in the env directory
        for filename in os.listdir(self.env_dir):
            os.remove(os.path.join(self.env_dir, filename))
            
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
        with open(self.path + 'results.csv', 'w', newline='') as csvfile:
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
                df = pd.DataFrame(results) # The results do not reset with each iteration
                df.to_csv(self.path + 'results.csv', mode='w', index=False) # Recommended Change: change mode to a write only (Changed) 
                # (This will update the results incase of a crash during training or interrupt so data is not lost)
                self.save()
            
        return print("Training complete")

    def save(self):
        # Save the model
        checkpoint = self.algo.save(self.path + "/models")
        return print("model saved at", checkpoint)
    
    def load(self,checkpoint):
        checkpoint_path = self.path + "/models/" + checkpoint
        self.algo.restore(checkpoint_path)
    
    def close(self):
        # Close the Ray agent
        ray.shutdown()
        
    def play(self,iterOut,checkpoint,plotting=False):
        with open(self.path + 'rewards.csv', 'w', newline='') as csvfile:
            csvfile.close()
        attempt = 1
        step = 0
        rewards = []
        observations_list = []
        attempts = []
        self.env = gym.make(self.env_name, render_mode="rgb_array")
        # self.env = gym.make(self.env_name)
        self.env.reset()
        print("Rendering environment")
        try:
            while attempt <= iterOut:
                # self.env.render()
                action = self.algo.compute_single_action(self.observations)
                self.observations, self.reward, self.terminated, self.truncated, self.info = self.env.step(action)
                observations_list.append(self.observations)
                rewards.append(self.reward)
                attempts.append(attempt)
                step+=1
                
                # Save the rendering of the environment as an image
                img = self.env.render()
                Image.fromarray(img).save(self.path + f'/images/env/env_{step}.png')  
                
                if self.terminated or self.truncated:
                    print("Attempt:", attempt)
                    attempt+=1
                    self.observations, self.info = self.env.reset()
                
            ## Create a GIF from the images after the environment has finished running
            # Extract the step number from the filename and sort the images based on that
            print("Creating environment gif")
            image_files = sorted(os.listdir(self.path + '/images/env'), key=lambda x: int(x.split('_')[1].split('.')[0]))
            images = [imageio.v3.imread(self.path + f'/images/env/{image_file}') for image_file in image_files]
            imageio.mimsave(self.path + '/images/envRender.gif', images, fps=30)
            
            if plotting:
                # agent is no longer needed (Do this to save memory while creating plots)
                self.close()
                print("Plotting Rewards and Observations")
                matplotlib.use('Agg') # Change backend to a non Tkinter one so it is threading-safe
                
                # Get the last step
                last_step = len(rewards)
                
                # Define the labels for the observation space
                labels = ['X Coordinate', 'Y Coordinate', 'X Velocity', 'Y Velocity', 'Angle', 'Angular Velocity', 'Left Leg Contact', 'Right Leg Contact']
            
                for step in range(len(rewards)):
                    # Create two subplots
                    fig, axs = plt.subplots(2, figsize=(10, 12))

                    # Plot the rewards on the first subplot
                    axs[0].plot(rewards[:step+1], color='blue', label='Reward')
                    axs[0].set_title(f'Checkpoint {checkpoint}, Attempt: {attempts[step]}, Rewards up to step {step+1}')
                    axs[0].set_xlim([0, last_step])  # Set the x-axis range
                    axs[0].legend()  # Add a legend

                    # Plot the observations on the second subplot
                    for i in range(len(labels)):
                        axs[1].plot([obs[i] for obs in observations_list[:step+1]], label=labels[i])
                    axs[1].set_title(f'Checkpoint {checkpoint}, Attempt: {attempts[step]}, Observations up to step {step+1}')
                    axs[1].set_xlim([0, last_step])  # Set the x-axis range
                    axs[1].legend()  # Add a legend

                    # Save the figure with the subplots as an image
                    plt.savefig(self.path + f'/images/plots/plots_{step+1}.png')
                    plt.close(fig)
                       
                print("Creating plot gif")
                image_files = sorted(os.listdir(self.path + '/images/plots'), key=lambda x: int(x.split('_')[1].split('.')[0]))
                images = [imageio.v3.imread(self.path + f'/images/plots/{image_file}') for image_file in image_files]
                imageio.mimsave(self.path + '/images/plots.gif', images, fps=30)
                self.compress()
            
            # Store rewards
            # Write the rewards to a CSV file
            print("Storing to csv")
            with open(self.path + 'rewards.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Attempt","Reward","Observations"])
                for attempt, reward, observation in zip(attempts, rewards,observations_list):
                    writer.writerow([attempt, reward, observation])
            
            print("Done :D")

        except KeyboardInterrupt:
            print("Training interrupted")
            self.env.close()
            pass   
    
    def compress(self):
        # Check if gifsicle is installed
        try:
            subprocess.check_call(['gifsicle', '--version'])
            gifsicle_installed = True
        except FileNotFoundError:
            gifsicle_installed = False

        if gifsicle_installed:
            # Only if you have gifsicle installed so you can use the wrapper
            print("Compressing plot gif")
            optimize(self.path + '/images/plots.gif')
        else:
            print("Skipping compression of plot gif as gifsicle is not installed")
        
# Class Experimentation            
if __name__ == "__main__":
    # available envs?
    # https://github.com/qgallouedec/panda-gym/
    # https://gymnasium.farama.org/environments/classic_control/
    
    # 0 for user_mode
    # 1 to train
    # 2 to play
    choice = 1
    
    if choice == 0:
        # init agent
        agent = trainDQN() # takes some time to init
        
        while True:
            try:
                # Ask the user for the number of iterations to train
                iters = int(input("Enter the number of iterations to train: "))
                # Ask the user for the number of attempts to render
                iterOut = int(input("Enter the number of attempts to render: "))
                break
            except ValueError:
                print("Invalid input. Please enter integer numbers.")
        
        # training
        agent.train(iters=iters)
        agent.save()
        
        # Generate the checkpoint name based on the number of iterations
        checkpoint = f"checkpoint_{str(iters).zfill(5)}"
        
        agent.load(checkpoint=checkpoint)
        agent.play(iterOut=iterOut,checkpoint=checkpoint) # iterOut = how many times do you want the model to run through the environment
        agent.close()
    elif choice == 1:
        agent = trainDQN() # takes some time to init
        # train a model to a set number of iterations/generations
        agent.train(iters=2000) # This will take a few hours to train
        agent.save()
        agent.close()
    elif choice == 2:
        agent = trainDQN() # takes some time to init
        # load the model you want to play
        checkpoint = "checkpoint_000002"
        agent.load(checkpoint=checkpoint)
        agent.play(iterOut=3,checkpoint=checkpoint,plotting=True) # iterOut = how many times do you want the model to run through the environment
    else:
        print("Invalid Choice, Choose between 0, 1, or 2")