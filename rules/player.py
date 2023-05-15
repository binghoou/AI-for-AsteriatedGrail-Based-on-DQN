import roles.entity as entity 
import numpy as np
from utils import Encode

class Player:
    def __init__(self,role):
        super().__init__()
        self.ShuiJing=0
        self.BaoShi=0
        self.attack_action=0
        self.spell_action=0
        self.both_action=0
        self.hand=[]
        self.attached=[]
        self.role=role
        self.max_hand=6
        self.available_action=[]

    def encode(self):
        encoded=np.zeros(129)
        for card in self.hand:
            encoded[card]=1
        return encoded
    