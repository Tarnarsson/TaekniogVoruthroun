###############################
#using python 3.10.0 64-bit
###############################
import mesa
import random
from functions import Function
from designer import Designer
from equations import technical_complexity

knowledge_requirement = [.5,.5,1,1,1,1,1,1,1,2]

class Mesamodel(mesa.Model):
    def __init__(self, N: int):
        super().__init__()
        self.designers = []
        self.functions = [] 
        self.num_agents = N
        self.schedule = mesa.time.BaseScheduler(self) #aðrar aðferðir RandomActivation eða SimultaneousActivation

        self.designers_function = {}

        for i in range(N):
            random.shuffle(knowledge_requirement)
            k_n = knowledge_requirement
            random.shuffle(knowledge_requirement)
            a_n = knowledge_requirement

            a_designer = Designer(unique_id = i, model =  self, knowledge_ability= technical_complexity(unique_id=i), a_n = a_n)
            a_function = Function(function_id = i, model = self, complexity = technical_complexity(unique_id = i), k_n = k_n) #i er identity af agentinum, self þarf að vera þarna en svo er hægt að passa fleiri args eftir það.
            self.designers.append(a_designer)
            self.functions.append(a_function)

            self.schedule.add(a_designer)
            a_designer.function = a_function
            self.designers_function[a_designer] = a_function
            a_function.designer = a_designer          


    def step(self):
        self.schedule.step()
        if all([function.status for function in self.functions]):
            self.running = False

        

