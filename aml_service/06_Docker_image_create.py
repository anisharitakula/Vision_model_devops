import os, json, sys
from azureml.core import Workspace, Experiment, Environment, ScriptRunConfig
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
experiment=Experiment(workspace=ws,name='vision-model-devops')


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

#os.chdir("./code/scoring")

# env_docker_conda = Environment(
#     image="mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu20.04",
#     conda_file="./code/scoring/conda_dependencies.yml",
#     name="docker-image-pytorch-vision",
#     description="Image with vision model",
# )

config=ScriptRunConfig(source_directory='./code/scoring',script='score.py',
                           compute_target='cpu-cluster')

#config.run_config.environment=env_docker_conda

env=Environment.from_conda_specification(name='docker-image-pytorch-vision',file_path=
                                             './code/scoring/conda_dependencies.yml')
config.run_config.environment=env

run=experiment.submit(config)
aml_url=run.get_portal_url()
print(aml_url)

#os.chdir("../..")


# Publish environment to Azure ML Studio
# env_docker_conda.publish(workspace=ws)

# Register the environment
env.register(workspace=ws)

# Writing the image details to /aml_config/image.json
image_json = {}
image_json["image_name"] = env.name
image_json["image_version"] = env.version

with open("aml_config/image.json", "w") as outfile:
    json.dump(image_json, outfile)
