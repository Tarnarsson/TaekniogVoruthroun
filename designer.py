###############################
#using python 3.10.0 64-bit
###############################
import mesa
from typing import List
from information import Info
import random
from random import triangular
from equations import integration_complexity


class Designer(mesa.Agent):
    def __init__(self, unique_id: int, model: mesa.Model, a_n: List[float], product_knowledge: List[float]): 
        super().__init__(unique_id, model)
        self.unique_id = unique_id
        self.product_knowledge = product_knowledge
        self.function = None 
        self.a_n = a_n

        # Initialize the value of knowledge 

    def send_information(self):
        effort_read = (self.function.num_tasks - self.function.on_task)*triangular(1,10,5) #EQ16 
        information = Info(function = self.function, Q_I = self.function.Q_I, Q_G = self.function.Q_G, H = self.function.H, effort_read=effort_read)
        for dependant_function in self.function.dependant_functions:
            dependant_function.information_recieved.append(information)

    def read_information(self, information:Info):
        information_type = "Parent" if information.function in self.function.subfunctions else "Interdependant"

        if information_type == "Parent":
            if information.Q_G < 0.95:
                if information.H == 1.0:
                    #self.model.send_consultation request
                    return "Consult" # TODO send consultation request
                return "Wait"
            else: 
                information.function.function_status = True
                return "Good"
            
            
        if information_type == "Interdependant":
            if information.Q_I < random.random():
                return "Consult" # TODO  send consultation request.
            return "Good"
        
    def check_information(self):
        for information in self.function.information_recieved:
            result = self.read_information(information=information)
            if result == "Consult":
                break

    def calc_product_knowledge(self)-> float:
        #returns .5 as is cause all pks are .5
        IC_PK_tmp = 0.0
        IC_tmp = 0.0
        for function in self.function.dependant_functions:
            IC_i = integration_complexity(V_vector=self.function.k_n, U_vector=function.k_n)
            IC_PK_tmp += (IC_i*function.designer.product_knowledge[function.function_id])
            IC_tmp += IC_i
        if IC_tmp == 0: #TODO how to deal with non dependant functions
            PK = 1
        else: 
            PK = IC_PK_tmp/IC_tmp
        #print(f"PK is {PK}")
        return PK

    def calc_goodness_of_input_info(self)-> float:
        IC_PK_tmp = 0.0
        IC_tmp = 0.0
        for function in self.function.dependant_functions:
            IC_i = integration_complexity(V_vector=self.function.k_n, U_vector=function.k_n)
            IC_PK_tmp += (IC_i*function.Q_G)
            IC_tmp += IC_i
        if IC_tmp == 0: #TODO how to deal with non dependant functions
            PK = 1
        else: 
            PK = IC_PK_tmp/IC_tmp
        #print(f"PK is {PK}")
        return PK     

    def step(self):
        assert self.function
        #print(f"I am designer agent number {str(self.unique_id)}")
        self.calc_product_knowledge()
        self.calc_goodness_of_input_info()
        if not self.function.function_status:
            self.check_information()
            task_status = self.function.work_on()
            if task_status:
                self.send_information()
        else:
            print(f"Function done by designer: {self.unique_id}")
            self.model.schedule.remove(self)




if __name__ == "__main__":
    print(Designer(1))

