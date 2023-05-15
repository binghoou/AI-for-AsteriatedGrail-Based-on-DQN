import settings 
import random
import numpy as np

def Card_Inquire(card):
    '''
    地 圣 1-3      幻 4-7      技 8-12     血 13-17    咏 18-21
    火 圣 22-25    幻 26-30    技 31-34    血 35-38    咏 39-42
    雷 圣 43-46    幻 47-51    技 52-55    血 56-59    咏 60-63
    风 圣 64-66    幻 67-70    技 71-75    血 76-79    咏 80-84
    水 圣 85-87    幻 88-91    技 92-95    血 96-99    咏 100-105
    暗 圣 106-109  咏 110-111
    光 圣 112-114  幻 115-116  技 117-119  血 120-122
    法术待补充
    '''
    info=[]
    if card<=105:
        info.append(int((card-1)/21+1))
    elif card>=106 and card<=111:
        info.append(int(6))
    else:
        info.append(int(7))
    return info
    
def Have_Attack(env,player_id):
    for card in env.players[player_id].hand:
        if card<=116:
            return True 
    return False

def Encode(info,length=4):
    res= np.zeros(length)
    for i in range(len(info)):
        res[i]=info[i]
    return res
    

def get_enemy(env,player_id):
    enemies=[]
    for i in range(0,len(env.team)):
        if env.team[i]!=env.team[player_id]:
            enemies.append(i)
    return enemies