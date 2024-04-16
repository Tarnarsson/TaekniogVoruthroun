###############################
#using python 3.10.0 64-bit
###############################
import mesa
import time
from random import triangular, random
from information import Info
from designer import Designer
from equations import work_efficiency, technical_complexity
from typing import List

#Learning factor
l = .05



class Task:
    def __init__(self, task_id: int, E_t_plan: float, function):
        self.function = function
        self.task_id = task_id
        self.E_t_plan = E_t_plan
        self.work_todo = E_t_plan
        self.work_done = 0
        self.task_status = False
        # create method work on

    def work_on(self, function_id: int):
        if self.work_todo - self.function.W > 0:# Verði  ekki <0 #TODO
            self.work_todo -= self.function.W
            self.work_done += self.function.W
        else:
            self.work_done += self.work_todo
            self.work_todo = 0 
            # Verði ekki > E_t_plan #TODO
        if self.work_todo == 0:
            self.task_status = True


        self.Q_I = 0
        self.Q_G = 0
        self.Q_T = 0

        print(f"working on task {self.task_id+1} in function {function_id+1}")
        return self.task_id


class Function(mesa.Agent):
    # The functions that the designer has to finish, it should be a cumulation of N tasks
    def __init__(self, function_id: int, model: mesa.Model, k_n: List[float], designer: Designer): 
       super().__init__(function_id, model) 
       self.designer = designer #TODO
       self.function_id = function_id
       self.k_n = k_n
       self.complexity = technical_complexity(unique_id = self.function_id, knowledge_vec = self.k_n)

       self.on_task = 0
       self.H = 0

       self.E_f_plan = triangular(1,100,30)*self.complexity #EQ (4)
       self.num_tasks = round(self.E_f_plan/4) #EQ (5) 
       self.E_t_plan = self.E_f_plan/self.num_tasks #EQ (6)

       self.tasks = [Task(task_id=i, E_t_plan=self.E_t_plan, function = self) for i in range(self.num_tasks)]
       self.W = None
       self.function_status = False

       self.Parent = None

       self.information_recieved = []
       self.dependant_functions = [] #TODO make tree

       self.subfunctions = [] #TODO make tree

    
    def work_on(self) -> bool:
        if not self.W:
            print(f"this is k_n {self.k_n} and it should not be equal to {self.designer.a_n}")

            self.W = work_efficiency(k_n = self.k_n, a_n = self.designer.a_n)

        task = self.tasks[self.on_task]
        task.work_on(function_id = self.function_id)

        if task.task_status: 
            self.on_task += 1
            self.H = self.on_task/self.num_tasks
            self.update_quality()
            print(f"##################Task {self.on_task+1}/{self.num_tasks+1} in function {self.function_id+1} is finished####################")

            
            print(self.H)
        
        #if self.H == 1.0:
        #    self.function_status = True

        
        return task.task_status #buið eða ekki #TODO
        


    def update_quality(self):
        self.Q_T = self.W
        self.Q_I = self.designer.product_knowledge[self.function_id]
        self.Q_G = .96 #TODO make Q_G


        #when work on is finished send information
            


        
        #AS IS: each step is performing a function
        #print(f"I am function number {str(self.function_id)}")

        #print(f"performed tasks {self.tasks[i].task_id+1} with complexity {task_time} and the progress of technical work H is {self.H}")

        #print(f"task {self.tasks[i].task_id+1} is repeated {r+1} times now with complexity {task_time*(1-l)**r}")




if __name__ == "__main__":

    print("Hello")

