###############################
#using python 3.10.0 64-bit
###############################
import mesa
from math import ceil
from random import triangular
from designer import Designer
from equations import work_efficiency, technical_complexity, calc_goodness, calc_actual_effort, integration_complexity
from typing import List

#Learning factor
l = .9

class Task:
    def __init__(self, task_id: int, E_t_plan: float, function: "Function"):
        self.function = function
        self.task_id = task_id
        self.E_t_plan = E_t_plan
        self.work_todo = E_t_plan
        self.work_done = 0
        self.task_status = False
        self.r = 0
        self.E_t_actual = calc_actual_effort(E_t_plan=self.E_t_plan, l=l, r=self.r)

    def work_on(self):

        if self.work_todo - self.function.W > 0:
            self.work_todo -= self.function.W
            self.work_done += self.function.W
            self.function.designer.effort_working_on_task += self.function.W
            if self.r > 0:
                self.function.designer.effort_rework += self.function.W
        else:
            self.work_done += self.work_todo
            self.work_todo = 0 
            self.function.designer.effort_working_on_task += self.work_todo
            if self.r > 0:
                self.function.designer.effort_rework += self.work_todo
        if self.work_todo == 0:
            self.task_status = True
            self.function.designer.tasks_completed += 1
            if self.r > 0:
                self.function.designer.tasks_reworked += 1
        return self.task_id


class Function(mesa.Agent):
    # The functions that the designer has to finish, should be a cumulation of N tasks
    def __init__(self, function_id: int, model: mesa.Model, k_n: List[float], designer: Designer): 
        super().__init__(function_id, model) 
        self.designer = designer
        self.function_id = function_id
        self.k_n = k_n
        self.complexity = technical_complexity(knowledge_vec = self.k_n)
 
        self.on_task = 0
        self.H = 0
 
        self.E_f_plan = triangular(10,30,25)*self.complexity #EQ (4)
        self.num_tasks = ceil(self.E_f_plan/4) #EQ (5) 
        self.E_t_plan = self.E_f_plan/self.num_tasks #EQ (6)
 
        self.tasks = [Task(task_id=i, E_t_plan=self.E_t_plan, function = self) for i in range(self.num_tasks)]
        self.W = None
        self.function_status = False
 
        self.Parent = None
 
        self.information_recieved = []
        self.dependant_functions = [] 
 
        self.subfunctions = [] 
 
        self.Q_T = 0
        self.Q_I = 0
        self.Q_G = 0

        self.can_start = False

    
    def work_on(self) -> bool:
        if not self.W:
            self.W = work_efficiency(k_n = self.k_n, a_n = self.designer.a_n)

        if self.on_task < self.num_tasks:
            task = self.tasks[self.on_task]
            task.work_on()
            if task.task_status: 
                self.on_task += 1
                self.H = self.on_task/self.num_tasks
                self.update_quality()
        else:
            task = self.tasks[self.num_tasks-1] 
        return task.task_status 
        
    def rework(self, rework_start: int) -> None:
        self.on_task = rework_start
        self.designer.tasks_completed -= (self.num_tasks - rework_start)
        self.function_status = False
        self.H = self.on_task/self.num_tasks
        for task in self.tasks[rework_start:]:
            task.r += 1
            task.work_todo = calc_actual_effort(E_t_plan=task.E_t_plan, l=l, r=task.r)
            task.work_done = 0
            task.task_status = False

    def unresolved_complexity(self) -> float:
     if self.function_status == True:
         return (0.0, 0.0)
     TC = self.complexity - self.H * self.complexity
     IC = sum(
         integration_complexity(self.k_n, dependant_function.k_n)
         for dependant_function in self.dependant_functions
         if dependant_function.function_status != True
     )
     return [TC,IC]

    def update_quality(self) -> None:
        old_Q_G = 0
        new_Q_G = 0
        self.Q_T = self.W
        self.Q_I = self.designer.product_knowledge[self.function_id]
        old_Q_G = self.Q_G
        new_Q_G = calc_goodness(self) #TODO if old and new Q_g are eq and pk is over 95%
        if old_Q_G == new_Q_G and self.designer.product_knowledge[self.function_id] > .95: #failsafe
            self.Q_G = .95
        elif self.function_id == 0 and self.designer.function.Q_G < .9: 
            self.Q_G = new_Q_G+0.02
        else: 
            self.Q_G = new_Q_G



