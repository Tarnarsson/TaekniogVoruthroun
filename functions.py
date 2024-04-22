###############################
#using python 3.10.0 64-bit
###############################
import mesa
from math import ceil
from random import triangular, random
from information import Info
from designer import Designer
from equations import work_efficiency, technical_complexity, calc_goodness, calc_actual_effort
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
        self.r = 0
        self.E_t_actual = calc_actual_effort(E_t_plan=self.E_t_plan, l=l, r=self.r)

    def work_on(self, function_id: int):
        if self.work_todo - self.function.W > 0:
            self.work_todo -= self.function.W
            self.work_done += self.function.W
        else:
            self.work_done += self.work_todo
            self.work_todo = 0 
        if self.work_todo == 0:
            self.task_status = True
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
 
        self.E_f_plan = triangular(1,3,2)*self.complexity #EQ (4)
        self.num_tasks = ceil(self.E_f_plan/4) #EQ (5) 
        self.E_t_plan = self.E_f_plan/self.num_tasks #EQ (6)
 
        self.tasks = [Task(task_id=i, E_t_plan=self.E_t_plan, function = self) for i in range(self.num_tasks)]
        self.W = None
        self.function_status = False
 
        self.Parent = None
 
        self.information_recieved = []
        self.dependant_functions = [] #TODO make tree
 
        self.subfunctions = [] #TODO make tree
 
        self.Q_T = 0
        self.Q_I = 0
        self.Q_G = 0

        self.can_start = False

        self.in_consultation = False
    
    def work_on(self) -> bool:
        if not self.W:
            #print(f"this is k_n {self.k_n} and it should not be equal to {self.designer.a_n}")

            self.W = work_efficiency(k_n = self.k_n, a_n = self.designer.a_n)

        if self.on_task < self.num_tasks:
            task = self.tasks[self.on_task]
            task.work_on(function_id = self.function_id)
            if task.task_status: 
                self.on_task += 1
                self.H = self.on_task/self.num_tasks
                self.update_quality()
                #print(f"##################Task {self.on_task+1}/{self.num_tasks+1} in function {self.function_id+1} is finished####################")
        else:
            task = self.tasks[self.num_tasks-1] 
        return task.task_status #buið eða ekki #TODO
        
    def rework(self, rework_start: int):
        self.on_task = rework_start
        self.function_status = False
        self.H = self.on_task/self.num_tasks
        for task in self.tasks[rework_start:]:
            task.r += 1
            task.work_todo = calc_actual_effort(E_t_plan=task.E_t_plan, l=l, r=task.r)
            task.work_done = 0
            task.task_status = False

    def update_quality(self):
        self.Q_T = self.W
        self.Q_I = self.designer.product_knowledge[self.function_id]
        self.Q_G = calc_goodness(self)


