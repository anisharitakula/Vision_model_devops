from azureml.core import Workspace
import os, json, sys
import azureml.core
from azureml.core.authentication import AzureCliAuthentication
#Newly added
from azureml.core.authentication import InteractiveLoginAuthentication

print("SDK Version:", azureml.core.VERSION)
# print('current dir is ' +os.curdir)
with open("aml_config/config.json") as f:
    config = json.load(f)

workspace_name = config["workspace_name"]
resource_group = config["resource_group"]
subscription_id = config["subscription_id"]
#location = config["location"]

#cli_auth = AzureCliAuthentication()
# Use interactive login authentication to authenticate the workspace
#auth = InteractiveLoginAuthentication()

try:
    ws = Workspace.get(
        name=workspace_name,
        subscription_id=subscription_id,
        resource_group=resource_group
        #auth=cli_auth
    )
    print("Workspace already exists")
except:
    # this call might take a minute or two.
    print("Creating new workspace")
    ws = Workspace.create(
        name=workspace_name,
        subscription_id=subscription_id,
        resource_group=resource_group,
        # create_resource_group=True,
        #location=location,
        #auth=cli_auth

    )

# print Workspace details
print(ws.name, ws.resource_group, ws.subscription_id, sep="\n")