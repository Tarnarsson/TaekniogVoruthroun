###############################
#using python 3.10.0 64-bit
###############################
import mesa
import time
from random import triangular, random

l = .05

class Task:
    def __init__(self, task_id: int, E_t_plan: float):
        self.task_id = task_id
        self.E_t_plan = E_t_plan



class Function(mesa.Agent):
    """The functions that the designer has to finish, it should be a cumulation of N tasks"""
    def __init__(self, unique_id: int, model: mesa.Model, complexity: float): 
       super().__init__(unique_id, model) 
       self.unique_id = unique_id
       self.complexity = complexity
       self.E_f_plan = triangular(1,10,5)*self.complexity
       self.num_tasks = round(self.E_f_plan/4)
       self.E_t_plan = self.E_f_plan/self.num_tasks

       self.tasks = [Task(task_id=i, E_t_plan=self.E_t_plan) for i in range(self.num_tasks)]  # Initialize tasks # Hér þarf að reikna complexity.

    
    def step(self) -> None:
        #print(f"I am function number {str(self.unique_id)}")
        for i in range(self.num_tasks):
            r = 0
            task_time = self.tasks[i].E_t_plan
            time.sleep(task_time)
            print(f"performed tasks {self.tasks[i].task_id+1} with complexity {task_time}")

            while random() >= .5: #####Breyta í 0.05 
                r += 1
                time.sleep(task_time*(1-l)**r)
                print(f"task {self.tasks[i].task_id+1} is repeated {r+1} times now with complexity {task_time*(1-l)**r}")

        print(f"##################Function {self.unique_id+1} is finished####################")



if __name__ == "__main__":

    print("Hello")

