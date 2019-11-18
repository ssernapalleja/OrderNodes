import numpy as np
import tensorflow as tf
import matplotlib.pylab as plt
import random
import math
import os
import environment
from tensorflow_core.python.framework.test_ops import none

MAX_EPSILON = 1
MIN_EPSILON = 0.01
LAMBDA = 0.00001
GAMMA = 1
BATCH_SIZE = 50

class Model:
    def __init__(self,num_states_nodes,num_states_wp,num_actions_nodes,num_actions_wp, batch_size):
        self._num_states_nodes = num_states_nodes
        self._num_actions_nodes = num_actions_nodes
        self._num_states_wp = num_states_wp
        self._num_actions_wp = num_actions_wp
        self._batch_size = batch_size
        self.createModel()    
        
        
    def createModel(self):

        self.model_nodos = tf.keras.Sequential([
            #tf.keras.layers.Dense(),
            tf.keras.layers.Dense((self._num_states_nodes+self._num_states_wp)*2, input_dim=(self._num_states_nodes+self._num_states_wp), activation='relu'),
            tf.keras.layers.Dense((self._num_actions_nodes+self._num_actions_wp), activation='relu'),
            tf.keras.layers.Dense(self._num_actions_nodes)
            ])


        self.model_wp = tf.keras.Sequential([
            #tf.keras.layers.Dense(),
            tf.keras.layers.Dense((self._num_states_nodes+self._num_states_wp)*2, input_dim=(self._num_states_nodes+self._num_states_wp), activation='relu'),
            tf.keras.layers.Dense((self._num_actions_nodes+self._num_actions_wp), activation='relu'),
            tf.keras.layers.Dense(self._num_actions_wp)
            ])        

        self.model_nodos.compile(
        optimizer = tf.keras.optimizers.Adam()#.minimize(),
        ,loss = tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']    
            )
        
        self.model_wp.compile(
        optimizer = tf.keras.optimizers.Adam()#.minimize(),
        ,loss = tf.keras.losses.MeanSquaredError(),
        metrics=['accuracy']    
            )
        
       
        self.checkpoint_path_wp = "training_2_wp/cp-{epoch:04d}.ckpt"
        self.checkpoint_path_nodes = "training_2_nodes/cp-{epoch:04d}.ckpt"
        
        self.checkpoint_dir_wp = os.path.dirname(self.checkpoint_path_wp)
        self.checkpoint_dir_nodes = os.path.dirname(self.checkpoint_path_nodes)

# Create a callback that saves the model's weights every 5 epochs
        self.cp_callback_wp = tf.keras.callbacks.ModelCheckpoint(
    filepath=self.checkpoint_path_wp, 
    verbose=1, 
    save_weights_only=True,
    save_freq=100)
        
        self.cp_callback_nodes = tf.keras.callbacks.ModelCheckpoint(
    filepath=self.checkpoint_path_nodes, 
    verbose=1, 
    save_weights_only=True,
    save_freq=100)
        
        #self.model_nodos.load_weights(tf.train.latest_checkpoint(self.checkpoint_dir_nodes))
        #self.model_wp.load_weights(tf.train.latest_checkpoint(self.checkpoint_dir_wp))

    #def _define_model(self):
        ##self._states = tf.placeholder(shape=[None, self._num_states], dtype=tf.float32)
        ##self._q_s_a = tf.placeholder(shape=[None, self._num_actions], dtype=tf.float32)
        # create a couple of fully connected hidden layers

        ##loss = tf.losses.mean_squared_error(self._q_s_a, self._logits)
        ##self._optimizer = tf.train.AdamOptimizer().minimize(loss)
        ##self._var_init = tf.global_variables_initializer()

    def predict_one(self , state_node , state_wp):
        
        return self.model_nodos.predict((state_node+state_wp).reshape(1, self.num_states)) , self.model_wp.predict((state_node+state_wp).reshape(1, self.num_states))

    def mergeStates(self,state1,state2):
       
        a = []
        cont = 0
        for k in state1:
            a.append([*state1[cont] , *state2[cont]])
            cont +=1
        b = np.asarray(a)
        return b


    def predict_batch(self, states_nodos,states_wp):
        return self.model_nodos.predict(self.mergeStates(states_nodos,states_wp)),self.model_wp.predict(self.mergeStates(states_nodos,states_wp))
        
    def train_batch(self, x_batch_nodo,x_batch_wp,y_batch_nodo, y_batch_wp):
        self.model_nodos.fit(self.mergeStates(x_batch_nodo,x_batch_wp), y_batch_nodo, callbacks=[self.cp_callback_nodes])
        self.model_wp.fit(self.mergeStates(x_batch_nodo,x_batch_wp), y_batch_wp, callbacks=[self.cp_callback_wp])
       
    @property
    def num_states(self):
        return self._num_states

    @property
    def num_actions(self):
        return self._num_actions

    @property
    def batch_size(self):
        return self._batch_size

    @property
    def var_init(self):
        return self._var_init


class Memory:
    def __init__(self, max_memory):
        self._max_memory = max_memory
        self._samples = []

    def add_sample(self, sample):
        self._samples.append(sample)
        if len(self._samples) > self._max_memory:
            self._samples.pop(0)

    def sample(self, no_samples):
        if no_samples > len(self._samples):
            return random.sample(self._samples, len(self._samples))
        else:
            return random.sample(self._samples, no_samples)


