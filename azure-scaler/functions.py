from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.containerservice import ContainerServiceClient

import os
import logging

logger = logging.getLogger('azure')
logger.setLevel(logging.WARNING)

def checkEnvSetup(vars):
    for var in vars:
        try:
            s = os.environ[var]
        except:
            logging.error("%s not set, set this env var", var)
            return False
    return True

def get_credentials():
    try:
        subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
        credentials = ClientSecretCredential(
            client_id=os.environ['AZURE_CLIENT_ID'],
            client_secret=os.environ['AZURE_CLIENT_SECRET'],
            tenant_id=os.environ['AZURE_TENANT_ID']
        )
        return credentials, subscription_id
    except:
        logging.exception("Exception while getting credentials from ENV", exc_info=True)
        exit(1)


def startStopVM(resource_group, vmname, action):
    credentials, subscription_id = get_credentials()
    try:
        compute_client = ComputeManagementClient(credentials, subscription_id)
        if action.lower() == 'start':
            logging.info("Starting Virtual Machine: %s", vmname)
            async_vm_start = compute_client.virtual_machines.begin_start(resource_group, vmname)
            async_vm_start.wait()
            return True
        elif action.lower() == 'stop':
            logging.info("Stopping Virtual Machine: %s", vmname)
            async_vm_stop = compute_client.virtual_machines.begin_deallocate(resource_group, vmname)
            async_vm_stop.wait()
            return True
    except:
        logging.exception("Exception occurred with VM, %s", vmname, exc_info=True)
    return False

def startStopAks(resource_group, cluster_name, action):
    credentials, subscription_id = get_credentials()
    try:
        containerservice_client = ContainerServiceClient(
            credential=credentials,
            subscription_id=subscription_id
        )
        if action.lower() == 'stop':
            async_aks_stop = containerservice_client.managed_clusters.begin_stop(resource_group, cluster_name)
            async_aks_stop.wait()
            return True
        elif action.lower() == 'start':
            async_aks_start = containerservice_client.managed_clusters.begin_start(resource_group, cluster_name)
            async_aks_start.wait()
            return True
    except:
        logging.exception("Exception occurred with AKS Cluster, %s", cluster_name, exc_info=True)
    return False