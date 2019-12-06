# 1、拉取最新的tomcat镜像到本地  

```perl
sudo docker pull tomcat 
```

# 2、基于Dockerfile创建镜像文件  

dockerfile可以帮助我们创建自定义的镜像，本文比较简单直接基于最新的tomcat镜像，当然tomcat镜像也可以自定义(tomcat版本、jdk版本)。  新建Dockerfile文件，并将需要部署的war包放在相同文件夹下

```perl
#基础镜像
FROM tomcat:8.5.31-jre8                                  
#作者信息
MAINTAINER yuzicheng yu.zicheng@neoway.com               
#定义变量、后续会使用，具体路径可以先启动容器然后进入进行查看
ENV DIR_WEBAPP /usr/local/tomcat/webapps/                
#删除webapp下所有文件，因为当前应用作为根应用
RUN  rm -rf $DIR_WEBAPP/*
#添加本地的war包到远程容器中
ADD ./target/restful.war $DIR_WEBAPP/ROOT.war
#配置文件夹映射
VOLUME /usr/local/tomcat/webapps
#配置工作目录
WORKDIR /usr/local/tomcat/webapps
#解压war包到ROOT目录
RUN unzip $DIR_WEBAPP/ROOT.war -d $DIR_WEBAPP/ROOT/
#暴露端口
EXPOSE 6375
#启动tomcat
CMD ["catalina.sh", "run"]
```

# 3、idea下载docker插件

# 4、配置docker插件链接远程Dcoker

![1532071508904](https://github.com/yu757371316/blogs/blob/master/images/idea%E8%BF%9C%E7%A8%8B%E9%83%A8%E7%BD%B2war-1.png)

# 5、创建docker服务并启动

![1533348434785](https://github.com/yu757371316/blogs/blob/master/images/idea%E8%BF%9C%E7%A8%8B%E9%83%A8%E7%BD%B2war-2.png)



注意问题：

1、此处未修改Tomcat默认的端口，故映射的还是8080的端口

2、此处添加了zookeeper的host，可以通过--add-host hostname:IP
