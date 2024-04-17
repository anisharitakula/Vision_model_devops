import os, json, sys
from azureml.core import Workspace, Environment
#from azureml.core.image import ContainerImage, Image
from azureml.core.model import Model
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.container_registry import ContainerRegistry
from azureml.core import Image
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
image_config = ContainerRegistry()
image = Image.create(workspace=ws,
                     name="pytorch-vision-image",
                     models=[],
                     image_config=image_config,
                     workspace=ws)

image.wait_for_creation(show_output=True)
os.chdir("../..")

if image.creation_state != "Succeeded":
    raise Exception("Image creation status: {image.creation_state}")

print(
    "{}(v.{} [{}]) stored at {} with build log {}".format(
        image.name,
        image.version,
        image.creation_state,
        image.image_location,
        image.image_build_log_uri,
    )
)
# Publish environment to Azure ML Studio
env_docker_conda.publish(workspace=ws)

# Writing the image details to /aml_config/image.json
image_json = {}
image_json["image_name"] = image.name
image_json["image_version"] = image.version
image_json["image_location"] = image.image_location
with open("aml_config/image.json", "w") as outfile:
    json.dump(image_json, outfile)
