<<<<<<< HEAD
import environment
import rospy
import time
=======
import environment 
>>>>>>> quad/master

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import random
import argparse
from keras.models import model_from_json, Model
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
import tensorflow as tf

import json
import pdb

from Replay_Buffer import Replay_Buffer
from Actor_Network import Actor_Network
from Critic_Network import Critic_Network

class OU(object):
<<<<<<< HEAD
=======

>>>>>>> quad/master
    def function(self, x, mu, theta, sigma=0.3):
        return theta * (mu - x) + sigma * np.random.randn(1)


def play_game(train_indicator = 1):

    env = environment.Environment()  # Rohit's custom environment

    obs_dim = env.num_states
    act_dim = env.num_actions

    buffer_size = 5000
    batch_size = 32
    gamma = 0.95
    tau = 0.001

    np.random.seed(1337)

    vision = False

>>>>>>> quad/master
    explore = 100000.
    eps_count = 2000
    max_steps = 100000
    reward = 0
    done = False
<<<<<<< HEAD
=======
    step = 0
>>>>>>> quad/master
    epsilon = 1
    indicator = 0

    #Tensorflow GPU optimization
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    sess = tf.Session(config=config)
    from keras import backend as K
    K.set_session(sess)
<<<<<<< HEAD

    # actor, critic and buffer
    actor = Actor_Network(env, sess)
    critic = Critic_Network(env, sess)
    replay_buffer = Replay_Buffer()

    # try:
    #   actor.model.load_weights("actormodel.h5")
    #   critic.model.load_weights("criticmodel.h5")
    #   actor.target_model.load_weights("actormodel.h5")
    #   critic.target_model.load_weights("criticmodel.h5")
    #   print("Weight load successfully")
    # except:
    #   print("WOW WOW WOW, Cannot find the weight")


    for e in range (eps_count):

        # receive initial observation state
        s_t = env._reset()  # cos theta, sin theta, theta dot
        s_t = np.asarray(s_t)
        total_reward = 0
        done = False
        step = 0

        while(done == False):
            if step > 200:
                break

            loss = 0
            epsilon -= 1.0/explore

            a_t = np.zeros([1, act_dim])
            noise_t = np.zeros([1, act_dim])

            # select action according to current policy and exploration noise
            a_t_original = actor.model.predict(s_t.reshape(1, s_t.shape[0]))
            
            noise_t[0][0] = train_indicator * max(epsilon, 0) * OU.function(a_t_original[0][0],  0.0 , 0.60, 0.30)
            noise_t[0][1] = train_indicator * max(epsilon, 0) * OU.function(a_t_original[0][1],  0.0 , 0.60, 0.30)
            noise_t[0][2] = train_indicator * max(epsilon, 0) * OU.function(a_t_original[0][2],  0.0 , 0.60, 0.30)

            a_t[0][0] = a_t_original[0][0] + noise_t[0][0]
            a_t[0][1] = a_t_original[0][1] + noise_t[0][1]
            a_t[0][2] = a_t_original[0][2] + noise_t[0][2]

            s_t1, r_t, done, _ = env._step(a_t[0])
            s_t1 = np.asarray(s_t1)

            # add to replay buffer
            replay_buffer.add(s_t, a_t[0], r_t, s_t1, done)
            # pdb.set_trace()
            # sample from replay buffer
            batch = replay_buffer.sample_batch()
            states = np.asarray([e[0] for e in batch])
            actions = np.asarray([e[1] for e in batch])
            rewards = np.asarray([e[2] for e in batch])
            new_states = np.asarray([e[3] for e in batch])
            dones = np.asarray([e[4] for e in batch])
            y_t = np.asarray([e[1] for e in batch])

            target_q_values = critic.target_model.predict([new_states, actor.target_model.predict(new_states)])

            for k in range (len(batch)):
                if dones[k]:
                    y_t[k] = rewards[k]
                else:
                    y_t[k] = rewards[k] + gamma*target_q_values[k]

            if (train_indicator):
                loss += critic.model.train_on_batch([states, actions], y_t)
                a_for_grad = actor.model.predict(states)
                grads = critic.gradients(states, a_for_grad)
                actor.train(states, grads)
                actor.target_train()
                critic.target_train()

            total_reward += r_t
            s_t = s_t1

            step += 1
            print('step: {}'.format(step))

        if np.mod(e, 3) == 0:
            if (train_indicator):
                print ('saving model')
                actor.model.save_weights("actormodel.h5", overwrite=True)
                with open("actormodel.json", "w") as outfile:
                    json.dump(actor.model.to_json(), outfile)

                critic.model.save_weights("criticmodel.h5", overwrite=True)
                with open("criticmodel.json", "w") as outfile:
                    json.dump(critic.model.to_json(), outfile)

        print('episode: ', e, ' total rewards: ', total_reward)

        # Plotting states
        states = env.plotState
        xs = states[:,0]
        ys = states[:,1]
        zs = states[:,2]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(xs, ys, zs)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        # plt.show()
        save_path = './plots/'+str(e)+'.png'
        plt.savefig(save_path)
        #########################

