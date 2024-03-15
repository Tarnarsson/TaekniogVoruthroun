###############################
#using python 3.10.0 64-bit
###############################
import mesa
from functions import Function
from designer import Designer
import random

V = {}
knowledge_requirement = [.5,.5,1,1,1,1,1,1,1,2]

def technical_complexity(unique_id: int) -> float:
    knowledge = knowledge_vector(unique_id=unique_id)
    TC = (sum([value**2 for value in knowledge[unique_id]])/len(knowledge[unique_id]))**0.5
    print(f"Created function {unique_id} with knowledge vector {knowledge[unique_id]} and technical complexity {TC}")
    return TC

def knowledge_vector(unique_id: int) -> dict:
    if unique_id not in V:
        shuffled_knowledge = knowledge_requirement.copy()
        random.shuffle(shuffled_knowledge)
        V[unique_id] = shuffled_knowledge
    return V
    

class Mesamodel(mesa.Model):
    def __init__(self, N: int):
        super().__init__()
        self.num_agents = N
        self.schedule = mesa.time.BaseScheduler(self) #aðrar aðferðir RandomActivation eða SimultaneousActivation

        for i in range(N):

            

            a_designer = Designer(unique_id = i+N, model =  self)
            a_function = Function(unique_id = i, model = self, complexity = technical_complexity(unique_id = i)) #i er identity af agentinum, self þarf að vera þarna en svo er hægt að passa fleiri args eftir það.
            self.schedule.add(a_designer)
            self.schedule.add(a_function)


    def step(self):
        self.schedule.step()


