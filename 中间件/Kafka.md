##### Topic & Partition
```
每一条消息被发送到broker中，会根据partition规则选择被存储到哪一个partition。如果partition规则设置的合理，所有消息可以均匀分布到不同的partition里，这样就实现了水平扩展。（一个topic可以认为一个一类消息,每个topic将被分成多个partition,每个partition在存储层面是append log文件。任何发布到此partition的消息都会被追加到log文件的尾部,每条消息在文件中的位置称为offset(偏移量)，offset为一个long型的数字，它唯一标记一条消息。每条消息都被append到partition中，是顺序写磁盘，因此效率非常高
```

##### Kafka文件存储机制

```
Kafka中消息是以topic进行分类的，topic在物理层面以partition为分组，一个topic可以分成若干个partition，partition还可以细分为segment，一个partition物理上由多个segment组成
partition：partition的名称规则为topic名称+有序序号，第一个序号从0开始计，最大的序号为partition数量减1
segment：每个partition(目录)相当于一个巨型文件被平均分配到多个大小基本相等的segment(段)数据文件中，提高磁盘的利用率。每个partition只需要支持顺序读写就行
segment组成：由两部分组成，分别为“.index”文件和“.log”文件，分别表示为segment索引文件和数据文件
```
##### 复制原理和同步方式

```
HW：取一个partition对应的ISR中最小的LEO作为HW，consumer最多只能消费到HW所在的位置。另外每个replica都有HW,leader和follower各自负责更新自己的HW的状态。对于leader新写入的消息，consumer不能立刻消费，leader会等待该消息被所有ISR中的replicas同步后更新HW，此时消息才能被consumer消费
LEO：当前partition的log最后一条Message的位置
```
##### ISR
```
ISR(In-Sync Replicas)：这个是指副本同步队列
AR：所有的副本(replicas)统称为Assigned Replicas，ISR是AR中的一个子集，由leader维护ISR列表
OSR：Outof-Sync Replicas
主leader partition只能从ISR中选取，选取ISR中第一个
```
##### 配置
```
request.required.acks：1(leader partition确认)、0(不等待)、-1(ISR中所有响应)
request.required.acks=：设定ISR中的最小副本数是多少，默认值为1
min.insync.replicas：最小写入副本数的个数
unclean.leader.election.enable：leader的选举是否允许从非ISR中
replication.factor：副本数
producer.type：同步还是异步
```
##### kafka的分区分配策略

```
1. 如果consumer比partition多，是浪费，因为kafka的设计是在一个partition上是不允许并发的，所以consumer数不要大于partition数
2. 如果consumer比partition少，一个consumer会对应于多个partitions，这里主要合理分配consumer数和partition数，否则会导致partition里面的数据被取的不均匀。最好partiton数目是consumer数目的整数倍，所以partition数目很重要，比如取24，就很容易设定consumer数目
3. 如果consumer从多个partition读到数据，不保证数据间的顺序性，kafka只保证在一个partition上数据是有序的，但多个partition，根据你读的顺序会有不同
4. 增减consumer，broker，partition会导致rebalance，所以rebalance后consumer对应的partition会发生变化
```
##### 分区分配策略的触发条件

```
1. 同一个consumer group内新增了消费者
2. 消费者离开当前所属的consumer group，比如主动停机或者宕机
3. topic新增了分区（也就是分区数量发生了变化）
```
##### 分区分配策略

```
RangeAssignor（范围分区）：Range策略是对每个主题而言的，首先对同一个主题里面的分区按照序号进行排序，并对消费者按照字母顺序进行排序。那么前m(分区数％消费者数量)个消费者每个分配n()+l个分区，后面的（消费者数量-m)个消费者每个分配n个分区; 弊端就是无法平均的情况下，前面的消费者总是多分分区
RoundRobinAssignor（轮询分区）：轮询分区策略简单说就是轮训所有消费者，一个消费者给一个分区，直到分区分配完毕；条件是每个消费者订阅的主题必须是相同的
StrickyAssignor 分配策略：又叫粘滞策略，分配上类似于轮训，同时保证重分配时尽可能和上次分配保持相同，从而减少分区移动
```
##### coordinator

```
作用：执行对于consumer group的管理，执行Rebalance
如何确定coordinator：消费者向kafka集群中的任意一个broker发送一个GroupCoordinatorRequest请求，服务端会返回一个负载最小的broker节点的id，并将该broker设置为coordinator
分配策略如何确定：每个消费者都可以设置自己的分区分配策略，每个consumer都会把自己支持的分区分配策略发送到coordinator，并投票选择一个票数最多的为实际分配的策略
```

##### 如何保存消费端的消费位置
```
同一topic下的不同分区包含的消息是不同的。每个消息在被添加到分区时，都会被分配一个offset（称之为偏移量），它是消息在此分区中的唯一编号，kafka通过offset保证消息在分区内的顺序，offset的顺序不跨分区，即kafka只保证在同一个分区内的消息是有序的； 对于应用层的消费来说，每次消费一个消息并且提交以后，会保存当前消费到的最近的一个offset
在kafka中，提供了一个consumer_offsets_*的一个topic，把offset信息写入到这个topic中，此topic默认有50个分区，根据groupid的hashcode能直到在那个分区，
```
##### 如何处理所有的Replica不工作的情况

```
在ISR中至少有一个follower时，Kafka可以确保已经commit的数据不丢失，但如果某个Partition的所
有Replica都宕机了，就无法保证数据不丢失了
1. 等待ISR中的任一个Replica“活”过来，并且选它作为Leader -- 保证一致性
2. 选择第一个“活”过来的Replica（不一定是ISR中的）作为Leader -- 保证可用性
```
##### producer的ack

```
表示producer发送消息到broker上以后的确认值
0：表示producer不需要等待broker的消息确认。时延最小但同时风险最大
1：表示producer只需要获得kafka集群中的leader节点确认即可，择时延较小同时确保了leader节点确认接收成功。
all(-1)：需要ISR中所有的Replica给予接收确认，速度最慢，安全性最高，但是由于ISR可能会缩小到仅包含一个Replica，所以设置参数为all并不能一定避免数据丢失，
```
##### 日志清除策略

```
前面提到过，日志的分段存储，一方面能够减少单个文件内容的大小，另一方面，方便kafka进行日志清理。日志的清理策略有两个
1. 根据消息的保留时间(log.retention.hours)，当消息在kafka中保存的时间超过了指定的时间，就会触发清理过程
2. 根据topic存储的数据大小(log.retention.bytes)，当topic所占的日志文件大小大于一定的阀值，则可以开始删除最旧的消息。kafka会启动一个后台线程，定期检查是否存在可以删除的消息
```
##### 日志压缩策略
```
服务端会在后台启动启动Cleaner线程池，定期将相同的key进行合并，只保留最新的value值
```
