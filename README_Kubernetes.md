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

* Expose deployment to service, pending since not deployed on a cloud provider

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

## Volumes - State

State is data created (user generated or app intermediate results) and used by application but which musnt be lost.
Volume lifetime depends on pod lifetime (survive restart but not removal of pods), we got local volumes (on nodes) and Cloud provider specific Volumes

There is a broad selection of volume types https://kubernetes.io/docs/concepts/storage/volumes/#volume-types that determines how data is stored.

Define volume where pods are configured and defined