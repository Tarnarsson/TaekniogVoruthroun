###############################
#using python 3.10.0 64-bit
###############################
import mesa
from typing import List

class Designer(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, knowledge_ability: List[int], a_n: List[float]): 
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.knowledge_ability = knowledge_ability
        self.function = None
        self.a_n = a_n
        # Initialize the value of knowledge 


        

    def step(self):
        assert self.function
        #print(f"I am designer agent number {str(self.unique_id)}")
        if not self.function.status:
            task_status = self.function.work_on()
        else:
            print(f"Function done by designer: {self.unique_id}")
            self.model.schedule.remove(self)
        # if function.status er buið:
            #senda info
        # akveða hvort info er sent




if __name__ == "__main__":
    print(Designer(1))

