- Key过期策略

```
主动删除：TTL 定时器
被动删除：访问key的时候，才去检查key是否过期，过期就删除
定期删除：每隔一段时间,去内存中采样检查一定数量的key(默认5，越大越接近传统LRU)，如果过期就删除
Redis是被动+定期
设置了过期时间的key和没设置过期时间的key分开存储

全未设key过期：当set值得时候，检查发现redis内存达到最大设置的值，则去掉一个释放内存空间的方法
释放规则算法：
LRU：least recently used最近最少使用，变种LRU，从数据库随机选择指定数目的key(默认5，越大越接近传统LRU)，然后将热度最低的key删除，热度即redisObject中lru属性上次被访问时间和当前全局时钟的差值
    全局时钟是定时器每100Ms更新一次，故最大延迟100Ms
LFU：least frequently used 一定时间内，使用频率最低。通过计数器，访问加1，不访问会衰减
Random：随机
```

- redis持久化

```
优先aof
RDB快照
含义：redis dataBase，将内存中所有的数据生成dump.rdb文件，可通过参数配置是否开启文件压缩和checkSum
触发条件：
    配置文件save seconds changes -> 多少秒内有多少改变，就会触发生成快照
    flushall命令、关机的时候
    save命令、bgsave命令

AOF：
含义：存储操作指令、rewrite重写，可以减小aof文件的大小
触发条件：always、everysecond、no(操作系统自己控制)、
重写条件：
    auto-aof-rewrite-peceentage 当前aof文件达到上一次aof大小的比例
    auto-aof-rewrite-min-size 最小重写文件大小
    重写是fork一个子线程重写
```
- 主从

```
slave端每隔一秒检测是否自己是另外一个实例的从节点，是的话，执行以下步骤
1、根据配置文件或者命令行传入的主节点地址，和主节点建立连接
2、发送数据复制的指令给主节点，主节点收到指令后，使用bgsave，生成一个RDB文件，并发送给从节点
    从节点接受主节点的RDB文件超时时间默认是60秒，超过会断开连接，从新发送请求，这里可能导致一直重复请求
    生成RDB文件后到从节点接受完该文件期间，主节点收到的新的指令，会放在缓冲区，待从节点接收完文件后在发送给从节点
3、从节点应用RDB文件
4、命令传播

如果从节点和主节点正常连接中，由于某些原因，断开了和主节点的连接，再次连接到主节点时，会根据上次复制的偏移量，继续增量复制
```
- 哨兵机制

```
哨兵节点互相监控，如果一个哨兵发现master节点超过指定时间没有汇报状态，他就会先将master标记为主观下线，然后询问其他哨兵，当大部分哨兵都认为master下线了，才会真正的将master下线
哨兵主节点选举算法：http://thesecretlivesofdata.com/raft/

```

- 安装和自启动
```
根目录：make
进入src：make install
建立配置文件：touch /etc/redis/redis.conf
开机启动：vim /etc/rc.local
增加：/usr/local/bin/redis-server /etc/redis/redis.conf
```

