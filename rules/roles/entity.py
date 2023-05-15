
class Entity():
    def __init__(self,id):
        super().__init__()
        self.id=id
        self.respond_before_action_start=False
        self.respond_on_action_start=False 
        self.respond_on_action_end=False
        self.respond_turn_end=False 
        self.respond_attack_1=False 
        self.respond_attack_2=False
        self.respond_attack_3=False
        self.respond_attack_4=False
        self.respond_attack_5=False
        self.respond_attack_6=False
        self.respond_attack_7=False 

    def check(env,to_check,incident):
        pass

    def respond(env,to_respond,incident):
        pass