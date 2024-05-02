###############################
#using python 3.10.0 64-bit
###############################
import mesa
import random
import pandas as pd
from functions import Function
from designer import Designer
from equations import technical_complexity, shuffle_knowledge_a, shuffle_knowledge_k
from  typing import Optional

df = pd.read_excel('Zhang_Thomson.xlsx')

class Mesamodel(mesa.Model):
    def __init__(self, N: int):
        super().__init__()
        self.designers = []
        self.functions = [] 
        self.num_agents = N
        self.schedule = mesa.time.BaseScheduler(self) #aðrar aðferðir RandomActivation eða SimultaneousActivation

        self.designers_function = {}

        for i in range(N):
            product_knowledge = [.5]*N

            a_n = shuffle_knowledge_a()
            a_designer = Designer(unique_id = i, model = self, a_n = a_n, product_knowledge=product_knowledge)
            k_n = shuffle_knowledge_k()
            a_function = Function(function_id = i, model = self, k_n = k_n, designer = a_designer) 

            self.designers.append(a_designer)
            self.functions.append(a_function)

            self.schedule.add(a_designer)
            a_designer.function = a_function
            self.designers_function[a_designer] = a_function
            a_function.designer = a_designer          
        
        # Create a tree of functions from the dataframe
        for index, row in df.iterrows():
            self.functions[index].Parent = row['Parent']
            if not pd.isnull(row['interdependent_functions']):
                dependant_functions = [int(x) for x in row['interdependent_functions'].split(',')]
                for dependant_function in dependant_functions:
                    self.functions[index].dependant_functions.append(self.functions[dependant_function])
            if not pd.isnull(row['subfunctions']):
                subfunctions = [int(x) for x in row['subfunctions'].split(',')]
                for subfunction in subfunctions:
                    self.functions[index].subfunctions.append(self.functions[subfunction])
            else:
                self.functions[index].can_start = True

    def find_expert(self, requester: Designer)->Optional[Designer]:
        best_designer = None
        best_diff = 0
        for designer in self.designers:
            tmp_best_diff = 0
            if designer == requester:
                continue
            for index, number in enumerate(designer.a_n):
                if number > requester.a_n[index]:
                    tmp_best_diff += 1
            if tmp_best_diff > best_diff:
                best_diff = tmp_best_diff
                best_designer = designer
        return best_designer
                
    def general_consultation_request(self, requester: Designer):
        expert = self.find_expert(requester=requester)
        print("### General consultation request ###")
        print(f"\tRequester: {requester.unique_id}")
        print(f"\tReceiver: {expert.unique_id}")
        if expert == None:
            return
        if random.random() < .5: #TODO Breyta
            print(f"Consultation accepted")
            requester.consultation_partner = expert
            requester.in_general_consultation = True

    def product_consultation_request(self,requester: Designer, incompatible: Function):
        reciever = incompatible.designer
        print("### Consultation request ###")
        print(f"\tRequester: {requester.unique_id}")
        print(f"\tIncompatible function: {incompatible.function_id}")
        print(f"\tReceiver: {reciever.unique_id}")
        if random.random() < .5: #TODO Breyta
            requester.consultation_partner = reciever
            reciever.consultation_partner = requester
            requester.in_product_consultation = True
            reciever.in_product_consultation = True

    def print_status(self):
        print("### Status ###")
        print(
                f"\tFunction | function_status | Designer | Q_G | Tasks"
            )
        for i, f in enumerate(self.functions):
            designer_string = (
                f"Designer: {f.designer.unique_id}" if f.designer else "Designer: "
            )
            task_string = (f"{f.on_task+1}/{f.num_tasks}" if f.on_task < f.num_tasks else "DONE")
            function_status = (f"DONE" if f.function_status else f"")
            print(
                f"\tFunction {i:<2}| {function_status:<5}| {designer_string:<13}| {f.Q_G:.2f} | {task_string}"
            )

    def step(self):
        self.schedule.step()
        self.print_status()
        if all([function.function_status for function in self.functions]):
            self.running = False