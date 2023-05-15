import settings
import random
import numpy as np
from utils import Encode


class Public_Deck():
    def __init__(self):
        self.deck = [int(i) for i in range(122)]
        self.abandon = []

    def shuffle(self):
        random.shuffle(self.abandon)
        random.shuffle(self.deck)
        self.deck = self.deck+self.abandon
        self.abandon=[]

    def draw(self, n):
        todraw = []
        num=n
        for card in self.deck:
            num = num-1
            todraw.append(card)
            self.deck.remove(card)
            if num == 0:
                break
        if num != 0:
            self.shuffle()
            return todraw + self.draw(num)
        else:
            return todraw

    def discard(self, card):
        self.abandon.append(card)

    def reset(self):
        self.deck = [int(i) for i in range(122)]
        self.abandon = []
        random.shuffle(self.deck)


class Public_Board():
    def __init__(self, state=[[15, 0, 0, 0],[15, 0, 0, 0]]):  # 士气，水晶，宝石，星杯
        self.state=state

    def check_grails(self):
        if self.state[0][3] == 5:
            return 0
        if self.red[1][3] == 5:
            return 1
        return -1
    
    def encode(self):
        return np.asarray(self.state[0]+self.state[1])

    def reset(self):
        self.state=[[15, 0, 0, 0],[15, 0, 0, 0]]
