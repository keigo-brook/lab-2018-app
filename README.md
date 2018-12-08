Author: Keigo Ogawa
Date: Dec 8, 2018
## description
Each applications are made from 2 parts, detector and load balancer.
This repository includes:
- Recipes for detector containers
- Recipes for load balancer containers and actual load balancer program

Note that actual detector programs are located in the local server (ask me), because these are too big to store this repository.

Each environment variables are stored in env.sh, which ignored from git.

## how to update applications
1. update application code
2. build container by `./build_container.sh` on each application repository
3. run the container

## how to push or pull continer from Kubernetes master
1. make SSH tunnel by `./make_tunnell....sh`
2. push (or pull) container by `docker push localhost:5000/k_ogawa/[application container name]`,
   or, if shell file like `./push_container.sh` exists, use it.

Note that you must launch repository container if it is not launched on the repository server (may be kubernetes master ?)

