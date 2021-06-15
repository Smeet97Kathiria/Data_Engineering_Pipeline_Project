#!/bin/bash

MATERIALS=airflow-materials-aws
# CHANGE marclamberti by your Git username!
GIT_USERNAME=Smeet97Kathiria

# Create the cluster
eksctl create cluster -f cluster.yml


# SCRIPT_SETUP_FLUX= 
chmod a+x /home/ec2-user/environment/setupflux.sh
/home/ec2-user/environment/setupflux.sh $GIT_USERNAME

fluxctl sync --k8s-fwd-ns flux

# If the command above failed, you migh need to
# recreate the deploy key airflow-workstation-deploy-flux in the repo
# airflow-eks-config with the key generated below
fluxctl identity --k8s-fwd-ns flux

# and execute fluxctl sync --k8s-fwd-ns flux again

# chmod +x setup.sh


# ./setup.sh

