from roles.entity import Entity
from basic_action import Attack,Attack_check,HeCheng_check,GouMai_check,GouMai,HeCheng,GouDao,Discard,Cancel
from utils import Card_Inquire,get_enemy
from call import Call
import numpy as np
import torch

class attack_bot(Entity):
    def __init__(self,i):
        super().__init__(id=i)
        self.respond_attack_2=True
        self.respond_action=True
        self.id=1
    
    def check(self,env,player_id,action_to_check,incident=None):
        option=[]
        if action_to_check==11: #合成检查
            if HeCheng_check(env,player_id):
                return [HeCheng(player_id,player_id)]
            return []
        if action_to_check==12: #购买检查
            if GouMai_check(env,player_id):
                return [GouMai(player_id,player_id)]
            return []
        if action_to_check==1:  #攻击检查
            if Attack_check(env,player_id):
                enemies=get_enemy(env,player_id)
                for i in range(len(env.players[player_id].hand)):
                    if env.players[player_id].hand[i]<=116:
                        for enemy in enemies:
                            option.append(Attack(player_id,enemy,env.players[player_id].hand[i]))
        if action_to_check==2:  
            attack_card_info=Card_Inquire(incident.card)
            enemies=get_enemy(env,player_id)
            enemies.remove(incident.source)
            if attack_card_info[0]==5:
                for i in range(len(env.players[player_id].hand)):
                    if Card_Inquire(env.players[player_id].hand[i])[0]==6:
                        option.append(Discard(player_id,incident.source,env.players[player_id].hand[i],incident))
            else:
                for i in range(len(env.players[player_id].hand)):
                    hand_info=Card_Inquire(env.players[player_id].hand[i])
                    if hand_info[0]==attack_card_info[0] or hand_info[0]==5:
                        for enemy in enemies:
                            option.append(GouDao(player_id,enemy,env.players[player_id].hand[i],incident))
                    elif hand_info[0]==6:
                        option.append(Discard(player_id,incident.source,env.players[player_id].hand[i],incident))
            cancel=Cancel(player_id,player_id,incident)
            option.append(cancel)
        if action_to_check==3:  
            for card in env.players[player_id].hand:
                option.append(Discard(player_id,player_id,card,incident))
        return option

    def respond(self,env,player_id,msg,incident=None):
        if msg=='before_action_start':
            env.players[player_id].both_action=1
            env.players[player_id].available_action=[]
            env.players[player_id].available_action=env.players[player_id].available_action+self.check(env,player_id,1)
            env.players[player_id].available_action=env.players[player_id].available_action+self.check(env,player_id,11)
            env.players[player_id].available_action=env.players[player_id].available_action+self.check(env,player_id,12)  
            if len(env.players[player_id].available_action)==0:
                hand_num=len(env.players[player_id].hand)
                for card in env.players[player_id].hand:
                    env.deck.discard(card)
                env.players[player_id].hand=env.deck.draw(hand_num)
                Call(env,'before_action_start',entity_id=env.current_player)

        
        if msg=='action':
            dict_action={}
            for i in range(len(env.players[player_id].available_action)):
                dict_action[i]=env.players[player_id].available_action[i].encode()
            state={'obs':env.get_state(player_id),'legal_actions':dict_action}
            if env.is_ai[player_id]:
                option=env.agents[player_id].step(state)
                env.players[player_id].available_action[option].step(env)
                env.previous_state[player_id]={'obs':env.get_state(player_id),'legal_actions':dict_action}
                env.previous_option[player_id]=option
                env.train_agent(player_id,state)
            else:
                pass
            
        if msg=='attack_2':
            dict_action={}
            available_options=self.check(env,player_id,2,incident)
            for i in range(len(available_options)):
                dict_action[i]=available_options[i].encode()
            state={'obs':env.get_state(player_id),'legal_actions':dict_action}
            if env.is_ai[player_id]:
                option=env.agents[player_id].step(state)
                available_options[option].step(env)
                env.train_agent(player_id,state)
                env.previous_state[player_id]={'obs':env.get_state(player_id),'legal_actions':dict_action}
                env.previous_option[player_id]=option  

        if msg=='GouDao_2':
            dict_action={}
            available_options=self.check(env,player_id,2,incident)
            for i in range(len(available_options)):
                dict_action[i]=available_options[i].encode()
            state={'obs':env.get_state(player_id),'legal_actions':dict_action}
            if env.is_ai[player_id]:
                option=env.agents[player_id].step(state)
                available_options[option].step(env)
                env.train_agent(player_id,state)
                env.previous_state[player_id]={'obs':env.get_state(player_id),'legal_actions':dict_action}
                env.previous_option[player_id]=option 
            
    
        if msg=='attack_6':
            
            env.players[player_id].hand=env.players[player_id].hand+env.deck.draw(incident.damage)
            loss=0
            while len(env.players[player_id].hand)>env.players[player_id].max_hand:
                dict_action={}
                options=self.check(env,player_id,3)
                for i in range(len(options)):
                    dict_action[i]=options[i].encode()
                state={'obs':env.get_state(player_id),'legal_actions':dict_action}
                if env.is_ai[player_id]:
                    option=env.agents[player_id].step(state)
                    options[option].step(env)
                    env.train_agent(player_id,state)
                    env.previous_state[player_id]={'obs':env.get_state(player_id),'legal_actions':dict_action}
                    env.previous_option[player_id]=option 
                loss=loss+1
            env.board.state[env.team[player_id]][0]=env.board.state[env.team[player_id]][0]-loss

            