class GameRunner:
    def __init__(self, model, env, memory, max_eps, min_eps,
                 decay, render=True):
        self._env = env
        self._model = model
        self._memory = memory
        self._render = render
        self._max_eps = max_eps
        self._min_eps = min_eps
        self._decay = decay
        self._eps = self._max_eps
        self._steps = 0
        self._reward_store = []
      

    def run(self):
        state_nodo, state_wp = self._env.reiniciar()
        tot_reward = 0
        max_x = -100
        while True:
            
            action_node,action_workPlace = self._choose_action(state_nodo, state_wp, self._env)
            next_state_nodo,next_state_wp, reward, done = self._env.step(action_node,action_workPlace)
            

            
            # is the game complete? If so, set the next state to
            # None for storage sake
            if done:
                next_state_nodo = None
                next_state_wp = None

            self._memory.add_sample((state_nodo,state_wp, action_node,action_workPlace, reward, next_state_nodo,next_state_wp))
            self._replay()

            # exponentially decay the eps value
            self._steps += 1
            self._eps = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) \
                                      * math.exp(-LAMBDA * self._steps)
            print( "eps: "+str(self._eps)+ " st:  "+str(self._steps))
            print("reward: " + str(reward))
            # move the agent to the next state and accumulate the reward
            state_nodo=next_state_nodo
            state_wp= next_state_wp

            tot_reward += reward

            # if the game is done, break the loop
            if done:
                self._reward_store.append(tot_reward)
                self._max_x_store.append(max_x)
                break

        print("Step {}, Total reward: {}, Eps: {}".format(self._steps, tot_reward, self._eps))

    def _choose_action(self, state_nodes, states_wp, env):
        if random.random() < self._eps:
            return  env.select_random()
        else:
            return np.argmax(self._model.predict_one(state_nodes, states_wp))

        

    def _replay(self):
        batch = self._memory.sample(self._model.batch_size)
        states_nodos = np.array([val[0] for val in batch])
        next_states_nodos = np.array([(np.zeros(self._model.num_states_nodos)
                                 if val[5] is None else val[5]) for val in batch])
        
        states_wp = np.array([val[1] for val in batch])
        next_states_wp = np.array([(np.zeros(self._model.num_states_nodos)
                                 if val[6] is None else val[6]) for val in batch])
        # predict Q(s,a) given the batch of states
        q_s_a_nodes, q_s_a_wp = self._model.predict_batch(states_nodos,states_wp)
        # predict Q(s',a') - so that we can do gamma * max(Q(s'a')) below
        q_s_a_d_nodes, q_s_a_d_wp = self._model.predict_batch(next_states_nodos,next_states_wp)
        # setup training arrays
        x_nodo = np.zeros((len(batch), self._model._num_states_nodes))
        y_nodo = np.zeros((len(batch), self._model._num_actions_nodes))
        x_wp = np.zeros((len(batch), self._model._num_states_wp))
        y_wp = np.zeros((len(batch), self._model._num_actions_wp))
        
        for i, b in enumerate(batch):
            state_node,state_wp, action_node,action_wp, reward, next_state_node,next_state_wp= b[0], b[1], b[2], b[3], b[4],b[5],b[6]
            # get the current q values for all actions in state
            current_q_nodes = q_s_a_nodes[i]
            current_q_wp = q_s_a_wp[i]
            # update the q value for action
            if (next_state_node is None) or i>=len(q_s_a_d_nodes):
                # in this case, the game completed after action, so there is no max Q(s',a')
                # prediction possible
                current_q_nodes[action_node] = reward
                current_q_wp[action_wp] = reward
            else:
                try:
                    current_q_nodes[action_node] = reward + GAMMA * np.amax(q_s_a_d_nodes[i])
                    current_q_wp[action_wp] = reward + GAMMA * np.amax(q_s_a_d_wp[i])
                except:    
                    current_q_nodes[action_node] = reward 
                    current_q_wp[action_wp] = reward 
            x_nodo[i] = state_node
            x_wp[i] = state_wp
            y_nodo[i] = current_q_nodes
            y_wp[i] = current_q_wp
        self._model.train_batch( x_nodo,x_wp,y_nodo, y_wp)

    @property
    def reward_store(self):
        return self._reward_store


if __name__ == "__main__":

    env = environment.environment()

    num_states_nodes = env.states_nodos
    num_states_wp = env.states_wp
    num_actions_nodes = env.maxNodos
    num_actions_wp = env.maxWP

    model = Model(num_states_nodes,num_states_wp,num_actions_nodes,num_actions_wp, BATCH_SIZE)
    mem = Memory(50000)


    #sess.run(model.var_init)
    gr = GameRunner( model, env, mem, MAX_EPSILON, MIN_EPSILON,
                    LAMBDA)
    num_episodes = 300
    cnt = 0
    while cnt < num_episodes:
        if cnt % 10 == 0:
            print('Episode {} of {}'.format(cnt+1, num_episodes))
        gr.run()
        cnt += 1
        model.model.summary()
        
        
        
    plt.plot(gr.reward_store)
    plt.show()
    plt.close("all")
    plt.show()