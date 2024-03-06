###############################
#using python 3.10.0 64-bit
###############################
import mesa
import time
from random import triangular

class Task:
    def __init__(self, task_id, complexity):
        self.task_id = task_id
        self.complexity = complexity


class Function(mesa.Agent):
    """The functions that the designer has to finish, it should be a cumulation of N tasks"""
    def __init__(self, unique_id: int, model: mesa.Model, num_tasks: int): 
       super().__init__(unique_id, model) 
       self.unique_id = unique_id
       self.num_tasks = num_tasks
       self.tasks = [Task(task_id=i, complexity=round(triangular(1,10,5))) for i in range(num_tasks)]  # Initialize tasks # Hér þarf að reikna complexity.

    
    def step(self) -> None:
        #print(f"I am function number {str(self.unique_id)}")
        for i in range(self.num_tasks):
            time.sleep(self.tasks[i].complexity)
            print(f"performed tasks {self.tasks[i].task_id} with complexity {self.tasks[i].complexity}")



if __name__ == "__main__":

    print("Hello")

