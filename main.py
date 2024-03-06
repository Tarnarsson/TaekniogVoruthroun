import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from mesamodel import Mesamodel


if __name__ == "__main__":

    starter_model = Mesamodel(2)
    for i in range(3):
        starter_model.step()
    print(f"step has been run")

