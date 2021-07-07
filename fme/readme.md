# FME containerization solutions

### Set up FME desktop

Assumption(s):
- FME floating license is granted via a licensing server.
- Host machine has access to the above server.
- User knows the proper value for FME_LICENSE_SERVER_HOSTNAME (licensing server) and FME_EDITION_NAME.

Additional note(s):
- Made use of a docker base image as installing fme desktop takes much time and not convenient for dev work.

Step(s):

```
docker build --tag fme-desktop-base -f Dockerfile_base .

docker build --tag fme-desktop .

docker run --network=host -e FME_LICENSE_SERVER_HOSTNAME=<FME_LICENSE_SERVER_HOSTNAME> -e FME_EDITION_NAME=<FME_EDITION_NAME> --rm -it fme-desktop:latest bash 
```

### Set up FME server

FME Server Container Deployments
https://s3-us-west-2.amazonaws.com/safe-software-container-deployments/index.html?prefix=2021.0/2021.0.3/

https://docs.safe.com/fme/2019.0/html/FME_Server_Documentation/AdminGuide/Deploying-with-Docker-Compose.htm#

Additional note(s):
- k8s-quickstart.sh and docker-compose.yaml has not been tested.