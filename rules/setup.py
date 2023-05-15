from settings import all_roles
import random
from settings import all_seats

def decide_seat(num_player,forbidden):
    seats=[]
    if num_player==4:
        if 'ErLian' not in forbidden:
            seats.append(all_seats.get('ErLian'))
        if 'JianWei' not in forbidden:
            seats.append(all_seats.get('JianWei'))     
    if num_player==6:
        if 'SanLian' not in forbidden:
            seats.append(all_seats.get('SanLian'))
        if 'ErLian' not in forbidden:
            seats.append(all_seats.get('ErLian'))
        if 'JianWei' not in forbidden:
            seats.append(all_seats.get('JianWei'))   
    return seats
    
class decide_roles():
    def __init__(self,num_player,role_list=all_roles.get_roles()):
        self.roles=[]
        remaining_roles=role_list
        for i in range(num_player):
            self.roles.append(random.sample(remaining_roles,3))
            remaining_roles=set(remaining_roles)-set(self.roles[i])
    def get_roles(self):
        return self.roles
