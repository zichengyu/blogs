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
主从选举、负载均衡、分布式锁、配置中心、注册中心等
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
2、leader将带有zxid的消息作为一个propose分发给集群中的每一个follower节点（leader对每一个follower节点维护一个FIFO队列(LearnerHandler)，保证消息的先后）
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

- Watcher原理
```
客户端在向Zookeeper服务器注册Watcher的同时，会将Watcher对象存储在客户端的ZKWatchManager中，当Zookeeper服务器触发Watcher事件后，会向客户端发送通知，客户端收到通知后，会从ZKWatchManager获取对应的Watcher对象来执行回调逻辑

1、一次性：无论是客户端还是服务端，一旦一个watch被触发，zk就会将其从对应的存储中移除，因此开发人员要记得触发后重新注册，此设计可有效减轻服务端的压力，试想一个更新非常频繁的节点，如果其watch是一直存在的话，那么服务端的压力会非常大
2、串行：客户端的watch回调是一个串行同步的过程，这为我们保证了顺序，开发人员需注意不要因为一个watch的处理逻辑，影响了所有watch的回调
3、轻量：WatchedEvent是整个zk中Watcher通知的最小单元，它仅包含通知状态、事件类型、节点路径。即他只会告诉客户端发生了事件，对于事件的具体变更，需要客户端主动重新去获取
```

ZK权限校验ACL

```
ACL的表示：scheme(权限模式):id(权限对象):permission(权限)
权限模式:IP、Digest(类似用户名密码)、World(开放权限模式)、Super
权限对象：权限授予的用户或指定实体，例如IP模式下的一个IP段、Digest模式下的一个用户名和密码
权限：CREATE、DELETE、READ、WRITE、ADMIN

自定义权限控制器
```

- [ZK初始化过程](https://github.com/yu757371316/blogs/blob/master/images/ZK%E5%AE%A2%E6%88%B7%E7%AB%AF%E5%88%9D%E5%A7%8B%E5%8C%96%E8%BF%87%E7%A8%8B.png)

```
ClientCnxn：客户端网络连接器，管理客户端和服务器的网络交互,并进行一系列网络通信,其底层I/O处理器是ClientCnxnSocket
包括以下组件：
  ClientWatchManager：客户端Watcher管理器
  SendThread：I/O线程，负责客户端和服务端的网络交互
    客户端会将ClientCnxnSocket分配给SendThread作为底层网络I/O处理器
  EventThread：事件线程，负责对服务端事件进行处理
    WaitingEvents：EventThread收到事件后，会将事件对象放到该待客户端处理的事件队列中。之后EventThread不断从WaitingEvents取出待处理的Event，从ClientWatchManager取出对应的Watcher，调用其process方法完成通知
  HostProvider：ZK服务器地址列表管理器，保存构造方法中传入的服务器地址列表
    地址会被解析成多个InetSocketAddress，打散顺序后存放到一个循环列表中，每次调用next都返回一个有效的InetSocketAddress
  pendingQueue：服务端响应等待队列
  outgoingQueue：客户端请求发送队列
```
- [ZK单机版服务端启动流程](https://github.com/yu757371316/blogs/blob/master/images/ZK%E5%8D%95%E6%9C%BA%E7%89%88%E6%9C%8D%E5%8A%A1%E7%AB%AF%E5%90%AF%E5%8A%A8%E6%B5%81%E7%A8%8B.png)
```
1、QuorumPeerMain启动，解析配置文件zoo.cfg
2、创建并启动历史文件清理器DatadirCleanupManager，可自动清理历史数据文件、包含对事务日志和快照数据文件进行定时清理
3、判断是单机还是集群，单机模式则委托给ZooKeeperServerMain进行启动处理
4、创建服务器统计器serverStats，运行时的统计器，包含服务器运行时的最基本信息
5、创建数据管理器FileTxnSnapLog，包含一些列操作数据文件的接口，包含事务日志文件和快照数据文件
6、设置服务器ticketTime和会话超时时间设置
7、创建、初始化并启动服务端网络连接工厂ServerCnxnFactory
8、本地数据恢复，从本地快照数据文件和事务日志文件中进行数据恢复
9、创建并启动服务端会话管理器sessionTracker
10、初始化服务端的请求处理链，zk请求处理方式为典型的责任链模式，单机模式下主要是PrepRequestProcessor、SyncRequestProcessor、FinalRequestProcessor
11、注册JMX服务，暴露一些运行时的信息
12、注册zk服务器实例，此时即可正常访问
```
- [ZK集群版服务端启动流程](https://github.com/yu757371316/blogs/blob/master/images/ZK%E9%9B%86%E7%BE%A4%E7%89%88%E6%9C%8D%E5%8A%A1%E7%AB%AF%E5%90%AF%E5%8A%A8%E6%B5%81%E7%A8%8B.png)
```
不同之处
1、QuorumPeer，zookeeperServer的托管者，代表集群中的一台机器，在运行时会不管检查实例的状态，并根据情况发起选举，其初始状态是Looking
2、ZKDatabase zk内存数据库，负责管理zk所有会话记录、dataTree及事务日志的存储
3、初始化leader选举，默认只支持fastLeaderElection，选举时ZXID > myid
```
- [LEADER服务器请求处理链](https://github.com/yu757371316/blogs/blob/master/images/ZK%E4%B8%ADLeader%E6%9C%8D%E5%8A%A1%E5%99%A8%E8%AF%B7%E6%B1%82%E5%A4%84%E7%90%86%E9%93%BE.png)
```
PrepRequestProcessor：Leader请求的预处理器，Leader服务器的第一个处理器，对于事务请求，会对客户端请求进行预处理，如创建请求事务头、事务体、会话检查、ACL检查、版本检查等
ProposalRequestProcessor：Leader服务器的事务投票处理器，也是Leader事务处理流程的发起者。对非事务请求，会直接将请求流转到CommitProcessor，不做其他处理；对事务请求，将请求交给CommitProcessor之外，并根据请求类型创建对应的proposal提议，并发送给所有的follower服务器发起一次集群内的投票。同时该处理器还会将事务请求交付给SyncRequestProcessor
SyncRequestProcessor：事务日志的记录处理器，将事务日志记录到事务日志文件中，同时触发zk进行数据快照
AckRequestProcessor：Leader特有的处理器，负责SyncRequestProcessor处理器完成事务日志记录后，向Proposal的投票收集器发送ACK反馈，以通知投票收集器当前服务器已完成该proposal的事务日志记录
CommitProcessor：事务提交处理器，非事务请求直接交给下一处理器；事务请求时，会等待集群内对proposal的投票直到该proposal可被提交；利用该processor处理器，每个服务器可很好地控制对事务请求的顺序处理
ToBeAppliedRequestProcessor：保留一个toBeApplied队列，存储那些已经被CommitProcessor处理过的可被提交的proposal；将请求逐个交付给FinalRequestProcessor处理完之后，在将其从toBeApplied队列中移除
FinalRequestProcessor：客户端请求返回之前的收尾工作，包括创建客户端响应；对数据请求，还会负责将事务应用到内存数据库中去

``` 
##### [ZK集群版请求链路](https://github.com/yu757371316/blogs/blob/master/images/ZK%E9%9B%86%E7%BE%A4%E4%B8%8B%E8%AF%B7%E6%B1%82%E9%93%BE%E8%B7%AF.png)












