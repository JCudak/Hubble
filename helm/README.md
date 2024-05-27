# Local setup

## Kubectl
Kubectl is a tool to interact with a k8s cluster. We're gonna need it a lot.
To install it (assumming linux, x86 env) execute:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```



## Minikube
Minikube is a local k8s cluster, and we will be using it in this project.
The guide for installation can be found here: https://minikube.sigs.k8s.io/docs/start/
If You're lazy, You can copy-paste theese commands (assuming linux x84 env):
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

After that, You can start the cluster with `minikube start` - it will need to have some sort of a driver running, Docker will be fine, as it'
s the preffered option (alternatively, You can use podman). Minikube supports many backends (look here: https://minikube.sigs.k8s.io/docs/drivers/), but we don't care about that.

## Helm
Helm can be thought of as a "kubernetes package manager". Many applications provide what's called a "helm chart" which is a pre-made recepie
for deploying an application to a k8s cluster. Those helm charts have a set of default values, which can be overriden (as is the case in this project).
You'll need to have helm installed on Your local system, so here's how to do that (guide: https://helm.sh/docs/intro/install/):
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

## MongoDB
Now that we have our enviroment up and running, we can begin to install our k8s services.
To start we're gonna need to add some helm repositories to our system. This project will use two, the `bitnami` repository, which provides most of the commonly used services, and the `cowboysysop` repository, which provides Mongo Express - a web-based GUI, that allows for interaction with a mongoDB installation.

To add the repositories:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add cowboysysop https://cowboysysop.github.io/charts/
helm repo update # pull the data from newly added repositories
```

Having set all of that up, we can proceed to install MongoDB to our local k8s cluster. For the sake of this project we'll use the PSA architecture (more info can be found here: https://www.mongodb.com/docs/v4.0/core/replica-set-architecture-three-members/#primary-with-a-secondary-and-an-arbiter-psa).

To install this service via helm, execute the following:


```bash
helm install mongo bitnami/mongodb -f mongo_values.yaml
```

After that, You can check if the k8s pods were succesfully created with `kubectl get pods -w` (`-w` stands for watch).

To actually interact with our installation, we'll make use of Mongo Express. Install it with:
```bash
helm install mongo-express cowboysysop/mongo-express -f mongo_express_values.yaml
```

Again, we can check if the pod was correctly initialized with `kubectl get pods -w`.

To access the web GUI from a browser, You need to execute the following command:

```bash
kubectl port-forward <the name of the mongo-express pod> 8081:8081
```

Now you can access the gui, when visiting `localhost:8081` in Your browser. 

