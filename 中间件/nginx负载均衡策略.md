Nginx能够配置代理多台服务器。当一台服务器宕机之后。仍能保持系统可用。详细配置步骤例如以下：

# 1、配置upstream

http节点下，加入upstream节点。

```
upstream linuxidc {       
	server 10.0.6.108:7080;       
	server 10.0.0.85:8980; 
}
```



# 2、配置proxy_pass

将server节点下的location节点中的proxy_pass配置为：http:// + upstream名称，即“http://linuxidc”.

```
location / {             
	root  html;             
	index  index.html index.htm;             
	proxy_pass linuxidc; 
	listen 12346;
    health_check;
}
```

​      如今负载均衡初步完毕了。upstream依照轮询（默认）方式进行负载，每一个请求按时间顺序逐一分配到不同的后端服务器。假设后端服务器down掉。能自己主动剔除。尽管这样的方式简便、成本低廉。但缺点是：可靠性低和负载分配不均衡。

适用于图片服务器集群和纯静态页面服务器集群。

# 3、upstream的分配策略

​    upstream还有其他的分配策略，分别例如以下：

## 3.1 ip_hash（訪问ip）

​    每一个请求按訪问ip的hash结果分配。这样每一个訪客固定訪问一个后端服务器，能够解决session的问题。

```
upstream favresin {       
	ip_hash;       
	server 10.0.0.10:8080;       
	server 10.0.0.11:8080; 
}
```



## 3.2 fair（第三方）

​    按后端服务器的响应时间来分配请求。响应时间短的优先分配。与weight分配策略相似。

```
upstream favresin {            
	server 10.0.0.10:8080;       
	server 10.0.0.11:8080;       
	fair; 
}
```



## 3.3 Generic Hash

确定发送请求的服务器是根据用户定义的键来确定的，可以是一个文本字符串,变量,或组合。
例如,关键字可能是成对的源IP地址和端口,或者一个URI

注意：在upstream中加入hash语句。server语句中不能写入weight等其他的參数，hash_method是使用的hash算法。

consistent参数表示打开 ketama 一致性hash功能

```
upstream resinserver {   
	hash $request_uri consistent;
	server 10.0.0.10:7777;       
	server 10.0.0.11:8888;             
	hash_method crc32; 
}
```

## 3.4 **Round Robin** 

请求被均匀地分布在服务器、存储与服务器权重考虑 ，默认就是这种方式

```
upstream backend {
   server backend1.example.com;
   server backend2.example.com;
}
```

## 3.5 Least Connections

一个请求被发送到服务器的活跃连接数最少的,其次考虑服务器的权重

```
 upstream backend {
    least_conn;
    server backend1.example.com;
    server backend2.example.com;
}
```

## 3.6 [**Least Time**](https://nginx.org/en/docs/http/ngx_http_upstream_module.html#least_time) (NGINX Plus only) 

为每个请求,NGINX +选择最低的服务器平均延迟和最低的活跃连接数

```
upstream backend {
    least_time header;
    server backend1.example.com;
    server backend2.example.com;
}
```

# 4、其他参数说明

upstream还能够为每一个设备设置状态值，这些状态值的含义分别例如以下：

down 表示单前的server临时不參与负载.

weight 默觉得1.weight越大，负载的权重就越大。

max_fails ：同意请求失败的次数默觉得1.当超过最大次数时，返回proxy_next_upstream 模块定义的错误.

fail_timeout : max_fails次失败后。暂停的时间。

backup： 其他全部的非backup机器down或者忙的时候，请求backup机器。所以这台机器压力会最轻。

```
upstream bakend { #定义负载均衡设备的Ip及设备状态       
	ip_hash;       
	server 10.0.0.11:9090 down;       
	server 10.0.0.11:8080 weight=2;       
	server 10.0.0.11:6060;       
	server 10.0.0.11:7070 backup; 
}
```