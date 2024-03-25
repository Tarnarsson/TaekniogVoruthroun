###############################
#using python 3.10.0 64-bit
###############################
import mesa
from functions import Function
from designer import Designer
from equations import technical_complexity


designers_function = {}

class Mesamodel(mesa.Model):
    def __init__(self, N: int):
        super().__init__()
        self.num_agents = N
        self.schedule = mesa.time.BaseScheduler(self) #aðrar aðferðir RandomActivation eða SimultaneousActivation

        for i in range(N):
            
            a_designer = Designer(unique_id = i+N, model =  self, knowledge_ability= technical_complexity(unique_id=i+N))
            a_function = Function(function_id = i, model = self, complexity = technical_complexity(unique_id = i)) #i er identity af agentinum, self þarf að vera þarna en svo er hægt að passa fleiri args eftir það.
            self.schedule.add(a_designer)
            self.schedule.add(a_function)

            #nota dict til að halda utan um Designer og Function
            


    def step(self):
        self.schedule.step()

        

