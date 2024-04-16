###############################
#using python 3.10.0 64-bit
###############################
import mesa
import random
import pandas as pd
from functions import Function
from designer import Designer
from equations import technical_complexity, shuffle_knowledge

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

            a_n = shuffle_knowledge()
            a_designer = Designer(unique_id = i, model =  self, a_n = a_n, product_knowledge=product_knowledge)
            k_n = shuffle_knowledge()
            a_function = Function(function_id = i, model = self, k_n = k_n, designer = a_designer) 

            self.designers.append(a_designer)
            self.functions.append(a_function)

            self.schedule.add(a_designer)
            a_designer.function = a_function
            self.designers_function[a_designer] = a_function
            a_function.designer = a_designer          


        #TODO Make tree . for function in funcitons append... functions
        """for function in self.functions[:-1]:
            subfunction = self.functions[function.function_id+1]
            function.subfunctions.append(subfunction)"""
        
        # Create a tree of functions from the dataframe
        for index, row in df.iterrows():
            if not pd.isnull(row['subfunctions']):
                subfunctions = [int(x) for x in row['subfunctions'].split(',')]
                dependant_functions = [int(x) for x in row['interdependent_functions'].split(',')]
                self.functions[index].Parent = row['Parent']
                for dependant_function in dependant_functions:
                    self.functions[index].dependant_functions.append(self.functions[dependant_function])
                for subfunction in subfunctions:
                    self.functions[index].subfunctions.append(self.functions[subfunction])


    def step(self):
        self.schedule.step()
        if all([function.function_status for function in self.functions]):
            self.running = False

        

    #TODO def consultation request