import random
from collections import deque

import torch


class Memory(object):
    def __init__(self, replay_memory):
        self.replay_memory = replay_memory
        self.memory = deque()

    def store_transition(self, current_state,
                         action, reward,
                         observation,
                         terminal):
        nextObservation = torch.cat(
            (observation, current_state[:, :3, :, :]), 1)
        self.memory.append((current_state, action,
                            reward, nextObservation, terminal))
        if len(self.memory) > self.replay_memory:
            self.memory.popleft()
        return nextObservation

    def preprocess_memory(self, batch):
        batch_memory = random.sample(self.memory, batch)
        current_states = torch.empty((batch, 4, 80, 80))
        next_states = torch.empty((batch, 4, 80, 80))
        terminals = []
        rewards = []
        action_indexs = []
        for i in range(0, batch):
            current_state = batch_memory[i][0]
            current_states[i] = current_state

            next_state = batch_memory[i][3]
            next_states[i] = next_state

            rewards.append(batch_memory[i][2])
            terminals.append(batch_memory[i][4])

            action = batch_memory[i][1]
            _, action_index = torch.max(action, -1)
            action_indexs.append(action_index)
        return current_states, next_states, terminals, rewards, action_indexs
