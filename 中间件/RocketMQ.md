##### [RocketMQ事务消息概要](https://gitee.com/seeks/blogs/blob/master/images/RocketMq%E4%BA%8B%E5%8A%A1%E6%B6%88%E6%81%AF%E6%A6%82%E8%A6%81.png)

```
事务消息发送及提交：
1、发送消（half消息-会将Topic替换为HalfMessage的Topic）
2、broker响应消息写入结果
3、根据broker响应结果执行本地事务(如果写入失败，此时half消息对业务不可见，本地逻辑也不执行)
4、根据本地事务状态执行Commit或者Rollback（Commit操作生成消息索引,还原topic，则消息对消费者可见)
补偿流程：
1、对没有Commit/Rollback的事务消息(pending状态的消息)，从broker服务端发起一次“回查”
2、Producer收到回查消息，检查回查消息对应的本地事务的状态，根据本地事务状态，重新Commit或者Rollback
补偿阶段用于解决消息Commit或者Rollback发生超时或者失败的情况。
```
##### 定时/延时消息
```
开源版本的RocketMQ中延时消息并不支持任意时间的延时，需要设置几个固定的延时等级，目前默认设置为：1s 5s 10s 30s 1m 2m 3m 4m 5m 6m 7m 8m 9m 10m 20m 30m 1h 2h，从1s到2h分别对应着等级1到18，而阿里云中的版本(要付钱)是可以支持40天内的任何时刻（毫秒级别）
1、Producer在自己发送的消息上设置好需要延时的级别。
2、Broker发现此消息是延时消息，将Topic进行替换成延时Topic，每个延时级别都会作为一个单独的queue，将自己的Topic作为额外信息存储。
3、构建ConsumerQueue
4、定时任务定时扫描每个延时级别的ConsumerQueue。
5、拿到ConsumerQueue中的CommitLog的Offset，获取消息，判断是否已经达到执行时间
6、如果达到，那么将消息的Topic恢复，进行重新投递。如果没有达到则延迟没有达到的这段时间执行任务。
持久化二级TimeWheel时间轮
```
##### 消息的可用性

```
刷盘：同步和异步的策略
主从同步：同步和异步两种模式来进行复制，当然选择同步可以提升可用性，但是消息的发送RT时间会下降10%左右。
```
##### 高性能日志存储

```
commitLog：消息主体以及元数据的存储主体，存储Producer端写入的消息主体内容,消息内容不是定长的。单个文件大小默认1G ，文件名长度为20位，左边补零，剩余为起始偏移量，比如00000000000000000000代表了第一个文件，起始偏移量为0，文件大小为1G=1073741824；当第一个文件写满了，第二个文件为00000000001073741824，起始偏移量为1073741824，以此类推。消息主要是顺序写入日志文件，当文件满了，写入下一个文件
config：保存一些配置信息，包括一些Group，Topic以及Consumer消费offset等信息。
consumeQueue:消息消费队列，引入的目的主要是提高消息消费的性能，ConsumeQueue（逻辑消费队列）作为消费消息的索引，保存了指定Topic下的队列消息在CommitLog中的起始物理偏移量offset，消息大小size和消息Tag的HashCode值。consumequeue文件可以看成是基于topic的commitlog索引文件，故consumequeue文件夹的组织方式如下：topic/queue/file三层组织结构
```
##### 网络模型

```
Netty网络框架   1+N1+N2+M的线程模型
1个acceptor线程，N1个IO线程，N2个线程用来做Shake-hand,SSL验证,编解码;M个线程用来做业务处理。
这样的好处将编解码，和SSL验证等一些可能耗时的操作放在了一个单独的线程池，不会占据我们业务线程和IO线程。
```
##### 消费模式

```
集群消费：同一个GroupId都属于一个集群，一般来说一条消息只会被任意一个消费者处理。
广播消费：广播消费的消息会被集群中所有消费者进行消息，但是要注意一下因为广播消费的offset在服务端保存成本太高，所以客户端每一次重启都会从最新消息消费，而不是上次保存的offset。
```
##### 消费模型

```
两种模型都是客户端主动去拉消息
MQPullConsumer：拉取消息需传入拉取消息的offset和每次拉取多少消息量，具体拉取哪里的消息，拉取多少是由客户端控制。
MQPushConsumer：同样也是客户端主动拉取消息，但是消息进度是由服务端保存，Consumer会定时上报自己消费到哪里，所以Consumer下次消费的时候是可以找到上次消费的点，一般来说使用PushConsumer我们不需要关心offset和拉取多少数据，直接使用即可。
```
##### [重平衡](https://mp.weixin.qq.com/s/8fB-Z5oFPbllp13EcqC9dw)

```
1、重平衡定时任务每隔20s定时拉取broker,topic的最新信息
3、随机(因为消费者客户端启动时会启动一个线程，向所有 broker 发送心跳包)选取当前Topic的一个Broker，获取当前Broker，当前ConsumerGroup的所有机器ID。
3、然后进行策略分配。
由于重平衡是定时做的，所以这里有可能会出现某个Queue同时被两个Consumer消费，所以会出现消息重复投递。
```
