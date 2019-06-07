'''
    This file shows how to test against an ACI instance 

    Taken from :
    https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deploy-to-cloud/model-register-and-deploy.ipynb

    PARAMETERS REQUIRED:
        Model Name
        ACI Service Name

    PRE-REQUISITE
        00_init_env.py
        01_register_model.py
'''

import json
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.model import InferenceConfig
from azureml.core.webservice import AciWebservice, Webservice
from azureml.exceptions import WebserviceException

from utilities import utils 

'''
    PARAMETERS
'''
modelName = "sklearn_regression_model.pkl"
aciServiceName = "aciservice1"

'''
    Get the saved worksapce (from running init_env.py)
'''
ws = Workspace.from_config()
print("")
print("Workspace Details:")
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')
print("")


'''
    Find models, if it's already registered we will skip registration
'''
model = utils.getModel(ws,modelName)


'''
    If the model is not registered, go back to 01_register_model.py
'''
if model:

    # Create the inference for the container
    inference_config = InferenceConfig(runtime= "python", 
                                       entry_script="model/score.py",
                                       conda_file="model/myenv.yml", 
                                       extra_docker_file_steps="model/helloworld.txt")

    deployment_config = AciWebservice.deploy_configuration(cpu_cores = 1, memory_gb = 1)

    # If the web service already exists, get rid of it.
    service = utils.getWebservice(ws, aciServiceName)
    if service:
        service.delete()

    # Create a service and wait for it's deployment
    service = Model.deploy(ws, aciServiceName, [model], inference_config, deployment_config)
    service.wait_for_deployment(True)
    print(service.state)                                       

    # Test the service
    test_sample = json.dumps({'data': [
        [1,2,3,4,5,6,7,8,9,10], 
        [10,9,8,7,6,5,4,3,2,1]
    ]})

    test_sample_encoded = bytes(test_sample,encoding = 'utf8')
    prediction = service.run(input_data=test_sample_encoded)
    print(prediction)

    # Clean up
    service.delete()

    container = utils.getContainerImage(ws, aciServiceName)
    if container:
        container.delete()