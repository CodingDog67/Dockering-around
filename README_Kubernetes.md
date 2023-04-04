# Kubernetes notes

## Important tools for trying at first locally
1) minicube
2) kubectl 
3) chocolatey package manager
4) virtualbox or on windows 10 hyperv

## Imperative deployment 

* To start a cluster and check on it and delete it: 

    minikube --start --driver=hyperv

    minikube status

    minikube delete

* Send image(build and uploded on dockerhub) to a pod and  deploy to cluster. And check if it worked
    
    kubectl create deployment object_name(uptoyou) --image=dockerhub/dockerimage

    kubectl get deployments

    kubect get pods

* Expose deployment to service, pending since not deployed on a cloud provider. A service will allow two main things, stable address that wont change all the time and can be configured to outside world access.

    kubectl expose deployment deployment_name --type=LoadBalancer --port=8080 

    kubectl get services 

    minicube service deployment_name (to get ip to check app)

* Scale a pod in run time for up or downscaling

    kubectl scale deployment/deployed_app_name --replicas=3

* update a deployment, find current container name under kubernetes website. Pods tab in workloads. will only update if tag is different or if imagePullPolicy is set to "Always" to pull latest image always

    kubectl set image deployment/deployed_app_name container_name=dockerhub_name/updated_image:new_tag

    kubectl rollout status deployment/deployed_app_name

* rollbacks and history 
   old pod will not shut down until new pod is succesfully pulled up and running.

   In case of a faulty rollout we can rollback via. Rollsback to previous one or history

    kubectl rollout history deployment/deployed_app_name --revision 3(optional)
    kubectl rollout undo deployment/deployed_app_name --to-revision=1(optional)

* clear everything

    kubectl delete service deployed_app_name
    kubectl delete deployment deployed_app_name

## Declarative Approach

Resource definition files (similar to docker compose yamls), -f file. 

    kubectl apply -f=deployment.yaml -f=service.yaml
    minicube service backend

- Selectors and labels. Deploymends are dynamic objects/things, selects pods that are added after deployment has been created. Selects those with a selector. Here we match labels or expressions. Labels key and values could also be multiple but pods need complete set of labels. 

Deleting resource(s) either by file or selector

    kubectl delete -f=deployment.yaml -f=serice.yaml
    kubectl delete deployments, services -l group=example

To Merge yamls merge and seperate by ---, must be three dashes. Bit more messy but only call one kubecrl apply instead of two

LivenessProbe to control how kubernetes checks if pods and containers are healthy or not

## Volumes - State - Environmental Vars

State is data created (user generated or app intermediate results) and used by application but which musnt be lost.
Volume lifetime depends on pod lifetime (survive restart but not removal of pods), we got local volumes (on nodes) and Cloud provider specific Volumes

There is a broad selection of volume types https://kubernetes.io/docs/concepts/storage/volumes/#volume-types that determines how data is stored.

Define volume where pods are configured and defined and bind it to a container. Three useful containers are: \
    - emptyDir: creates empty directory whenever the pods starts, keeps it alive and filled with data as long as the pod is alive
    - hostPath : good for multiple replicas, multiple pods can share one and the same path on host machine. (but wont sovle multiple host machines, hostPath is node specific)
    - CSI: flexible type, interface for various storage solution from other cloud provider. Search for an integration 

Repetitive and hard to administer on a global level

### Persistent Volumes

Not destroyed upon Pod removal, volume detached/independent from pod and pod life cycle, eg clous storage service. One node can have multiple claims to a PV and different claims to different PV on different nodes. Full Flexibilty, standalone cluster resource. 
Define a host Persistent Volume and a claim, the claim is then made by pods to use the volume.

Use by calling these commands

    kubectl apply -f=host-pv.yaml 
    kubectl apply -f=host-pvc.yaml
    kubectl apply -f=deployment.yaml

Kubectl get pv to see all persitent volumes

### Environmental Vars

Define in the Container yaml or as extra env.yaml and apply via kubectl apply -f=environment.yaml

## Networking

**Internally to outside pod** you can network via services to allow out of pod request sent inside a pod container. 

**Pod-internal** for multiple containers within a pod. Comunication is done via declaration of a second container within the same pod yaml file. No need to edit service though auth api should not be reachable to the outside world. Localhost is the magic address to use inside the pod.

**Cluster Internal** pod to pod communication via IP address, eg take the ip of the auth service in user deployment instead of local host. Downside you have to manually find out the address and hard code it. 

Or

Kubernetes provides automatically generated environmental variables to get the automatically generated IP Address. process.env.SERVICE_NAME_SERVICE_HOST eg process.env.auth-service becomes AUTH_SERVICE_SERVICE_HOST. to run it with docker, you need to add this new kubernetes env var to the docker compose yaml SERVICE_NAME_SERVICE_HOST: auth and re-build the image and push it.

Or

Automatic generated domain names \
CoreDNS to create cluster internal domain names for all services. service-name.namespace (default) is the value to use under env in the yaml of the pod that needs to access e.g auth-service.default. Look up other namespaces via kubectl namespace