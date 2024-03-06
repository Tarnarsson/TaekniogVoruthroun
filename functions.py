###############################
#using python 3.10.0 64-bit
###############################
import mesa

class Function(mesa.Agent):
    """The functions that the designer has to finish, it should be a cumulation of N tasks"""
    def __init__(self, unique_id: int, model: mesa.Model, additional_arg1: int): 
       super().__init__(unique_id, model) 
       self.unique_id = unique_id
       self.additional_arg1 = additional_arg1

    
    def step(self) -> None:
        print(f"I am function number {str(self.unique_id)}")
        #print(f"additional argument {str(self.additional_arg1)}")

if __name__ == "__main__":

    print("Hello")

