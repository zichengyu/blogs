##### 服务续约

```
Eureka Client 会每隔 30 秒发送一次心跳来续约。通过续约来告知 Eureka Server 该EurekaClient运行正常，没有出现问题。默认情况下，如果 Eureka Server在90秒内没有收到EurekaClient的续约，Server 端会将实例从其注册表中删除，此时间可配置，一般情况不建议更改。
服务续约任务的调用间隔时间，默认为30秒
eureka.instance.lease-renewal-interval-in-seconds=30
服务失效的时间，默认为90秒。
eureka.instance.lease-expiration-duration-in-seconds=90
```
##### 获取注册列表信息

```
Eureka Client 从服务器获取注册表信息，并将其缓存在本地。客户端会使用该信息查找其他服务，从而进行远程调用。该注册列表信息定期（每30秒钟）更新一次。每次返回注册列表信息可能与 Eureka Client 的缓存信息不同，Eureka Client 自动处理。

# 启用服务消费者从注册中心拉取服务列表的功能
eureka.client.fetch-registry=true

# 设置服务消费者从注册中心拉取服务列表的间隔
eureka.client.registry-fetch-interval-seconds=30
```
##### 自我保护机制
```
Eureka Server 在运行期间会去统计心跳失败比例在15分钟之内是否低于85%，如果低于85%，EurekaServer即会进入自我保护机制。
Eureka 自我保护机制是为了防止误杀服务而提供的一个机制。当个别客户端出现心跳失联时，则认为是客户端的问题，剔除掉客户端；当 Eureka 捕获到大量的心跳失败时，则认为可能是网络问题，进入自我保护机制；当客户端心跳恢复时，Eureka会自动退出自我保护机制。
如果在保护期内刚好这个服务提供者非正常下线了，此时服务消费者就会拿到一个无效的服务实例，即会调用失败。对于这个问题需要服务消费者端要有一些容错机制，如重试，断路器等。
```
##### [Eureka 集群原理](https://github.com/yu757371316/blogs/blob/master/images/Eureka%E9%9B%86%E7%BE%A4%E5%8E%9F%E7%90%86.png)
```
Eureka Server 集群相互之间通过Replicate来同步数据，相互之间不区分主节点和从节点，所有的节点都是平等的。在这种架构中，节点通过彼此互相注册来提高可用性，每个节点需要添加一个或多个有效的 serviceUrl 指向其他节点。
所有的操作都会进行节点间复制，将请求复制到其它EurekaServer 当前所知的所有节点中，每个 Eureka Server 同时也是 Eureka Client，多个EurekaServer之间通过P2P的方式完成服务注册表的同步。不过是异步同步的，所以不保证某一时刻数据一定能一致
```
##### Eureka 分区

```
Eureka 提供了 Region 和 Zone 两个概念来进行分区，
region：可以理解为地理上的不同区域
zone：可以简单理解为 region 内的具体机房
Zone内的EurekaClient优先和Zone内的EurekaServer进行心跳同步，同样调用端优先在Zone内的EurekaServer获取服务列表，当Zone 内的EurekaServer挂掉之后，才会从别的 Zone中获取信息。
```
##### Eurka 保证 AP

```
Eureka Server 各个节点都是平等的，几个节点挂掉不会影响正常节点的工作，剩余的节点依然可以提供注册和查询服务。而Eureka Client 在向某个Eureka注册时，如果发现连接失败，则会自动切换至其它节点。只要有一台EurekaServer还在，就能保证注册服务可用(保证可用性)，只不过查到的信息可能不是最新的(不保证强一致性)。
```
##### Eureka 工作流程

```
1、Eureka Server 启动成功，等待服务端注册。在启动过程中如果配置了集群，集群之间定时通过 Replicate 同步注册表，每个EurekaServer都存在独立完整的服务注册表信息
2、Eureka Client启动时根据配置的EurekaServer地址去注册中心注册服务
3、Eureka Client会每30s向EurekaServer发送一次心跳请求，证明客户端服务正常
4、当 Eureka Server90s内没有收到EurekaClient的心跳，注册中心则认为该节点失效，会注销该实例
5、单位时间内 Eureka Server 统计到有大量的 Eureka Client 没有上送心跳，则认为可能为网络异常，进入自我保护机制，不再剔除没有上送心跳的客户端
6、当 Eureka Client 心跳请求恢复正常之后，Eureka Server 自动退出自我保护模式
7、Eureka Client 定时全量或者增量从注册中心获取服务注册表，并且将获取到的信息缓存到本地
8、服务调用时，Eureka Client 会先从本地缓存找寻调取的服务。如果获取不到，先从注册中心刷新注册表，再同步到本地缓存
9、Eureka Client 获取到目标服务器信息，发起服务调用
10、Eureka Client 程序关闭时向 Eureka Server 发送取消请求，Eureka Server 将实例从注册表中删除
```
