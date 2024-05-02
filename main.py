import warnings
import os
warnings.filterwarnings("ignore", category=FutureWarning)
from mesamodel import Mesamodel
import matplotlib.pyplot as plt


completed_tasks = []
reworked_tasks = []
consultion_effort = []
read_effort = []
prep_effort = []
rework_effort = []
working_on_task_effort = []


if __name__ == "__main__":

    starter_model = Mesamodel(57)
    q_g = [[] for _ in starter_model.designers]
    
    for i in range(3000):
        starter_model.step()
        print(f"step {i} has been run")
        completed_tasks.append(sum([designer.tasks_completed for designer in starter_model.designers]))
        reworked_tasks.append(sum([designer.tasks_reworked for designer in starter_model.designers]))
        consultion_effort.append(sum([designer.effort_consultation for designer in starter_model.designers]))
        read_effort.append(sum([designer.effort_read for designer in starter_model.designers]))
        prep_effort.append(sum([designer.effort_prepare for designer in starter_model.designers]))
        rework_effort.append(sum([designer.effort_rework for designer in starter_model.designers]))
        working_on_task_effort.append(sum([designer.effort_working_on_task for designer in starter_model.designers]))
        #for designer in starter_model.designers: [6, 25, 26, 27, 49, 50, 51]
        #    q_g[designer.unique_id].append(designer.function.Q_G)
        
        for designer in starter_model.designers: 
            if designer.unique_id in [6, 25, 26, 27, 49, 50, 51]:
                q_g[designer.unique_id].append(designer.function.Q_G)


    # Ensure the img directory exists
    if not os.path.exists('img'):
        os.makedirs('img')

    plt.figure(figsize=(10, 5))
    plt.plot(completed_tasks, label='Completed Tasks Over Time', c = 'black')
    #plt.plot(reworked_tasks, label='Reworked Tasks', c = 'red')
    plt.xlabel('Step')
    plt.ylabel('Number of Completed Tasks')
    plt.title('Completed Tasks Throughout the Simulation')
    plt.legend()
    plt.savefig('img/completed_tasks_plot.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    plt.plot(consultion_effort, label='Consultation Effort', c='blue', alpha = 1)
    plt.plot(read_effort, label='Read Effort', c='green', alpha = 1)
    plt.plot(prep_effort, label='Preparation Effort', c='purple', alpha = 1)
    plt.plot(rework_effort, label='Rework Effort', c='orange', alpha = 1)
    plt.plot(working_on_task_effort, label='Working on Task Effort', c='brown', alpha = 1)
    plt.xlabel('Step')
    plt.ylabel('Effort')
    plt.title('Effort Over Time for Different Activities')
    plt.legend()
    plt.savefig('img/effort_over_time.png')
    plt.close()

    plt.figure(figsize=(12, 6))
    for idx, designer_q_g in enumerate(q_g):
        if idx in [6, 25, 26, 27, 49, 50, 51]:
            plt.plot(designer_q_g, label=f'Designer {idx} Q_G Over Time')
    plt.xlabel('Step')
    plt.ylabel('Q_G Value')
    plt.title('General Knowledge Quality (Q_G) Over Time for Each Designer')
    plt.legend()
    plt.savefig('img/q_g_over_time.png')
    plt.close()



