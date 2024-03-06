###############################
#using python 3.10.0 64-bit
###############################
import mesa
from functions import Function
from designer import Designer

class Mesamodel(mesa.Model):
    def __init__(self, N: int):
        super().__init__()
        self.num_agents = N
        self.schedule = mesa.time.BaseScheduler(self) #aðrar aðferðir RandomActivation eða SimultaneousActivation

        for i in range(N):
            a_function = Function(i, self, 3) #i er identity af agentinum, self þarf að vera þarna en svo er hægt að passa fleiri args eftir það.
            a_designer = Designer(i+N, self)
            self.schedule.add(a_function)
            self.schedule.add(a_designer)


    def step(self):
        self.schedule.step()


