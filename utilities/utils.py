
from azureml.core import Workspace
from azureml.core.model import Model
from azureml.core.webservice import Webservice
from azureml.core.image import ContainerImage
from azureml.core.compute import ComputeTarget

'''
    Pick up the models associated with this workspace. 

    This one gets particular models by name. 
'''
def getModel(workspace, modelName):
    model = None
    registeredModels = Model.list(workspace)
    for mdl in registeredModels:
        if mdl.name == modelName:
            model = mdl
            break
    return model 

'''
    Pick up the web services associated with this workspace. 

    This one gets particular service by name. 
'''
def getWebservice(workspace, webserviceName):
    webservice = None
    services = Webservice.list(workspace)
    for svc in services:
        if svc.name == webserviceName:
            webservice = svc
            break 
    return webservice

'''
    Pick up the container images associated with this workspace. 

    This one gets particular container by name.Note that you provide
    a container name with AKS but the container for ACI is the same
    as the service you create. 
'''
def getContainerImage(workspace, imageName):
    image = None
    images = ContainerImage.list(workspace)
    for img in images:
        if img.name == imageName:
            image = img
    return image

'''
    Pick up the compute targets associated with this workspace. 

    This one gets particular target by name. 
'''
def getComputeTarget(workspace, targetName):
    cTarget = None
    targets = ComputeTarget.list(workspace)
    for tgt in targets:
        if tgt.name == targetName:
            cTarget = tgt
            break 
    return cTarget
