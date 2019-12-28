docker run -d -p 本地端口:容器端口 -v 本地目录或volume:容器目录 -e 参数名=参数值 --priivileged
 --name=容器名 --net=自定义网络名 --ip IP地址 镜像名

##### [Veth Pair](https://github.com/yu757371316/blogs/blob/master/images/veth_pair.png)
```
veth pair是用于不同network namespace间进行通信的方式，veth pair将一个network namespace数据发往另一个network namespace的veth
如果多个network namespace需要进行通信，则需要借助bridge(现行环境下，多个容器和主机的通信，就是通过docker0的bridge网络和主机通信的)
```
##### docker网络类型
```
docker network ls命令查看
bridge  host    none

创建新的网络并指定网段：docker network create --subnet=172.18.0.0/24 mynet
```

##### 存储
```
每创建一个一个容器，就会同时创建一个volume(docker volume ls命令查看),每个volume都对应主机上的一个目录(docker inspect volumeName查看)，容器在启动时，就是把容器内的目录映射到该volume来保证即使容器删除，数据也会被持久化而不会被删除
也可以创建容器时指定目录，达到将本地机器的任意目录和容器中任意目录映射：docker run -d 8080:8080 -v 本地路径:容器内某个路径 tomcat
```

