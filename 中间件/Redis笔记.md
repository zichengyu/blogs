- 安装和自启动
```
根目录：make
进入src：make install
建立配置文件：touch /etc/redis/redis.conf
开机启动：vim /etc/rc.local
增加：/usr/local/bin/redis-server /etc/redis/redis.conf
```
