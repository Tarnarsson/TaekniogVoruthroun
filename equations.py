import random


random.seed(3)

V = {}
knowledge_requirement = [.5,.5,1,1,1,1,1,1,1,2]

def technical_complexity(unique_id: int) -> float:
    # Calculates the technical complexity of function with a unique_id
    knowledge = knowledge_dict(unique_id=unique_id)
    TC = (sum([value**2 for value in knowledge[unique_id]])/len(knowledge[unique_id]))**0.5 # EQ (1)
    #print(f"Created function {unique_id} with knowledge vector {knowledge[unique_id]} and technical complexity {TC}")
    return TC

def knowledge_dict(unique_id: int) -> dict:
    # Wanted to use this to create both knowledge requirements for task and for designer knowledge 
    #### But if the unique id is the same for function and designer this might be problematic
    if unique_id not in V:
        shuffled_knowledge = knowledge_requirement.copy()
        random.shuffle(shuffled_knowledge)
        V[unique_id] = shuffled_knowledge
    return V

def integration_complexity(unique_id1 :int, unique_id2 :int) -> int:
    #Number of interfaces between function 1 and 2
    NF = 2 ### Ekki viss með þetta
    
    IC = 0.5 * NF * knowledge_difference(unique_id1=unique_id1, unique_id2=unique_id2) # EQ (3)

def knowledge_difference(unique_id1 :int, unique_id2 :int)-> int:
    #This function should fetch two knowledge vectors and return a value on the knowledge difference
    V_vector = V[unique_id1]
    U_vector = V[unique_id2]
    r = 2 # upper limit of knowledge scale

    KD = r**((1-(sum(v * u for v, u in zip(V_vector, U_vector))  /  (len(V_vector)*len(U_vector)))**2)**0.5)
    return KD 

def work_efficiency(k_n,a_n) -> int:
    for index, value in enumerate(k_n):
        if value < 1:
            k_n.pop(index)
            a_n.pop(index)

    W = 1/8 * sum(min(1, a/k) for a, k in zip(a_n, k_n))
    print(f"k_n : {k_n} and a_n : {a_n} with work efficiency of {W}")
    return W


if __name__ == "__main__":

    knowledge_dict(1)
    knowledge_dict(2)
    knowledge_dict(3)
    knowledge_dict(4)
    work_efficiency(1)
    work_efficiency(2)
    print(knowledge_difference(1,2))

