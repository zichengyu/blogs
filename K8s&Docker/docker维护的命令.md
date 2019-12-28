先上删除命令：

```
docker images|grep none|awk '{print $3 }'|xargs docker rmi
```

也可以先查看，后删除
```
docker ps -a | grep "Exited" | awk '{print $1 }'|xargs docker stop

docker ps -a | grep "Exited" | awk '{print $1 }'|xargs docker rm

docker images|grep none|awk '{print $3 }'|xargs docker rmi
```


强制删除镜像名称中包含“doss-api”的镜像
```
docker rmi --force $(docker images | grep doss-api | awk '{print $3}')
```

杀死所有正在运行的容器
```
docker kill $(docker ps -a -q)
```

删除所有已经停止的容器
```
docker rm $(docker ps -a -q)
```

删除所有未打 dangling 标签的镜像
```
docker rmi $(docker images -q -f dangling=true)
```

删除所有镜像
```
docker rmi $(docker images -q)
```

删除停止的容器
```
docker rm $(docker ps --all -q -f status=exited)
```

删除没有使用的镜像
```
docker rmi -f $(docker images | grep "<none>" | awk "{print \$3}")
```

批量删除镜像
```
docker images | awk '{print $3}' | xargs docker rmi
```

批量删除容器
```
docker ps -a | awk '{print $1}' | xargs docker rm
```

如果需要根据具体的容器名或镜像名过滤的话，可以修改上面的awk表达式进行处理。
类似这样，删除test_开头的镜像：
```
docker rmi -f $(docker images --format "{{.Repository}}" |grep "^test_*")
```
