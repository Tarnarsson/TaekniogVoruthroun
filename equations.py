import random
from typing import List
from math import e

def technical_complexity(unique_id: int, knowledge_vec: List[float]) -> float:
    # Calculates the technical complexity of function with a unique_id
    #knowledge = knowledge_dict(unique_id=unique_id)
    TC = (sum([value**2 for value in knowledge_vec])/len(knowledge_vec))**0.5 # EQ (1)
    #print(f"Created function {unique_id} with knowledge vector {knowledge[unique_id]} and technical complexity {TC}")
    return TC

def shuffle_knowledge()->List[float]:
    shuffled_knowledge = [.5,.5,1,1,1,1,1,1,1,2].copy()
    random.shuffle(shuffled_knowledge)
    return shuffled_knowledge

def integration_complexity(V_vector: List[float], U_vector: List[float]) -> int:
    #Number of interfaces between function 1 and 2
    NF = 2  
    IC = 0.5 * NF * knowledge_difference(V_vector=V_vector, U_vector=U_vector) # EQ (3)
    return IC

def knowledge_difference(V_vector: List[float], U_vector: List[float])-> int:
    #This function should fetch two knowledge vectors and return a value on the knowledge difference
    r = 2 # upper limit of knowledge scale
    KD = r**((1-(sum(v * u for v, u in zip(V_vector, U_vector))  /  (len(V_vector)*len(U_vector)))**2)**0.5) #EQ (2)
    return KD 

def work_efficiency(k_n, a_n) -> int:
    # Use list comprehension to filter out elements where k_n value is less than 1
    filtered_pairs = [(k, a) for k, a in zip(k_n, a_n) if k >= 1]

    # Unzip the pairs back into two lists
    k_n_filtered, a_n_filtered = zip(*filtered_pairs) if filtered_pairs else ([], [])

    # Convert tuples back to lists if necessary
    k_n_filtered = list(k_n_filtered)
    a_n_filtered = list(a_n_filtered)

    # Calculate work efficiency based on filtered lists
    # Assuming the rest of the work_efficiency calculation goes here
    W = 1/8 * sum(min(1, a/k) for a, k in zip(a_n_filtered, k_n_filtered))
    #print(f"k_n : {k_n_filtered} and a_n : {a_n_filtered} with work efficiency of {W}")
    return W
    
def Q_Goodness(Q_G_input: float, PK: float, H: float)-> float: #EQ 12
    alpha = 50
    beta = 10
    Q_G = Q_G_input/(1+alpha*e**(-beta*PK*H))
    return Q_G



if __name__ == "__main__":
    print()

"""    knowledge_dict(1)
    knowledge_dict(2)
    knowledge_dict(3)
    knowledge_dict(4)
    work_efficiency(1)
    work_efficiency(2)
    print(knowledge_difference(1,2))"""

