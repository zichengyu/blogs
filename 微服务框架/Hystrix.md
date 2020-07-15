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
