import random
from itertools import cycle
import sys
import pygame
from pygame.locals import *
from game import flappy_bird_utils

FPS = 30
SCREENWIDTH = 288
SCREENHEIGHT = 512

pygame.init()
FPSCLOCK = pygame.time.Clock()
SCREEN = pygame.display.set_mode((SCREENWIDTH*2, SCREENHEIGHT))
pygame.display.set_caption('Flappy Bird')

IMAGES, SOUNDS, HITMASKS = flappy_bird_utils.load()
p_IMAGES,p_SOUNDS,p_HITMASKS = flappy_bird_utils.load_playerBird()
PIPEGAPSIZE = 100  # gap between upper and lower part of pipe
BASEY = SCREENHEIGHT * 0.79

PLAYER_WIDTH = IMAGES['player'][0].get_width()
PLAYER_HEIGHT = IMAGES['player'][0].get_height()
PIPE_WIDTH = IMAGES['pipe'][0].get_width()
PIPE_HEIGHT = IMAGES['pipe'][0].get_height()
BACKGROUND_WIDTH = IMAGES['background'].get_width()

PLAYER_INDEX_GEN = cycle([0, 1, 2, 1])


class GameState:
    def __init__(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(SCREENWIDTH * 0.2)
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
        self.basex = 0
        self.baseShift = IMAGES['base'].get_width() - BACKGROUND_WIDTH

        newPipe1 = getRandomPipe(0)
        newPipe2 = getRandomPipe(0)
        self.upperPipes = [
            {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        self.lowerPipes = [
            {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        # player velocity, max velocity, downward accleration, accleration on flap
        self.pipeVelX = -4
        self.playerVelY = 0  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerFlapAcc = -9  # players speed on flapping
        self.playerFlapped = False  # True when player flaps
        self.playerBird=GameByPlayer()

    def start_again(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(SCREENWIDTH * 0.2)
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
        self.basex = 0
        self.baseShift = IMAGES['base'].get_width() - BACKGROUND_WIDTH

        newPipe1 = getRandomPipe(0)
        newPipe2 = getRandomPipe(0)
        self.upperPipes = [
            {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
            {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        self.lowerPipes = [
            {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
            {'x': SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        # player velocity, max velocity, downward accleration, accleration on flap
        self.pipeVelX = -4
        self.playerVelY = 0  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerFlapAcc = -9  # players speed on flapping
        self.playerFlapped = False  # True when player flaps

    def frame_step(self, input_actions):
        pygame.event.pump()

        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: flap the bird
        if input_actions[1] == 1:
            if self.playery > -2 * PLAYER_HEIGHT:
                self.playerVelY = self.playerFlapAcc
                self.playerFlapped = True
                #SOUNDS['wing'].play()

        #playerBird
        for event in pygame.event.get():

            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if self.playerBird.playery > -2 * PLAYER_HEIGHT:
                    self.playerBird.playerVelY = self.playerBird.playerFlapAcc
                    self.playerBird.playerFlapped = True
                    #SOUNDS['wing'].play()

        # check for score
        playerMidPos = self.playerx + PLAYER_WIDTH / 2
        for pipe in self.upperPipes:
            pipeMidPos = pipe['x'] + PIPE_WIDTH / 2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                self.score += 1
                SOUNDS['point'].play()
                reward = 1

        p_playerMidPos = self.playerBird.playerx + PLAYER_WIDTH / 2
        for pipe in self.playerBird.upperPipes:
            p_pipeMidPos = pipe['x'] + PIPE_WIDTH / 2
            if p_pipeMidPos <= p_playerMidPos < p_pipeMidPos + 4:
                self.playerBird.score += 1
                SOUNDS['point'].play()

        # playerIndex basex change
        if (self.loopIter + 1) % 3 == 0:
            self.playerIndex = next(PLAYER_INDEX_GEN)
        self.loopIter = (self.loopIter + 1) % 30
        self.basex = -((-self.basex + 100) % self.baseShift)


        #playerBird
        if (self.playerBird.loopIter + 1) % 3 == 0:
            self.playerBird.playerIndex = next(PLAYER_INDEX_GEN)
        self.playerBird.loopIter = (self.playerBird.loopIter + 1) % 30
        self.playerBird.basex = SCREENWIDTH-((-self.playerBird.basex+388) % self.playerBird.baseShift)


        # player's movement
        if self.playerVelY < self.playerMaxVelY and not self.playerFlapped:
            self.playerVelY += self.playerAccY
        if self.playerFlapped:
            self.playerFlapped = False
        self.playery += min(self.playerVelY, BASEY -
                            self.playery - PLAYER_HEIGHT)
        if self.playery < 0:
            self.playery = 0

        if self.playerBird.playerVelY < self.playerBird.playerMaxVelY and not self.playerBird.playerFlapped:
            self.playerBird.playerVelY += self.playerBird.playerAccY
        if self.playerBird.playerFlapped:
            self.playerBird.playerFlapped = False
        self.playerBird.playery += min(self.playerBird.playerVelY, BASEY -
                            self.playerBird.playery - PLAYER_HEIGHT)
        if self.playerBird.playery < 0:
            self.playerBird.playery = 0

        # move pipes to left
        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            uPipe['x'] += self.pipeVelX
            lPipe['x'] += self.pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < self.upperPipes[0]['x'] < 5:
            newPipe = getRandomPipe(0)
            self.upperPipes.append(newPipe[0])
            self.lowerPipes.append(newPipe[1])

        # remove first pipe if its out of the screen
        if self.upperPipes[0]['x'] < -PIPE_WIDTH:
            self.upperPipes.pop(0)
            self.lowerPipes.pop(0)

        #playerBird
        for uPipe, lPipe in zip(self.playerBird.upperPipes, self.playerBird.lowerPipes):
            uPipe['x'] += self.playerBird.pipeVelX
            lPipe['x'] += self.playerBird.pipeVelX

        if SCREENWIDTH < self.playerBird.upperPipes[0]['x'] < SCREENWIDTH+5:#288-293
            p_newPipe = getRandomPipe(1)
            self.playerBird.upperPipes.append(p_newPipe[0])
            self.playerBird.lowerPipes.append(p_newPipe[1])

        if self.playerBird.upperPipes[0]['x'] < SCREENWIDTH:#288-52=236 -PIPE_WIDTH+SCREENWIDTH
            self.playerBird.upperPipes.pop(0)
            self.playerBird.lowerPipes.pop(0)


        # check if crash here
        isCrash = checkCrash({'x': self.playerx, 'y': self.playery,
                              'index': self.playerIndex},
                             self.upperPipes, self.lowerPipes)
        if isCrash:
            #SOUNDS['hit'].play()
            SOUNDS['die'].play()
            terminal = True
            self.start_again()
            reward = -1

        p_isCrash = checkCrash({'x': self.playerBird.playerx, 'y': self.playerBird.playery,
                              'index': self.playerBird.playerIndex},
                             self.playerBird.upperPipes, self.playerBird.lowerPipes)
        if p_isCrash:
            #SOUNDS['hit'].play()
            SOUNDS['die'].play()
            self.playerBird.showGameOverScreen()
            self.playerBird.__init__()

        # draw sprites1
        SCREEN.blit(IMAGES['background'], (0, 0))

        for uPipe, lPipe in zip(self.upperPipes, self.lowerPipes):
            SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (self.basex, BASEY))
        # print score so player overlaps the score
        showScore(self.score,0)
        SCREEN.blit(IMAGES['player'][self.playerIndex],
                    (self.playerx, self.playery))


        #draw sprites2
        SCREEN.blit(p_IMAGES['background'], (SCREENWIDTH, 0))

        for uPipe, lPipe in zip(self.playerBird.upperPipes, self.playerBird.lowerPipes):
            SCREEN.blit(p_IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
            SCREEN.blit(p_IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

        SCREEN.blit(IMAGES['base'], (self.playerBird.basex, BASEY))

        # print score so player overlaps the score
        showScore(self.playerBird.score,1)
        SCREEN.blit(p_IMAGES['player'][self.playerBird.playerIndex],
                    (self.playerBird.playerx, self.playerBird.playery))

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())[:288,::]
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        # print self.upperPipes`[0]['y'] + PIPE_HEIGHT - int(BASEY * 0.2)
        return image_data, reward, terminal

#供玩家控制的封装类，作为前一个类的数据成员
class GameByPlayer:
    def __init__(self):
        self.score = self.playerIndex = self.loopIter = 0
        self.playerx = int(SCREENWIDTH * 1.2)
        self.playery = int((SCREENHEIGHT - PLAYER_HEIGHT) / 2)
        self.basex = SCREENWIDTH
        self.baseShift = IMAGES['base'].get_width() - BACKGROUND_WIDTH

        newPipe1 = getRandomPipe(1)
        newPipe2 = getRandomPipe(1)
        self.upperPipes = [
            {'x': 2*SCREENWIDTH, 'y': newPipe1[0]['y']},
            {'x': 2*SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
        ]
        self.lowerPipes = [
            {'x': 2*SCREENWIDTH, 'y': newPipe1[1]['y']},
            {'x': 2*SCREENWIDTH + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
        ]

        # player velocity, max velocity, downward accleration, accleration on flap
        self.pipeVelX = -4
        self.playerVelY = 0  # player's velocity along Y, default same as playerFlapped
        self.playerMaxVelY = 10  # max vel along Y, max descend speed
        self.playerMinVelY = -8  # min vel along Y, max ascend speed
        self.playerAccY = 1  # players downward accleration
        self.playerFlapAcc = -9  # players speed on flapping
        self.playerFlapped = False  # True when player flaps
        self.playerRot=45

    def showGameOverScreen(self):
        """crashes the player down ans shows gameover image"""
        self.playerx = SCREENWIDTH * 1.2
        self.playery = SCREENHEIGHT*0.4
        self.playerAccY = 2
        self.playerVelRot = 7

        # play hit and die sounds
        SOUNDS['die'].play()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                    #if self.playery + self.playerHeight >= BASEY - 1:
                    return
            """
            # player y shift
            if playery + playerHeight < BASEY - 1:
                playery += min(playerVelY, BASEY - playery - playerHeight)

            # player velocity change
            if playerVelY < 15:
                playerVelY += playerAccY

            # rotate only when it's a pipe crash
            if not crashInfo['groundCrash']:
                if playerRot > -90:
                    playerRot -= playerVelRot
            """
            if self.playerRot > -90:
                self.playerRot -= self.playerVelRot
            # draw sprites
            #SCREEN.blit(IMAGES['background'], (SCREENWIDTH, 0))

            #for uPipe, lPipe in zip(upperPipes, lowerPipes):
                #SCREEN.blit(IMAGES['pipe'][0], (uPipe['x'], uPipe['y']))
                #SCREEN.blit(IMAGES['pipe'][1], (lPipe['x'], lPipe['y']))

            #SCREEN.blit(IMAGES['base'], (basex, BASEY))

            showScore(self.score,1)

            #playerSurface = pygame.transform.rotate(p_IMAGES['player'][1], self.playerRot)
            #SCREEN.blit(playerSurface, (self.playerx, self.playery))
            #SCREEN.blit(p_IMAGES['player'][1], (self.playerx, self.playery))
            SCREEN.blit(p_IMAGES['gameover'], (338, 180))

            FPSCLOCK.tick(FPS)
            pygame.display.update()

def playerShm(playerShm):
    """oscillates the value of playerShm['val'] between 8 and -8"""
    if abs(playerShm['val']) == 8:
        playerShm['dir'] *= -1

    if playerShm['dir'] == 1:
         playerShm['val'] += 1
    else:
        playerShm['val'] -= 1



def getRandomPipe(player):
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe

    """
    gapY = random.randrange(0, int(BASEY * 0.6 - PIPEGAPSIZE))
    gapY += int(BASEY * 0.2)
    PIPE_HEIGHT = IMAGES['pipe'][0].get_height()
    pipeX = [SCREENWIDTH + 10,2*SCREENWIDTH+10]
    """

    gapYs = [20, 30, 40, 50, 60, 70, 80, 90]
    index = random.randint(0, len(gapYs) - 1)
    gapY = gapYs[index]

    gapY += int(BASEY * 0.2)
    pipeX = [SCREENWIDTH + 10,2*SCREENWIDTH+10]

    return [
        {'x': pipeX[player], 'y': gapY - PIPE_HEIGHT},  # upper pipe
        {'x': pipeX[player], 'y': gapY + PIPEGAPSIZE},  # lower pipe
    ]


def showScore(score,player):
    """displays score in center of screen"""
    scoreDigits = [int(x) for x in list(str(score))]
    totalWidth = 0  # total width of all numbers to be printed

    for digit in scoreDigits:
        totalWidth += IMAGES['numbers'][digit].get_width()

    Xoffset = [(SCREENWIDTH - totalWidth) / 2,(SCREENWIDTH - totalWidth) / 2+SCREENWIDTH]

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xoffset[player], SCREENHEIGHT * 0.1))
        Xoffset[player] += IMAGES['numbers'][digit].get_width()


def checkCrash(player, upperPipes, lowerPipes):
    """returns True if player collders with base or pipes."""
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    # if player crashes into ground
    if player['y'] + player['h'] >= BASEY - 1:
        return True
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                                 player['w'], player['h'])

        for uPipe, lPipe in zip(upperPipes, lowerPipes):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(
                uPipe['x'], uPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)
            lPipeRect = pygame.Rect(
                lPipe['x'], lPipe['y'], PIPE_WIDTH, PIPE_HEIGHT)

            # player and upper/lower pipe hitmasks
            pHitMask = HITMASKS['player'][pi]
            uHitmask = HITMASKS['pipe'][0]
            lHitmask = HITMASKS['pipe'][1]

            # if bird collided with upipe or lpipe
            uCollide = pixelCollision(
                playerRect, uPipeRect, pHitMask, uHitmask)
            lCollide = pixelCollision(
                playerRect, lPipeRect, pHitMask, lHitmask)

            if uCollide or lCollide:
                return True

    return False


def pixelCollision(rect1, rect2, hitmask1, hitmask2):
    """Checks if two objects collide and not just their rects"""
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1 + x][y1 + y] and hitmask2[x2 + x][y2 + y]:
                return True
    return False


