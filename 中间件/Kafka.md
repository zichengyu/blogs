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
