#!/bin/bash

#### INFO ####
# This script should help to get you started with k8s and it should only be used for dev/testing purposes.
# For production deployments, please use helm directly without of this script. The values used in this quickstart script,
# should provide a good starting point for production deployments.
##############

# Ensure we are failing on all errors
set -e

# Ensure helm and kubectl is installed
command -v helm >/dev/null 2>&1 || { echo >&2 "This script requires helm (https://docs.helm.sh/) but it's not installed.  Aborting."; exit 1; }
command -v kubectl >/dev/null 2>&1 || { echo >&2 "This script requires kubectl (https://kubernetes.io/docs/tasks/tools/install-kubectl/) but it's not installed.  Aborting."; exit 1; }

listArg="-n fmeserver"
releaseName="fmeserver"

if [[ $(helm version -c --short) == *"v2"* ]] ; then
    # Ensure tiller is running
    helm list >/dev/null 2>&1 || { echo >&2 "Tiller is not installed, please run 'helm init' first and ensure helm is working as expected"; exit 1; }
    listArg=""
    releaseName="-n fmeserver"
fi

if [ "$FORCE" = "true" ] ; then
    echo "Assuming NGINX ingress controller is installed..."
else
    echo "FME Server requires a running NGINX ingress controller to work correctly"
    while true; do
        read -p "Is NGINX ingress controller running in the cluster? " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* )
                echo "Please install the NGINX ingress controller first: https://kubernetes.github.io/ingress-nginx/ or https://hub.kubeapps.com/charts/stable/nginx-ingress"
                exit
                ;;
            * ) echo "Please answer yes or no.";;
        esac
    done
fi

# Ensure Chart repo is added and up to date
if helm repo list | grep -q https://safesoftware.github.io/helm-charts/ ; then
    repo=`helm repo list | grep https://safesoftware.github.io/helm-charts/`
    [[ $repo =~ ^([a-z-]+)[[:space:]]+https://safesoftware.github.io/helm-charts/ ]]
    repo_name=${BASH_REMATCH[1]}
    helm repo update >/dev/null 2>&1
    echo "Updated the Safe Software Chart repository ($repo_name)"
else
    helm repo add safesoftware https://safesoftware.github.io/helm-charts/
    echo "Added Safe Software Chart repository"
fi

current_k8s_context=`kubectl config current-context`

# Ensure FME Server is not installed already
if helm list $listArg | grep -q fmeserver ; then
    echo >&2 "FME Server is already running in your Kubernetes cluster (current context: $current_k8s_context). Please delete the previous installation first before proceeding."
    exit 1
fi

# Set kubernetes environment config
if [ -n "$K8S_ENV" ] ; then
    env=$K8S_ENV
else
    printf "\nWhat environment is your Kubernetes cluster running in?\n"
    PS3="Please choose an option: "
    options=("docker-for-mac" "docker-for-win" "linux-with-host-dir" "aks" "gke" "eks" "quit")
    select env in "${options[@]}"
    do
        case $env in
            "docker-for-mac"|"docker-for-win"|"linux-with-host-dir"|"aks"|"gke")
                echo ""
                break
                ;;
            "eks")
                echo "Please note that GP2 needs to be added as a storage class first for this deployment to work (https://docs.aws.amazon.com/eks/latest/userguide/storage-classes.html)"
                break
                ;;
            "quit")
                exit
                ;;
            *) echo "invalid option $REPLY";;
        esac
    done
fi

# Get hostname
if [ -z "$K8S_HOSTNAME" ] ; then
    read -p "Enter hostname (default localhost): " k8s_hostname
    K8S_HOSTNAME=${k8s_hostname:-localhost}
fi

# Get base path if required
if [ -z "$HOST_DIR_BASE_PATH" ] && [[ $env =~ with-host-dir ]] ; then
    read -p "Enter a base path for fmeserver data (default /tmp/k8s): " base_path
    base_path=${base_path:-/tmp/k8s}
    base_path_param="--set storage.postgresql.path=$base_path/db,storage.fmeserver.path=$base_path/data"
elif [ -n "$HOST_DIR_BASE_PATH" ] && [[ $env =~ with-host-dir ]] ; then
    base_path_param="--set storage.postgresql.path=$HOST_DIR_BASE_PATH/db,storage.fmeserver.path=$HOST_DIR_BASE_PATH/data"
fi

# Create namespace
kubectl create namespace fmeserver || true
# Generate helm command
helm_install_command="helm install --namespace fmeserver $releaseName safesoftware/fmeserver-2021.0.3 --version 0.2.29 -f https://s3-us-west-2.amazonaws.com/safe-software-container-deployments/2021.0.3/tags/2021.0.3-20210601/environments/$env.values.yaml $base_path_param --set fmeserver.image.tag=2021.0.3-20210601,deployment.hostname=$K8S_HOSTNAME --set fmeserver.image.registry=quay.io,fmeserver.image.namespace=safesoftware $JENKINS_PARAMS"

printf "\nExecuting the following command: $helm_install_command \n\n"
if [ "$FORCE" = "true" ] ; then
    echo "Skipping confirmation..."
else
    printf "\nInstalling FME Server 2021.0.3 (build 21326, chart version 0.2.29) with hostname $K8S_HOSTNAME into namespace 'fmeserver' of your cluster on $env using the current context \"$current_k8s_context\"\n"
    while true; do
        read -p "Would you like to proceed? " yn
        case $yn in
            [Yy]* ) break;;
            [Nn]* ) exit;;
            * ) echo "Please answer yes or no.";;
        esac
    done
fi

$helm_install_command