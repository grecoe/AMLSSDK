import os
from azureml.core import Workspace

'''
    This script expects that you have logged in already. Perform the following steps if you have not already done so:

    az login
    az account set -s [YOUR_SUBSCRIPTION_ID]

    PARAMETERS REQUIRED:
        Subscription ID
        Resource Group Name
        Workspace Name

    PRE-REQUISITES
        pip install --upgrade azureml-sdk
'''

'''
    PARAMETERS
'''
subscription_id = os.getenv("SUBSCRIPTION_ID", default="YOUR_SUBSCRIPTION_ID")
resource_group = os.getenv("RESOURCE_GROUP", default="NEW_RESOURCE_GROUP_NAME")
workspace_name = os.getenv("WORKSPACE_NAME", default="AMLS_WORKSPACE_NAME")
workspace_region = os.getenv("WORKSPACE_REGION", default="eastus")

amlsWorkspace = None

try:
    amlsWorkspace = Workspace(subscription_id = subscription_id, resource_group = resource_group, workspace_name = workspace_name)
    print("Workspace configuration succeeded.")
except Exception as e:
    print("Workspace not accessible. Attempting to create it now.....")
    print("Error: ", str(e))

    try:
        amlsWorkspace = Workspace.create(name = workspace_name,
                          subscription_id = subscription_id,
                          resource_group = resource_group, 
                          location = workspace_region,
                          default_cpu_compute_target=Workspace.DEFAULT_CPU_CLUSTER_CONFIGURATION,
                        default_gpu_compute_target=Workspace.DEFAULT_GPU_CLUSTER_CONFIGURATION,
                        create_resource_group = True,
                        exist_ok = True)
    except Exception as ie:
        print("Creating of workspace failed.")
        print("Error: ", str(ie))

# Report on what every happened, but more importantly, write config if there is one. 
if amlsWorkspace:
    print("Workspace details:")
    details = amlsWorkspace.get_details()                      
    for key in details.keys():
        print(key, details[key])

    # write the details of the workspace to a configuration file to the notebook library
    print("Workspace details saved...")
    amlsWorkspace.write_config()
else:
    print("Unable to retrieve or create workspace.")