if __name__ == "__main__":
    rospy.init_node('quad', anonymous=True)
    play_game()
=======

    # actor, critic and buffer
    actor = Actor_Network(env, sess)
    critic = Critic_Network(env, sess)
    replay_buffer = Replay_Buffer()

    try:
        actor.model.load_weights("actormodel.h5")
        critic.model.load_weights("criticmodel.h5")
        actor.target_model.load_weights("actormodel.h5")
        critic.target_model.load_weights("criticmodel.h5")
        print("Weight load successfully")
    except:
        print("WOW WOW WOW, Cannot find the weight")


    for e in range (eps_count):

        # receive initial observation state
>>>>>>> quad/master

##############################################  turn obs into a np array

        obs = env._reset()  

        total_reward = 0
        done = False

        while(done == False):
            loss = 0
            epsilon -= 1.0/explore

            action = np.zeros([1, act_dim])
            noise_t = np.zeros([1, act_dim])

            # select actionn according to current policy and exploration noise
            action_original = actor.model.predict(obs.reshape(1, obs.shape[0]))

            noise_t[0][0] = train_indicator * max(epsilon, 0) * OU.function(action_original[0][0],  0.0 , 0.60, 0.30)
            action[0][0] = action_original[0][0] + noise_t[0][0]

            next_obs, reward, done, _ = env._step(action[0])  # ######################## might need to change stuff

            # add to replay buffer
            replay_buffer.add(obs, action[0], reward, next_obs, done)

            # sample from replay buffer
            batch = replay_buffer.sample_batch()
            states = np.asarray([e[0] for e in batch])
            actions = np.asarray([e[1] for e in batch])
            rewards = np.asarray([e[2] for e in batch])
            new_states = np.asarray([e[3] for e in batch])
            dones = np.asarray([e[4] for e in batch])
            y_t = np.asarray([e[1] for e in batch])

            target_q_values = critic.target_model.predict([new_states, actor.target_model.predict(new_states)])

            for k in range (len(batch)):
                if dones[k]:
                    y_t[k] = rewards[k]
                else:
                    y_t[k] = rewards[k] + gamma*target_q_values[k]

            if (train_indicator):
                loss += critic.model.train_on_batch([states, actions], y_t)
                a_for_grad = actor.model.predict(states)
                grads = critic.gradients(states, a_for_grad)
                actor.train(states, grads)
                actor.target_train()
                critic.target_train()

            total_reward += reward
            obs = next_obs

            step += 1
            # env.render()

        print ('total reward for episode: ', e, ' is: ', total_reward)

        if np.mod(e, 3) == 0:
            if (train_indicator):
                print ('saving model')
                actor.model.save_weights("actormodel.h5", overwrite=True)
                with open("actormodel.json", "w") as outfile:
                    json.dump(actor.model.to_json(), outfile)

                critic.model.save_weights("criticmodel.h5", overwrite=True)
                with open("criticmodel.json", "w") as outfile:
                    json.dump(critic.model.to_json(), outfile)

if __name__ == "__main__":
    play_game()
