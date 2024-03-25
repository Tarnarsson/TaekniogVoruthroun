###############################
#using python 3.10.0 64-bit
###############################
import mesa

class Designer(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, knowledge_ability: list[int]): 
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.knowledge_ability = knowledge_ability
        # Initialize the value of knowledge 


        

    def step(self):
        print(f"I am designer agent number {str(self.unique_id)}")




if __name__ == "__main__":
    print(Designer(1))

