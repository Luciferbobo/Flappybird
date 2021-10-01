import random

import torch
import torch.nn as nn

from memory import Memory
from network import DeepQNetwork

CHANNEL = 4
ACTIONS = 2
GAMMA = 0.99
REPLAY_MEMORY = 50000
BATCH = 32
# 神经网络参数替换间隔
REPLAYCE_INTERVAL = 500
SAVE_INTERVAL = 1000
PATH = 'saved_networks/dqn.pt'


class RL_Brain(object):
    def __init__(self, init_memory, initial_epsilon, train):
        self.device = torch.device(
            'cuda:0' if torch.cuda.is_available() else 'cpu')
        self.train = train
        self.time_step = 0
        self.memory = Memory(REPLAY_MEMORY)
        self.epsilon = initial_epsilon
        self.build()
        current_state = torch.stack(
            (init_memory, init_memory, init_memory, init_memory), 0)
        self.current_state = current_state.resize_((1, 4, 80, 80))

    def init_weights(self, model):
        if type(model) == nn.Conv2d or type(model) == nn.Linear:
            model.weight.data.normal_(0.0, 0.01)
        if type(model) == nn.Conv2d:
            model.bias.data.fill_(0.01)

    def build(self):
        input = CHANNEL
        output = ACTIONS
        self.q_eval = DeepQNetwork(input, output)
        self.q_target = DeepQNetwork(input, output)
        self._load_model()
        self.optimizer = torch.optim.Adam(self.q_eval.parameters(), lr=1e-6)
        self.loss = nn.MSELoss()

    def _load_model(self):
        try:
            checkpoint = torch.load(PATH,map_location=torch.device('cpu'))
            self.epsilon = checkpoint['epsilon']
            self.q_eval.load_state_dict(checkpoint['q_eval_model_state_dict'])
            self.q_target.load_state_dict(
                checkpoint['q_target_model_state_dict'])
            if self.train:
                self.q_eval.train()
                self.q_target.train()
            else:
                self.q_eval.eval()
                self.q_target.eval()
            self.q_eval = self.q_eval.to(device=self.device)
            self.q_target = self.q_target.to(device=self.device)
            print("Successfully loaded")
        except Exception:
            self.q_eval = self.q_eval.to(device=self.device)
            self.q_target = self.q_target.to(device=self.device)
            self.q_eval.apply(self.init_weights)
            print("Could not find old network weights")

    def train_network(self, epoch):
        if epoch % REPLAYCE_INTERVAL == 0:
            self.q_target.load_state_dict(self.q_eval.state_dict())
            print('target_params_replaced')

        current_states, q_target = self._compute_value()

        self.optimizer.zero_grad()
        outputs = self.q_eval(current_states)

        loss = self.loss(outputs, q_target)
        loss.backward()

        self.optimizer.step()
        self._save_model(epoch)
        return loss

    def _compute_value(self):
        current_states, next_states, terminals, rewards, action_indexs = \
            self.memory.preprocess_memory(BATCH)
        current_states = current_states.to(device=self.device)
        next_states = next_states.to(device=self.device)
        q_eval_next = self.q_eval(next_states)
        q_target_next = self.q_target(next_states)
        q_eval = self.q_eval(current_states)
        q_target = q_eval.clone()
        for i in range(0, BATCH):
            if terminals[i]:
                q_target[i][action_indexs[i]] = rewards[i]
            else:
                _, max_act_next = torch.max(q_eval_next[i], 0)
                q_target[i][action_indexs[i]] = rewards[i] + \
                    GAMMA * q_target_next[i][max_act_next]
        return current_states, q_target

    def _save_model(self, epoch):
        # save network every 1000 iteration
        if epoch % SAVE_INTERVAL == 0:
            torch.save({'epsilon': self.epsilon,
                        'q_eval_model_state_dict': self.q_eval.state_dict(),
                        'q_target_model_state_dict': self.q_eval.state_dict()},
                        'saved_networks/'+str(epoch)+'dqn.pt')
            print('save network')

    def choose_action(self):
        action = torch.zeros(2)
        q_max = None
        if random.random() <= self.epsilon and self.train:
            print("----------Random Action----------")
            action_index = random.randint(0, ACTIONS - 1)
            action[action_index] = 1
        else:
            q_eval = self.q_eval(self.current_state.to(device=self.device))[0]
            q_max, action_index = torch.max(q_eval, -1)
            action[action_index] = 1
        return action, q_max

    def store_memeory(self, action, reward, observation, terminal):
        self.current_state = self.memory.store_transition(
            self.current_state, action, reward, observation, terminal)
