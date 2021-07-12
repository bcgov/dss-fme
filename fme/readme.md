# FME container approach

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


# FME Vagrant VM approach

Background:
In order to run kirk workloads that include reading Esri Geodatabase and writing to an Esri enterprise geodatabase e.g. BCGW, there are 2 necessary conditions:
- Run FME Desktop in windows environment.
- In the same environment, there needs to be licensed arcGIS installed.

See below ref
https://community.safe.com/s/article/notes-on-fme-and-esri-versions-and-compatibility
https://community.safe.com/s/article/geodatabase-formats-missing-greyed-out-or-have-unm

Assumption(s):
- Host machine is linux-based.
- Host machine has virtualBox, Vagrant, ansible and [pywinrm package](https://docs.ansible.com/ansible/latest/user_guide/windows_winrm.html) installed.

### Set up FME desktop

Assumption(s):
- FME floating license is granted via a licensing server.
- Host machine has access to the above server.
- User knows the proper value for FME_LICENSE_SERVER_HOSTNAME (licensing server) and FME_EDITION_NAME.

Additional note(s):
- https://app.vagrantup.com/mwrock/boxes/Windows2016 can take some time to download

For host machine that's on Mac Mojave / High Sierra, if you encounter error like
```
objc[98536]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called.
objc[98536]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called. We cannot safely call it or ignore it in the fork() child process. Crashing instead. Set a breakpoint on objc_initializeAfterForkError to debug.
```
the workaround is to
```
export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES
```

Step(s):

```
export FME_LICENSE_SERVER_HOSTNAME=<FME_LICENSE_SERVER_HOSTNAME> FME_EDITION_NAME=<FME_EDITION_NAME> && vagrant up .

```
