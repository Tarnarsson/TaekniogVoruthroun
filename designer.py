###############################
#using python 3.10.0 64-bit
###############################
import mesa

class Designer(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model): #knowledge_ability
        super().__init__(unique_id, model)

        # Initialize the value of knowledge 
        """Might be better to have a list of knowledge"""
        #self.knowledge_ability: list[int] = [] 

    def step(self):
        print(f"I am designer agent number {str(self.unique_id)}")




if __name__ == "__main__":
    print(Designer(1))

