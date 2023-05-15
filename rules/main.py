from enviroment import grail_env
from rlcard.agents import DQNAgent

episodes=100
e=grail_env(4,[0,0,1,1])
agents=[]
for i in range(4):
    agents.append(DQNAgent(state_shape=e.state_shape,num_actions=112,mlp_layers=[64,64],save_path='rules/train/check_point',save_every=1000))
e.set_agents(agents)
for i in range(episodes):
    turns=e.run()
    e.reset()
    