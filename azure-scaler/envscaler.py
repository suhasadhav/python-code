import os
from os.path import exists
import argparse
import yaml
import logging
from functions import startStopVM, checkEnvSetup, startStopAks
from yaml.loader import SafeLoader

logging.basicConfig(level=logging.getLevelName(os.getenv('LOGLEVEL', "INFO")), 
    format=os.getenv("LOGFORMAT", "%(asctime)s | %(filename)s | %(levelname)-8s  : %(message)s (line-%(lineno)d)"))

MANDATORY_ENVVARS = [
        'AZURE_CLIENT_ID',
        'AZURE_TENANT_ID',
        'AZURE_CLIENT_SECRET',
        'AZURE_SUBSCRIPTION_ID'
    ]
# get arguments from command line
def getArguments():
    parser = argparse.ArgumentParser(description='Start/Stop Job for Env')
    parser.add_argument('--env', help='Environment dev/uat/prod', required=True)
    parser.add_argument('--action', help='start/stop', required=True)
    parser.add_argument('--repoFile', help='env.yaml', default='env.yaml')
    return parser.parse_args()

if __name__ == '__main__':
    args = getArguments()
    if not checkEnvSetup(MANDATORY_ENVVARS):
        exit(1)
    if exists(args.repoFile):
        logging.info("Reading %s file for env %s", args.repoFile, args.env)
        
        with open(args.repoFile, "r") as f:
            yaml_data = yaml.load(f, SafeLoader)
        
        if args.env in yaml_data:
            logging.info("Handling %s", args.env)
            env_data = yaml_data[args.env]
            try:
                rg = env_data['rg']
            except:
                logging.exception("Failed to get rg from env.yaml", exc_info=True)
                exit(1)
            if rg: 
                logging.info("Got resource Group: %s env: %s", rg, args.env)
                if 'vm' in env_data:
                    for vm in env_data['vm']:
                        logging.info("VM: %s, Action: %s", vm, args.action)
                        if startStopVM(rg, vm, args.action):
                            logging.info("VM: %s, Action: %s performed successfully", vm, args.action)
                        else:
                            logging.error("Failed to stop VM: %s", vm)
                if 'aks' in env_data:
                    for cluster in env_data['aks']:
                        logging.info("AKS: %s, Action: %s", cluster, args.action)
                        if startStopAks(rg, cluster, args.action):
                            logging.info("AKS: %s, Action: %s performed successfully", cluster, args.action)
                        else:
                            logging.error("Failed to stop AKS Cluster: %s", cluster)
                            exit(1)
        else:
            logging.error("%s does not exists in env.yaml", args.env)
            exit(1)
    else:
        logging.error("Failed to open repofile %s")
        exit(1)
