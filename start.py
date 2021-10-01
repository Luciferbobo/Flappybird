import torch
import utils
import cv2
import game.wrapped_flappy_bird as game
from rl_brain import RL_Brain
import pygame

TRAIN = True
OBSERVE = 10000
# OBSERVE = 1000000
EXPLORE = 2000000
INITIAL_EPSILON = 0.1
# INITIAL_EPSILON = 0
FINAL_EPSILON = 0.0001


def preprocess(observation):
    # preprocess raw image to 80*80 gray image
    observation = cv2.cvtColor(cv2.resize(
        observation, (80, 80)), cv2.COLOR_BGR2GRAY)
    ret, observation = cv2.threshold(observation, 1, 255, cv2.THRESH_BINARY)
    return torch.torch.FloatTensor(observation).resize_((1, 1, 80, 80))


def playFlappyBird():
    brain, flappyBird = init()
    time_step = 0
    score = 0
    pygame.mixer.init()
    pygame.mixer.music.load("assets/audio/bgm.mp3")
    pygame.mixer.music.play(-1)
    while True:
        #flappyBird_Player.frame_step()
        action, q_max = brain.choose_action()
        nextObservation, reward, terminal = flappyBird.frame_step(action)
        nextObservation = preprocess(nextObservation)
        if reward == 1:
            score += 1
        elif reward == -1:
            print("game over score: %d" % score)
            if not TRAIN:
                exit()
            score = 0

        brain.store_memeory(action, reward, nextObservation, terminal)

        loss = train(time_step, brain)

        _, action = torch.max(action, -1)
        print_info(action, brain.epsilon, loss, q_max, reward, time_step)
        time_step += 1


def init():
    flappyBird = game.GameState()
    #flappyBird_Player=game.GameByPlayer()
    init_action = torch.IntTensor([1, 0])
    #flappyBird_Player.frame_step()
    init_observation, _, _ = flappyBird.frame_step(init_action)
    init_observation = preprocess(init_observation)
    brain = RL_Brain(init_observation, INITIAL_EPSILON, TRAIN)
    return brain, flappyBird


def train(time_step, brain):
    loss = None
    if time_step > OBSERVE and TRAIN:
        loss = brain.train_network(time_step)
    if brain.epsilon > FINAL_EPSILON and time_step > OBSERVE:
        brain.epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE
    return loss


def print_info(action, epsilon, loss, q_max, reward, time_step):
    if time_step <= OBSERVE:
        utils.print_simple_info(time_step, epsilon, action, reward)
    elif OBSERVE < time_step <= OBSERVE + EXPLORE:
        utils.print_train_info(time_step, "explore", epsilon,
                               action, reward, q_max, loss)
    else:
        utils.print_train_info(time_step, "train", epsilon,
                               action, reward, q_max, loss)


def main():
    playFlappyBird()


if __name__ == '__main__':
    main()
