import settings 
from call import Call
import roles.entity as entity
from components import Public_Deck
from utils import Have_Attack,Encode,Card_Inquire
import numpy as np

class Action:
    def __init__(self,source,target):
        self.source=source 
        self.target=target
    
    def step():
        pass 

    def encode():
        pass

class Cancel(Action):
    def __init__(self, source, target,incident):
        super().__init__(source, target)
        self.id=0
        self.incident=incident

    def step(self,env):
        if self.incident.id==1 or self.incident.id==2:
            self.incident.is_hit=True 
        env.board.state[env.team[self.incident.source]][1]=env.board.state[env.team[self.incident.source]][1]+1

    def encode(self):
        return Encode([self.source,self.target,self.id])

class Attack(Action):
    def __init__(self,source,target,card,damage=2):
        super().__init__(source,target)
        self.card=card
        self.damage=damage
        self.is_hit=False
        self.id=1
    
    def step(self,env):
        env.players[self.source].hand.remove(self.card)
        env.deck.discard(self.card)
        Call(env,'attack_2',self.target,self)
        if self.is_hit==True:
            if env.board.state[env.team[self.source]][1]<5:
                env.board.state[env.team[self.source]][1]=env.board.state[env.team[self.source]][1]+1
            Call(env,'attack_6',self.target,self)

    def encode(self):
        return Encode([self.source,self.target,self.id,self.card])


class GouDao(Action):
    def __init__(self,source,target,card,damage=2):
        super().__init__(source,target)
        self.card=card
        self.damage=damage
        self.is_hit=False
        self.id=2
    
    def step(self,env):
        env.players[self.source].hand.remove(self.card)
        env.deck.discard(self.card)
        Call(env,'GouDao_2',self.target,self)
        if self.is_hit==True:
            if env.board.state[env.team[self.source]][1]<5:
                env.board.state[env.team[self.source]][1]=env.board.state[env.team[self.source]][1]+1
            Call(env,'GouDao_6',self.target,self)


    def encode(self):
        return Encode([self.source,self.target,self.id,self.card])


class Discard(Action):
    def __init__(self, source, target,card,incident):
        super().__init__(source, target)
        self.card=card 
        self.incident=incident
        self.id=3

    def encode(self):
        return Encode([self.source,self.target,self.id])

    def step(self,env):
        env.players[self.source].hand.remove(self.card)
        env.deck.discard(self.card)

class HeCheng(Action):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = 11
    
    def step(self,env):
        env.board.state[env.team[self.source]][1]=env.board.state[env.team[self.source]][1]-3
        env.board.state[env.team[self.source]][3]=env.board.state[env.team[self.source]][3]+1
        if env.team[self.source]==1:
            env.board.state[0][0]=env.board.state[0][0]-1
        else:
            env.board.state[1][0]=env.board.state[1][0]-1
        env.players[self.source].hand=env.players[self.source].hand+env.deck.draw(3)
    
    def encode(self):
        return Encode([self.source,self.target,self.id])

class GouMai(Action):
    def __init__(self, source, target):
        super().__init__(source, target)
        self.id = 12
    
    def step(self,env):
        if env.board.state[env.team[self.source]][1]==4:
            env.board.state[env.team[self.source]][1]=env.board.state[env.team[self.source]][1]+1
        else:
            env.board.state[env.team[self.source]][1]=env.board.state[env.team[self.source]][1]+2
        env.players[self.source].hand=env.players[self.source].hand+env.deck.draw(3)
    
    def encode(self):
        return Encode([self.source,self.target,self.id])

def Attack_check(env,player_id):
    if env.players[player_id].attack_action==0:
        if env.players[player_id].both_action==0:
            return False
    if not Have_Attack(env,player_id):
        return False 
    return True


def HeCheng_check(env,player_id):
    if env.TeShuXingDong==False:
        return False
    if len(env.players[player_id].hand)>env.players[player_id].max_hand-3:
        return False 
    if env.team[player_id]==0:
        if env.board.state[0][1]+env.board.state[0][2]<3:
            return False 
    else:
        if env.board.state[1][1]+env.board.state[1][2]<3:
            return False 
    return True

def GouMai_check(env,player_id):
    if env.TeShuXingDong==False:
        return False
    if len(env.players[player_id].hand)>env.players[player_id].max_hand-3:
        return False 
    if env.board.state[env.team[player_id]][1]+env.board.state[env.team[player_id]][2]>=5:
        return False
    return True
        