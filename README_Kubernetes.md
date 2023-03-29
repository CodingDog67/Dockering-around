# Kubernetes notes

## Important tools for trying at first 
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

    minicube service deployment_name 

* Scale a pod in run time for up or downscaling

    kubectl scale deployment/deployed_app_name --replicas=3

* update a deployment, find current container name under kubernetes website. Pods tab in workloads. will only update if tag is different

    kubectl set image deployment/deployed_app_name container_name=dockerhub_name/updated_image:new_tag

    kubectl rollout status deployment/deployed_app_name

* rollbacks and history 
   old pod will not shut down until new pod is succesfully pulled up and running.

   In case of a faulty rollout we can rollback via. Rollsback to previous one or history

    kubectl rollout history deployment/deployed_app_name --revision 3(optional)
    kubectl rollout undo deployment/deployed_app_name --to-revision=1(optional)


