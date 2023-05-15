import rlcard
import settings
from call import Call
from roles.attack_bot import attack_bot
from player import Player
from components import Public_Deck,Public_Board
# from setup import Decide_Roles,Decide_Seat
import numpy as np
from utils import Encode

class grail_env():
    def __init__(self,num_player,team,deck=Public_Deck(),board=Public_Board()):
        self.current_player=0
        self.deck=deck 
        self.deck.shuffle()
        self.board=board 
        self.players=[]
        self.turn=0
        self.num_player=num_player
        for i in range(num_player):
            self.players.append(Player(1))
        self.entities=[]
        self.agents=[]
        self.team=team
        self.winner=-1
        self.is_over=False
        self.state_shape=[[1],[154]]   #
        self.num_action=129
        self.previous_state=[None,None,None,None]
        self.previous_option=[None,None,None,None]
        self.TeShuXingDong=True
        self.is_ai=[True,True,True,True]

    def set_agents(self,agents):
        self.agents=agents
    
    def get_payoffs(self,player_id):
        if self.winner==-1:
            return 0
        elif self.winner==self.team[player_id]:
            return 1
        else:
            return -1


    def encode(self):
        info=[]
        for i in range(len(self.players)):
            info.append(len(self.players[i].hand))
            info.append(self.players[i].ShuiJing)
            info.append(self.players[i].BaoShi)
            info.append(self.players[i].role.id)
        return np.hstack((self.board.encode(),np.asarray(info)))

    def get_state(self,player_id):
        return np.hstack((self.encode(),np.asarray([player_id]),self.players[player_id].encode()))
        
    def step(self,incident):
        incident.step(self)

    def run(self,is_training=False):
        for i in range(len(self.players)):
            role=attack_bot(i)
            self.players[i].role=role
            self.entities.append(role)
            self.players[i].hand=self.deck.draw(4)
        while True:
            Call(self,'before_action_start',entity_id=self.current_player)
            Call(self,'action',entity_id=self.current_player)
            if self.is_over:
                break
            self.current_player=(self.current_player+1)%self.num_player
            self.turn=self.turn+1
        for player_id in range(self.num_player):
            legal_actions={}
            legal_actions[0]=Encode([0,0,0,0])
            state={'obs':self.get_state(player_id),'legal_actions':legal_actions}
            self.train_agent(player_id,state)
        return self.turn
    
    def train_agent(self,player_id,state):
        if self.previous_state[player_id] is not None:
            reward=self.get_payoffs(player_id)
            done=self.is_over
            self.agents[player_id].feed([self.previous_state[player_id],self.previous_option[player_id],reward,state,done])
    
    def check(self):
        if self.board.state[0][0]<=0:
            self.is_over=True
            self.winner=1
        if self.board.state[1][0]<=0:
            self.is_over=True
            self.winner=0
        if self.board.state[0][3]>=5:
            self.is_over=True
            self.winner=0
        if self.board.state[1][3]>=5:
            self.is_over=True
            self.winner=0

    def reset(self):
        self.current_player=0
        self.deck.reset()
        self.board.reset()
        self.players=[]
        for i in range(self.num_player):
            self.players.append(Player(1))
        self.entities=[]
        self.winner=-1
        self.turn=0
        self.is_over=False
        self.previous_state=[None,None,None,None]
        self.previous_option=[None,None,None,None]
        self.TeShuXingDong=True
