##### Hystrix特点
```
1、包裹请求：使用HystrixCommand包裹对依赖的调用逻辑，每个命令在独立的线程中执行，使用了设计模式中的“命令模式”；
2、跳闸机制：当某服务的错误率超过一定阈值时，Hystrix可以自动或者手动跳闸，停止请求该服务一段时间；
3、资源隔离：Hystrix为每个依赖都维护了一个小型的线程池（或者信号量）。如果该线程已满，则发向该依赖的请求就会被立即拒绝，而不是排队等候，从而加速失败判定；
4、监控：Hystrix可以近乎实时地监控运行指标和配置的变化，例如成功、失败、超时、以及被拒绝的请求等；
5、回退机制：当请求失败、超时、被拒绝，或当断路器打开时，执行回退逻辑，回退逻辑由开发人员自行提供，如返回一个缺省值；
6、自我修复：断路器打开一段时间后，会自动进入“半开”状态，此时断路器可允许一个请求访问依赖的服务，若请求成功，则断路器关闭，否则断路器转为“打开”状态；
```
##### HystrixRequestContext实现请求级别的context

```
常规操作：
1、在filter拦截器中拦截请求，然后初始化HystrixRequestContext和HystrixRequestVariable
2、HystrixRequestContext实现
    requestVariables属性：类型为ThreadLocal<HystrixRequestContext>)，利用ThreadLocal,每个线程各有一份HystrixRequestContext
    state属性：类型为ConcurrentHashMap<HystrixRequestVariableDefault<?>,HystrixRequestVariableDefault.LazyInitializer<?>>)，
3、HystrixRequestVariable设置value时，实际是先从requestVariables获取当前线程的HystrixRequestContext，在获取该HystrixRequestContext的state属性，然后再把当前HystrixRequestVariable作为key，实际值作为value保存下来
4、在HystrixContextRunnable和HystrixContextCallable有如下操作
    在构造函数中，将原始任务Runnable包装成Callable,创建了一个新的callable
    然后获取到当前线程的HystrixRequestContext保存下来
    运行实际的Runnable之前，先保存此线程的HystrixRequestContext，然后设置当前线程的HystrixRequestContext为上一级线程,因此两个线程是同一个HystrixRequestContext
    最后还原当前线程的HystrixRequestContext
```

##### 三种熔断规则

```
熔断降级: 在指定时间内，超过一定的请求失败了，则触发熔断规则，默认熔断时间为5秒，5秒后在将前端请求转发到服务器，如果请求是成功的话，则关闭熔断器
超时降级: 默认超时时间为1秒
资源隔离触发降级：线程池或者信号量不够
```

##### 回退方法规则
```
必须与原方法参数个数、类型一致
```

##### Fallback的情况和熔断器事件类型

| 失败情况                      | 原始异常类型               | 是否触发fallback | 是否纳入熔断器统计 | 事件类型             |
| ----------------------------- | -------------------------- | ---------------- | ------------------ | -------------------- |
| short-circuited短路           | RuntimeException           | 是               | 是                 | SHORT_CIRCUITED      |
| threadpool-rejected线程池拒绝 | RejectedExecutionException | 是               | 是                 | THREAD_POOL_REJECTED |
| semaphore-rejected信号量拒绝  | RuntimeException           | 是               | 是                 | SEMAPHORE_REJECTED   |
| timed-out超时                 | TimeoutException           | 是               | 是                 | TIMEOUT              |
| failed失败                    | 目标方法抛出的异常类型     | 是               | 是                 | FAILURE              |
| HystrixBadRequestException    | 该异常亦由目标方法抛出     | 否               | 否                 | 无                   |

##### 断路器状态

```
Closed：熔断器关闭状态，调用失败次数积累，到了阈值（或一定比例）则启动熔断机制；
Open：熔断器打开状态，此时对下游的调用都内部直接返回错误，不走网络，但设计了一个时钟选项，默认的时钟达到了一定时间（这个时间一般设置成平均故障处理时间，也就是MTTR），到了这个时间，进入半熔断状态；
Half-Open：半熔断状态，允许定量的服务请求，如果调用都成功（或一定比例）则认为恢复了，关闭熔断器，否则认为还没好，又回到熔断器打开状态； 

关键参数配置：
sleepWindowInMillseconds:服务熔断后(closed)恢复到半打开(halfopen)状态的时间窗口，以毫秒为单位。
requestVolumeThreshold:熔断状态下尝试进入半打开状态这个时间里允许使用正常逻辑处理的并发请求数
errorThresholdPercentage:服务进入熔断状态的错误比例。
```
##### 两种模式执行逻辑

```
1、信号量隔离：execution.isolation.strategy设置为SEMAPHORE
2、线程隔离：execution.isolation.strategy设置为THREAD
线程池方式下业务请求线程和执行依赖的服务的线程不是同一个线程、各个服务互不影响、但是存在上下文切换的开销；信号量方式下业务请求线程和执行依赖服务的线程是同一个线程、没有上下文切换、不支持异步、多个依赖请求时串行
```
##### 数据统计方式
```
Hystrix通过滑动窗口来统计数据，窗口大小为10秒，包含十个统计段
```

##### 基本实现原理

```
在HystrixCommandAspect(通过@Aspect定义了切面)中，定义了两个切点，一个是HyxtrixCommand，一个是HystrixCollapser
```

