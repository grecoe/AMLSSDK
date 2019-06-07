'''
    This file shows how to deploy to an AKS cluster 

    Taken from :
    https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deployment/production-deploy-to-aks/production-deploy-to-aks.ipynb

    PARAMETERS REQUIRED:
        Model Name
        ACI Service Name
        AKS Name
        Docker Image Name

    PRE-REQUISITE
        00_init_env.py
        01_register_model.py
'''
import os
import json
import requests
from azureml.core import Workspace
from azureml.core.compute import AksCompute, ComputeTarget
from azureml.core.webservice import Webservice, AksWebservice
from azureml.core.image import Image
from azureml.core.model import Model
from azureml.core.image import ContainerImage

from utilities import utils 

'''
    PARAMETERS
'''
modelName = "sklearn_regression_model.pkl"
aksServiceName = "aksservice1"
aksName = "testaks"
imageName = "testaksimage1"

'''
    Get the saved worksapce (from running init_env.py)
'''
ws = Workspace.from_config()
print("")
print("Workspace Details:")
print(ws.name, ws.resource_group, ws.location, ws.subscription_id, sep = '\n')
print("")

'''
    Get Model and image
'''
model = utils.getModel(ws, modelName)
containerImage = utils.getContainerImage(ws, imageName)
aks_target = utils.getComputeTarget(ws, aksName)
aks_service = utils.getWebservice(ws, aksServiceName) 

'''
    Now get down to it.
'''
if not model:
    print("Cannot continue without a model....")
else:

    # Create the container image if it's not there
    if not containerImage:
        print("Creating container image")

        # Unlike the InferenceConfig from the ACI script, you MUST be in the same directory
        # as the files being added here....paths do NOT work. 
        print("Changing working directory....")
        currentDirectory = os.getcwd()
        os.chdir(os.path.join(currentDirectory, "model"))
        image_config = ContainerImage.image_configuration(execution_script = "score.py",
                                                          runtime = "python",
                                                          conda_file = "myenv.yml",
                                                          description = "Image with ridge regression model",
                                                          tags = {'area': "diabetes", 'type': "regression"}
                                                         )
        containerImage = ContainerImage.create(name = imageName,
                                      # this is the model object
                                      models = [model],
                                      image_config = image_config,
                                      workspace = ws)

        print("Wait for container image....")
        containerImage.wait_for_creation(show_output = True)
        os.chdir(currentDirectory)

    # Create the AKS target if it's not there.
    if not aks_target:
        print("Creating AKS target")

        # Use the default configuration (can also provide parameters to customize)
        prov_config = AksCompute.provisioning_configuration()

        # Create the cluster
        aks_target = ComputeTarget.create(workspace = ws, 
                                          name = aksName, 
                                          provisioning_configuration = prov_config)

        print("Wait for AKS compute target....")
        aks_target.wait_for_completion(show_output = True)
        print(aks_target.provisioning_state)
        print(aks_target.provisioning_errors)

    if not aks_service:
        #Set the web service configuration (using default here)
        aks_config = AksWebservice.deploy_configuration()

        aks_service = Webservice.deploy_from_image(workspace = ws, 
                                                   name = aksServiceName,
                                                   image = containerImage,
                                                   deployment_config = aks_config,
                                                   deployment_target = aks_target)

        print("Wait for AKS service....")
        aks_service.wait_for_deployment(show_output = True)
        print(aks_service.state)        

    
    # Now get ready to call the service
    key1, Key2 = aks_service.get_keys()
    print(key1)

    test_sample = json.dumps({'data': [
            [1,2,3,4,5,6,7,8,9,10], 
            [10,9,8,7,6,5,4,3,2,1]
        ]})
    test_sample = bytes(test_sample,encoding = 'utf8')

    # Don't forget to add key to the HTTP header.
    headers = {'Content-Type':'application/json', 'Authorization': 'Bearer ' + key1}

    resp = requests.post(aks_service.scoring_uri, test_sample, headers=headers)

    print("prediction:", resp.text)