- 节点信息说明
```
null(节点中保存的数据信息)
cZxid = 0x100000052（创建节点的事务ID）
ctime = Fri Jun 22 17:50:30 CST 2018（节点创建时间）
mZxid = 0x100000052（最后一次更新节点的事务ID）
mtime = Fri Jun 22 17:50:30 CST 2018（节点更新时间）
pZxid = 0x100000052（子节点最后一次被更新的事务ID）
cversion = 0（子节点的版本号）
dataVersion = 0（数据版本号）
aclVersion = 0（权限版本号）
ephemeralOwner = 0x0（用于临时节点，保存临时节点的ID，如果为持久化节点，则其值为0）
dataLength = 0（节点存储的数据的长度）
numChildren = 0（当前节点的子节点的个数）
```

- znode的类型

```
PERSISTENT                持久化节点
PERSISTENT_SEQUENTIAL     顺序自动编号持久化节点，这种节点会根据当前已存在的节点数自动加 1
EPHEMERAL                 临时节点, 客户端session超时这类节点就会被自动删除
EPHEMERAL_SEQUENTIAL      临时自动编号节点

同级节点必须唯一；零时节点不能存在子节点
```

- ZK用途

```
主从选举、复杂均衡、分布式锁、配置中心、注册中心等
```

- zk集群角色

```
Leader：集群中唯一、通过选举产生，负责处理所有的事务请求(会话状态变更和数据节点变更)，默认情况下也处理读请求
Follower：处理客户端非事务请求，转发事务请求给Leader，参与leader选举和事务操作的‘过半通过’投票策略
Observer：只提供读服务，在不影响集群写性能的情况下扩展集群的读性能，不参与任何形式的选举
```

- ZAB协议
支持崩溃恢复的原子广播协议，用于实现数据一致性

```
原子广播
1、leader对每一个事务请求都生成一个zxid(64位自增ID，低32位表示消息计数器，高32位表示epoch)
2、leader将带有zxid的消息作为一个propose分发给集群中的每一个follower节点（leader对每一个follower节点维护一个FIFO队列，保证消息的先后）
3、follower将收到的propose写入到磁盘，返回一个ack
4、leader收到合法数量的follower的ack以后(一般是一半)，再发送一个commit

崩溃恢复
时机：当leader失去过半的follower的联系、leader挂了、刚启动
问题：已经被处理的消息不能丢失(选举zxid最大的为leader)、被丢弃的消息不能再次出现(旧节点启动后，epoch比较小，所以不会成为主节点，上面没提交的propose会被丢弃)
原理：leader选举出新的leader后，epoch会加1，然后leader会跟所有的follower通信，比对zxid，将没有同步的消息通过FIFO队列同步到每一个follower；前一个leader重启后，因为epoch比较小，所以不可能选举为leader，其未提交的消息会被丢弃
```

- leader选举

```
fastleader
zxid最大会被选举为leader，越大表示数据越新
myid越大，在leader选举中权重越大
epoch每一轮投票都会递增
启动的时候或者leader挂了

1、每个节点都会发送自己（myid,zxid,epoch）给集群的每一个节点
2、每个节点收到其他节点的信息，会依次比较epoch zxid myid，大的会被投票
3、统计投票，最终有一半以上的节点都投同一个节点，然后该节点就会变为leading状态，并转为leader节点
```

- 节点状态
```
looking(选举状态) 
leading(leader节点状态)
following 
observing
```

- 数据存储

```
代码中存储在CurrentHashMap存储
事务日志：zoo.cfg中datadir目录
快照日志：同上
运行时日志：bin/zookeeper.out
```







