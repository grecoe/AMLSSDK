'''
    This file shows how to register a model with the appropriate files 

    Taken from :
    https://github.com/Azure/MachineLearningNotebooks/blob/master/how-to-use-azureml/deploy-to-cloud/model-register-and-deploy.ipynb

    PARAMETERS REQUIRED:
        Model Name
'''
from azureml.core import Workspace
from azureml.core.model import Model
from utilities import utils 

'''
    PARAMETERS
'''
modelName = "sklearn_regression_model.pkl"

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
    If the model was not found, register it.
'''
if not model:
    print("Model not found, creating new registration")
    model = Model.register(model_path = "model/sklearn_regression_model.pkl",
                           model_name = modelName,
                           tags = {'area': "diabetes", 'type': "regression"},
                           description = "Ridge regression model to predict diabetes",
                           workspace = ws)
else:
    print("Model already registered.")

