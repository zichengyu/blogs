dashboard

> 查看状态：kubectl get deployment --all-namespaces   
> 查看详细信息：kubectl describe deployment kubernetes-dashboard --namespace=kube-system   
> 删除：kubectl delete deployment kubernetes-dashboard --namespace=kube-syste

dashboardsvc
> 查看状态：kubectl get svc --all-namespaces   
> 查看详细信息: kubectl describe svc kubernetes-dashboardsvc --namespace=kube-system   
> 删除：kubectl delete svc kubernetes-dashboardsvc --namespace=kube-system

Pod
> 实时查看所有pod和其状态：kubectl get pods --all-namespaces -w
> kubectl get pods -o wide       
> kubectl进入pod：kubectl exec -it podName bash   
> 查看：kubectl get pod -o wide --all-namespaces   
> 查看详细信息：kubectl describe pod podName      
> 查看log：kubectl logs -f podName   
> 物理主机上访问(nginx为例)：kubectl port-forward nginx 8080:80（要做端口转发）  
> 用yaml删除：kubectl delete -f yamlName

扩容
> 将名字为NGINX的pod扩容为五个：kubectl scale rs nginx --replicas=5
