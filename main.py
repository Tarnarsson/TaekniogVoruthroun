import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from mesamodel import Mesamodel



if __name__ == "__main__":

    starter_model = Mesamodel(57)
    for i in range(5):
        starter_model.step()
        print(f"step {i} has been run")


