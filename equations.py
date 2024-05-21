import random
from typing import List, TYPE_CHECKING
from math import e
if TYPE_CHECKING:
    from functions import Function

def technical_complexity( knowledge_vec: List[float]) -> float:
    TC = (sum([value**2 for value in knowledge_vec])/len(knowledge_vec))**0.5 # EQ (1)
    return TC

def shuffle_knowledge_k()->List[float]:
    shuffled_knowledge = [.5,.5,.5,.5,1,1,1,1,1,2].copy()
    random.shuffle(shuffled_knowledge)
    return shuffled_knowledge

def shuffle_knowledge_a()->List[float]:
    shuffled_knowledge = [.5,.5,1,1,1,1,2,2,2,2].copy()
    random.shuffle(shuffled_knowledge)
    return shuffled_knowledge

def integration_complexity(V_vector: List[float], U_vector: List[float]) -> float:
    #Number of interfaces between function 1 and 2 , could be 1-3 according to Zhang
    NF = 3 
    IC = 0.5 * NF * knowledge_difference(V_vector=V_vector, U_vector=U_vector) # EQ (3)
    return IC

def knowledge_difference(V_vector: List[float], U_vector: List[float])-> float:
    #This function should fetch two knowledge vectors and return a value on the knowledge difference
    r = 2 # upper limit of knowledge scale
    KD = r**((1-(sum(v * u for v, u in zip(V_vector, U_vector))  /  (len(V_vector)*len(U_vector)))**2)**0.5) #EQ (2)
    return KD 

def work_efficiency(k_n, a_n) -> float:
    # Use list comprehension to filter out elements where k_n value is less than 1
    filtered_pairs = [(k, a) for k, a in zip(k_n, a_n) if k > 0.5]

    # Unzip the pairs back into two lists
    k_n_filtered, a_n_filtered = zip(*filtered_pairs) if filtered_pairs else ([], [])

    # Convert tuples back to lists if necessary
    k_n_filtered = list(k_n_filtered)
    a_n_filtered = list(a_n_filtered)

    # Calculate work efficiency based on filtered lists
    # Assuming the rest of the work_efficiency calculation goes here
    W = 1/len(k_n_filtered) * sum(min(1, a/k) for a, k in zip(a_n_filtered, k_n_filtered))
    return W

def calc_product_knowledge(function: "Function")-> float:
    IC_PK_tmp = 0.0
    IC_tmp = 0.0
    for f in function.dependant_functions:
        IC_i = integration_complexity(V_vector=function.k_n, U_vector=f.k_n)
        IC_PK_tmp += (IC_i*function.designer.product_knowledge[f.function_id])
        IC_tmp += IC_i
    if IC_tmp == 0: #TODO how to deal with non dependant functions
        PK = function.designer.product_knowledge[function.function_id]
    else: 
        PK = IC_PK_tmp/IC_tmp
    return PK

def calc_goodness_of_input_info(function: "Function")-> float:
    Q_G_i_tmp = 0.0
    IC_tmp = 0.0
    for subfunction in function.subfunctions:
        IC_i = integration_complexity(V_vector=function.k_n, U_vector=subfunction.k_n)
        Q_G_i_tmp += (IC_i*subfunction.Q_G)
        IC_tmp += IC_i
    if IC_tmp == 0: #TODO how to deal with non dependant functions
        Q_G_input = 1
    else: 
        Q_G_input = Q_G_i_tmp/IC_tmp
    return Q_G_input   

def calc_goodness(function: "Function")->float:
    alpha = 100
    beta = 10
    up = calc_goodness_of_input_info(function=function)
    down = (1+alpha*e**(-beta*calc_product_knowledge(function=function)*function.H))
    return up/down

def update_product_knowledge(PK_in: float, IC: float, E_cnslt: float) -> float:
    delta = 3
    s = 0.1
    return 1/(1 + (1/PK_in - 1) * e**(-(delta*s*E_cnslt)/IC)) #EQ 15

def update_general_knowledge(X_n: float, a_n_in: float, E_cnslt: float, TC: float)-> float:
    gamma = 3
    s = 0.1
    return X_n/(1 + (X_n/a_n_in - 1)*e**-((gamma*s*E_cnslt)/TC))

def calc_actual_effort(E_t_plan: float ,l: float,r: int) -> float:
    return E_t_plan * (1-l)**r



