import os
from azureml.core import Experiment
from azureml.core import Workspace
from azureml.core.authentication import AzureCliAuthentication
#cli_auth = AzureCliAuthentication()

def getExperiment():
    # Specify the path to your config.json file
    config_path = 'aml_config/config.json'

    ws = Workspace.from_config(path=config_path)
    #script_folder = "."
    experiment_name = "vision-model-devops"
    exp = Experiment(workspace=ws, name=experiment_name)
    print(exp.name, exp.workspace.name, sep="\n")
    return exp


if __name__ == "__main__":
    exp = getExperiment()