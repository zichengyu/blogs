##### AbstractServerPredicate
```
AbstractServerPredicate，它的作用就是在众多Server的列表中，通过一定的过滤策略，T除不合格的Server，留下来合格的Server列表，进而供以选择。

负载均衡策略的核心之一就是对已知的服务列表进行过滤，留下一堆合格的Server进而按照一定规则进行choose选择

CompositePredicate：组合模式，如果主的Predicate产生的过滤服务器太少，它将一个接一个地尝试fallback的Predicate，直到过滤服务器的数量超过一定数量的阈值或百分比阈值。
AvailabilityPredicate：主要是对服务的可用性进行过滤（过滤掉不可用的服务器）
ZoneAvoidancePredicate：当某个zone糟糕到统计达到了threshold阈值，那么就会过滤掉这个zone里面所有的Server们，ZoneAvoidanceRule就是基于此断言器来实现服务器过滤的，对应的负载均衡器有ZoneAwareLoadBalancer，它是SpringCloud下默认的负载均衡器。
ZoneAffinityPredicate：选取指定zone区域内的Server，言外之意就是会过滤掉其它区域的Server

```
##### 负载均衡策略

```
IRule：所有负载均衡策略的父接口，里边的核心方法就是choose方法，用来选择一个服务实例
AbstractLoadBalancerRule：里边主要定义了一个ILoadBalancer，辅助负责均衡策略选取合适的服务端实例
RandomRule：随机选择一个服务实例，
    原理：random生成随机数方式
RoundRobinRule：线性负载均衡策略，BaseLoadBalancer负载均衡器中默认采用的负载均衡策略
    原理：先通过incrementAndGetModulo方法获取一个下标，这个下标是一个不断自增长的数先加1然后和服务清单总数取模之后获取到的(所以这个下标从来不会越界)，拿着下标再去服务清单列表中取服务，每次循环计数器都会加1
RetryRule:载均衡策略带有重试功能
    原理：每次还是采用RoundRobinRule中的choose规则来选择一个服务实例，如果选到的实例正常就返回，如果选择的服务实例为null或者已经失效，则在失效时间deadline之前不断的进行重试
WeightedResponseTimeRule：
    原理：有一个名叫DynamicServerWeightTask的定时任务，默认情况下每隔30秒会计算一次各个服务实例的权重，如果一个服务的平均响应时间越短则权重越大，那么该服务实例被选中执行任务的概率也就越大。
BestAvailableRule：
    原理：找出并发请求最小的服务实例来使用，为空则使用线性轮询
PredicateBasedRule：
    原理：通过内部定义的一个过滤器过滤出一部分服务实例清单，然后再采用线性轮询的方式从过滤出来的结果中选取一个服务实例
ZoneAvoidanceRule：
    原理：ZoneAvoidancePredicate为主过滤条件和以AvailabilityPredicate为次过滤条件组成的一个叫做CompositePredicate的组合过滤条件，过滤成功之后，继续采用线性轮询的方式从过滤结果中选择一个出来。
```
##### 基本配置
```
ribbon:
  eager-load:
    enabled: true
    #说明：同一台实例的最大自动重试次数，默认为1次，不包括首次
    MaxAutoRetries: 1
    #说明：要重试的下一个实例的最大数量，默认为1，不包括第一次被调用的实例
    MaxAutoRetriesNextServer: 1
    #说明：是否所有的操作都重试，默认为true
    OkToRetryOnAllOperations: true
    #说明：从注册中心刷新服务器列表信息的时间间隔，默认为2000毫秒，即2秒
    ServerListRefreshInterval: 2000
    #说明：使用Apache HttpClient连接超时时间，单位为毫秒
    ConnectTimeout: 3000
    #说明：使用Apache HttpClient读取的超时时间，单位为毫秒
    ReadTimeout: 3000
```
##### Ribbon和Hystrix的超时时间配置的关系

```
Hystrix的超时时间=Ribbon的重试次数(包含首次)*(ribbon.ReadTimeout + ribbon.ConnectTimeout)
Ribbon的重试次数=1 + ribbon.MaxAutoRetries+ ribbon.MaxAutoRetriesNextServer  +  (ribbon.MaxAutoRetries * ribbon.MaxAutoRetriesNextServer)
以上面基本配置为例
Ribbon的重试次数=1+(1+1+1)=4，
Hystrix的超时配置应该>=4*(3000+3000)=24000毫秒。
在Ribbon超时但Hystrix没有超时的情况下，Ribbon便会采取重试机制；而重试期间如果时间超过了Hystrix的超时配置则会立即被熔断（fallback）。
```
