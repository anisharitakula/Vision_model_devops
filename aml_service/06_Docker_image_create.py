import os, json, sys
from azureml.core import Workspace, Environment
#from azureml.core.image import ContainerImage, Image
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.container_registry import ContainerRegistry
from azureml.core import Image
from azureml.core.image import ContainerImage
#cli_auth = AzureCliAuthentication()

# Get workspace
config_path='aml_config/config.json'
ws = Workspace.from_config(path=config_path)

# Get the latest model details

try:
    with open("aml_config/model.json") as f:
        config = json.load(f)
except:
    print("No new model to register thus no need to create new scoring image")
    # raise Exception('No new model to register as production model perform better')
    sys.exit(0)

model_name = config["model_name"]
model_version = config["model_version"]


model_list = Model.list(workspace=ws)
model, = (m for m in model_list if m.version == model_version and m.name == model_name)
print(
    "Model picked: {} \nModel Description: {} \nModel Version: {}".format(
        model.name, model.description, model.version
    )
)

os.chdir("./code/scoring")

env_docker_conda = Environment(
    image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
    conda_file="conda_dependencies.yml",
    name="docker-image-pytorch-vision",
    description="Image with vision model",
)

# Set the post_creation_script property to the script you want to run
env_docker_conda.post_creation_script = "python score.py"

os.chdir("../..")


# Publish environment to Azure ML Studio
# env_docker_conda.publish(workspace=ws)

# Register the environment
env_docker_conda.register(workspace=ws)

# Writing the image details to /aml_config/image.json
image_json = {}
image_json["image_name"] = env_docker_conda.name
image_json["image_version"] = env_docker_conda.version

with open("aml_config/image.json", "w") as outfile:
    json.dump(image_json, outfile)
