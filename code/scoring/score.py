from pathlib import Path

# Get the parent directory of the current file
parent_dir = Path(__file__).resolve().parent.parent

# Add the parent directory to the Python module search path
import sys
sys.path.append(str(parent_dir))


import subprocess

# Log installed Python packages
subprocess.run(['pip', 'list'])

import pickle
import json
import numpy
import torch
from training.model import Net
from azureml.core.model import Model
from load.load_data import data_loading


def get_input():
    trainloader=data_loading()
    first_batch_inputs, first_batch_labels = next(iter(trainloader))
    return first_batch_inputs


def run(input):
    net= Net()
    net.load_state_dict(torch.load('./models/model_1.pth'))
    with torch.no_grad():
        probabilities = F.softmax(net(input),dim=1)
        predictions= torch.argmax(probabilities,dim=1)
        print(predictions)
        return predictions


if __name__ == "__main__":
    model_path = Model.get_model_path(model_name="pytorch_model.pth")
    # Test scoring
    inputs=get_input()
    predictions = run(inputs)
    print("Test result: ", predictions)
