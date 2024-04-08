from azureml.core import Workspace,Experiment,Environment,ScriptRunConfig
from azureml.core.runconfig import RunConfiguration
import json


if __name__=="__main__":
    config_path='aml_config/config.json'
    ws=Workspace.from_config(path=config_path)
    # Attach Experiment
    experiment_name = "devops-ai-demo"
    experiment = Experiment(workspace=ws, name=experiment_name)

    # Editing a run configuration property on-fly.
    run_config_user_managed = RunConfiguration()
    run_config_user_managed.environment.python.user_managed_dependencies = True

    config=ScriptRunConfig(source_directory="./code",script="training/train.py",
                           run_config=run_config_user_managed,
                           compute_target="cpu-cluster")
    
    
    run=experiment.submit(config)

    # Shows output of the run on stdout.
    run.wait_for_completion(show_output=True, wait_post_processing=True)

    # Raise exception if run fails
    if run.get_status() == "Failed":
        raise Exception(
            "Training on local failed with following run status: {} and logs: \n {}".format(
                run.get_status(), run.get_details_with_logs()
            )
    )

    # Writing the run id to /aml_config/run_id.json

    run_id = {}
    run_id["run_id"] = run.id
    run_id["experiment_name"] = run.experiment.name
    with open("aml_config/run_id.json", "w") as outfile:
        json.dump(run_id, outfile)