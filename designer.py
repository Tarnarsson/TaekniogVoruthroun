###############################
#using python 3.10.0 64-bit
###############################
import mesa
from typing import List, TYPE_CHECKING
from information import Info
import random
from random import triangular
from math import ceil
from equations import update_product_knowledge,update_general_knowledge, integration_complexity
if TYPE_CHECKING:
    from mesamodel import Mesamodel

class Designer(mesa.Agent):
    def __init__(self, unique_id: int, model: "Mesamodel", a_n: List[float], product_knowledge: List[float]): 
        super().__init__(unique_id, model)
        self.model = model
        self.unique_id = unique_id
        self.product_knowledge = product_knowledge
        self.function = None 
        self.a_n = a_n
        self.consultation_partner = None

    def send_information(self):
        effort_read = (self.function.num_tasks - self.function.on_task)*triangular(1,10,5) #EQ16 
        information = Info(function = self.function, Q_I = self.function.Q_I, Q_G = self.function.Q_G, H = self.function.H, effort_read=effort_read)
        for dependant_function in self.function.dependant_functions:
            dependant_function.information_recieved = [i for i in  dependant_function.information_recieved if i.function != self.function]
            dependant_function.information_recieved.append(information)

    def read_information(self, information:Info):
        information_type = "Parent" if information.function in self.function.subfunctions else "Interdependant"

        if information_type == "Parent":
            print(f"Q_g is  {information.Q_G} ################### {information.function.function_id}")
            if information.Q_G < 0.95:
                if information.H == 1.0:
                    #self.model.send_consultation request
                    return "Consult" # TODO send consultation request
                return "Wait"
            else: 
                print(f"changing function status in {self.function.function_id}")
                information.function.function_status = True
                self.check_start()
                return "Good"
                     
        if information_type == "Interdependant":
            if information.Q_I < random.random():
                self.model.product_consultation_request(requester=self, incompatible=information.function)
                return "Consult" 
            return "Good"
        
    def check_information(self):
        for information in self.function.information_recieved:
            result = self.read_information(information=information)
            if result == "Consult":
                break

    def consult_on_product_knowledge(self):
        IC = integration_complexity(V_vector=self.function.k_n, U_vector=self.consultation_partner.function.k_n)
        E_cnslt = triangular(1,3,2)
        for function in [self.function, self.consultation_partner.function]:
            self.product_knowledge[function.function_id] = update_product_knowledge(PK_in = self.product_knowledge[function.function_id],IC=IC,E_cnslt=E_cnslt)
        rework_start = self.function.num_tasks  - ceil((1-self.function.Q_I)*self.function.num_tasks)
        self.function.rework(rework_start=rework_start)
        self.function.update_quality()
        self.function.in_consultation = False
                
    def consult_on_general_knowledge(self):
        E_cnslt =triangular(1,3,2)
        for i in range(len(self.a_n)):
            self.a_n[i] = update_general_knowledge(X_n = self.consultation_partner.a_n[i] ,a_n_in = self.a_n[i], E_cnslt=E_cnslt, TC=self.function.complexity)
        self.function.in_consultation = False
        
    def check_start(self):
        if all(subfunction.function_status for subfunction in self.function.subfunctions):
            self.function.can_start = True

    def perform_technical_review(self)-> bool:
        print(f"Performing TC")
        print(f"function id {self.function.function_id}, designer: {self.unique_id}")
        print(f"Q_t: {self.function.Q_T}")
        rework_start = None
        for i in range(self.function.num_tasks):
            if self.function.Q_T < random.random():
                print(f"Failed on task {i}")
                rework_start = i
                break
        if rework_start == None:
            print(f"Review passed")
            return True
        self.function.rework(rework_start)
        self.model.general_consultation_request(self)
        return False
        
    def step(self):
        assert self.function
        #print(f"I am designer agent number {str(self.unique_id)}")
        if self.function.in_consultation:
            self.consult_on_product_knowledge()
            return

        if not self.function.can_start:
            self.check_information()
            if not self.function.can_start:
                #print(f"WE ARE HERE {self.function.function_id+1}")
                return

        if not self.function.function_status:
            self.check_information()
            task_status = self.function.work_on()
            if task_status:
                if self.function.H == 1:
                    if self.perform_technical_review():
                        if self.function.Parent != None:
                            self.send_information()
                        else:
                            self.function.function_status = True
                elif 0.75 < random.random(): #TODO communication breyta
                    self.send_information()
        else:
            #print(f"Function done by designer: {self.unique_id}")
            self.model.schedule.remove(self)
