###############################
#using python 3.10.0 64-bit
###############################
import mesa
import time
from random import triangular, random
from information import Info

#Learning factor
l = .05

information = {"H": 0,
               "IC": 0,
               "Q_T": 0,
               "Q_I": 0,
               "Q_G": 0,
               "PK": 0
               }

class Task:
    def __init__(self, task_id: int, E_t_plan: float):
        self.task_id = task_id
        self.E_t_plan = E_t_plan
        self.status = False
        # create method work on

    def work_on(self, function_id: int):
        print(f"working on task {self.task_id+1} in function {function_id+1}")
        return self.task_id


class Function(mesa.Agent):
    # The functions that the designer has to finish, it should be a cumulation of N tasks
    def __init__(self, function_id: int, model: mesa.Model, complexity: float): 
       super().__init__(function_id, model) 
       self.function_id = function_id
       self.complexity = complexity

       self.on_task = 0

       self.H = 0

       self.E_f_plan = triangular(1,10,5)*self.complexity #EQ (4)
       self.num_tasks = round(self.E_f_plan/4) #EQ (5) 
       self.E_t_plan = self.E_f_plan/self.num_tasks #EQ (6)

       self.tasks = [Task(task_id=i, E_t_plan=self.E_t_plan) for i in range(self.num_tasks)]  

       self.information = {}

    
    def step(self) -> None:
        if self.on_task == 0: #one information dict for each function.
            self.information = Info(information=information)
        #current task working in
        Task = self.tasks[self.on_task]
        Task.work_on(function_id = self.function_id)
        

        #when work on is finished send information
            


        
        #AS IS: each step is performing a function
        #print(f"I am function number {str(self.function_id)}")

        #print(f"performed tasks {self.tasks[i].task_id+1} with complexity {task_time} and the progress of technical work H is {self.H}")

        #print(f"task {self.tasks[i].task_id+1} is repeated {r+1} times now with complexity {task_time*(1-l)**r}")

        print(f"##################Task number {self.on_task+1} in function {self.function_id+1} is finished####################")
        self.on_task += 1



if __name__ == "__main__":

    print("Hello")

