##### [dubbo下zk作为注册中心原理图](https://github.com/yu757371316/blogs/blob/master/images/Dubbo%E4%B8%8Bzk%E6%B3%A8%E5%86%8C%E4%B8%AD%E5%BF%83%E7%BB%93%E6%9E%84%E5%9B%BE.png)

```
以dubbo作为根目录
以service作为二级目录
providers或consumers作为三级目录
服务地址作为四级目录
```
##### 负载均衡算法

```
RandomLoadBalance：权重随机算法，根据权重值进行随机负载
LeastActiveLoadBalance：最少活跃调用数算法，活跃调用数越小，表明该服务提供者效率越高，单位时间内可处理更多的请求这个是比较科学的负载均衡算法。
ConsistentHashLoadBalance：hash一致性算法，相同参数的请求总是发到同一提供者
RoundRobinLoadBalance：加权轮询算法
```
##### Dubbo 容错方案

```
Failover Cluster：失败自动切换，当出现失败，重试其它服务器。retries配置重试次数；通常用于读操作，但重试会带来更长延迟。
Failfast Cluster：快速失败，只发起一次调用，失败立即报错。通常用于非幂等性的写操作，比如新增记录。
Failsafe Cluster：失败安全，出现异常时，直接忽略。通常用于写入审计日志等操作。
Failback Cluster：失败自动恢复，后台记录失败请求，定时重发。通常用于消息通知操作。
Forking Cluster：并行调用多个服务器，只要一个成功即返回。通常用于实时性要求较高的读操作，但需要浪费更多服务资源。可通过 forks="2" 来设置最大并行数。
Broadcast Cluster：广播调用所有提供者，逐个调用，任意一台报错则报错
```
##### Dubbo SPI

```
1、需要在 resource目录下配置META-INF/dubbo或者META-INF/dubbo/internal或者META-INF/services，并基于SPI接口去创建一个文件
2、文件名称和接口名称保持一致，文件内容和SPI有差异，内容是 KEY 对应 Value；Dubbo针对的扩展点非常多，可以针对协议、拦截、集群、路由、负载均衡、序列化、容器…几乎里面用到的所有功能，都可以实现自己的扩展，我觉得这个是dubbo比较强大的一点。
```
##### @SPI和@Adaptive

```
@SPI：@SPI注解注释接口，说明他是一个扩展点
@Adaptive:要么注释在扩展点@SPI的方法上,要么注释在其实现类的类定义上,设计的目的是为了识别固定已知类和扩展未知类
    注释在@SPI接口的方法上：代表自动生成和编译一个动态的Adpative类，它主要是用于SPI，因为spi的类是不固定、未知的扩展类，所以设计了动态$Adaptive类.
    修饰类：主要作用于固定已知类,Dubbo不会为该类生成代理类，表明当前类是自适应扩展实现(每个扩展点最多只能有一个自适应实现，如果所有实现中没有被@Adaptive注释的，那么dubbo会动态生成一个自适应实现类)，此情况很少,在Dubbo中,仅有两个类被Adaptive注解了，分别是 AdaptiveCompiler 和AdaptiveExtensionFactory
每个扩展点可以有多个可自动激活的扩展点实现(使用@Activate注解)    
```
##### dubbo 负载均衡-随机算法

```
原理：如果各实例权重相同，则随机取一个，如果不同，则循环让offset数减去服务提供者权重值,当offset小于0时,返回相应的 Invoker。
举例：我们有 servers = [A, B, C]，weights =[5,3,2],
如offset=7。
第一次循环,offset-5=2>0，即offset>5，表明其不会落在服务器A对应的区间上。 
第二次循环，offset-3=-1<0,即5<offset<8
表明其会落在服务器 B 对应的区间上
```


