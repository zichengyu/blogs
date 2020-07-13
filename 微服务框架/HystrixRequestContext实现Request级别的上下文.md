# 一、简介

 在微服务架构中，我们会有这样的需求，A服务调用B服务，B服务调用C服务，ABC服务都需要用到当前用户上下文信息（userId、orgId等），那么如何实现呢？
**方案一：** 拦截器加上ThreadLocal实现，但是如果在这次请求中创建了一个新的线程就拿不到了，也就是无法跨线程传递数据。
**方案二：** 使用拦截器加上 HystrixRequestContext 这个 request level 的 context实现，即保存到HystrixRequestContext中的数据在整个请求中都能访问。

# 二、使用

## 2.1代码示例

首先需要在pom文件引入依赖hystrix

```
<dependency>
      <groupId>com.netflix.hystrix</groupId>
      <artifactId>hystrix-core</artifactId>
      <version>1.5.12</version>
    </dependency>
```

保存上下文信息的对象ServiceContextHolder

```java
package cn.sp.context;

import com.netflix.hystrix.strategy.concurrency.HystrixRequestContext;
import com.netflix.hystrix.strategy.concurrency.HystrixRequestVariableDefault;

public class ServiceContextHolder {

  private static final HystrixRequestVariableDefault<ServiceContext> context = new HystrixRequestVariableDefault<>();


  public static ServiceContext getServiceContext() {
    initServiceContext();
    return context.get();
  }

  public static void setServiceContext(ServiceContext serviceContext) {
    initServiceContext();
    context.set(serviceContext);
  }

  private static void initServiceContext() {
    if (!HystrixRequestContext.isCurrentThreadInitialized()) {
      HystrixRequestContext.initializeContext();
    }
  }

  public static void destroy() {
    if (HystrixRequestContext.isCurrentThreadInitialized()) {
      HystrixRequestContext.getContextForCurrentThread().shutdown();
    }
  }
}
```

ServiceContextInterceptor的作用是将请求头中的userId保存到上下文对象中。

```java
@Slf4j
public class ServiceContextInterceptor extends HandlerInterceptorAdapter {


  @Override
  public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
      throws Exception {
    initServiceContext(request, request.getRequestURL().toString());
    return true;
  }

  @Override
  public void postHandle(HttpServletRequest request, HttpServletResponse response, Object handler,
      @Nullable ModelAndView modelAndView) throws Exception {
    ServiceContextHolder.destroy();
  }

  private void initServiceContext(HttpServletRequest request, String url) {
    ServiceContext serviceContext = new ServiceContext();
    String userId = request.getHeader("userId");
    serviceContext.setUserId(Long.valueOf(userId));
    ServiceContextHolder.setServiceContext(serviceContext);
  }
}
```

添加拦截器配置

```java
@Configuration
@EnableWebMvc
@Import(value = {RestResponseBodyAdvice.class})
public class MvcConfig implements WebMvcConfigurer {

  @Bean
  public ServiceContextInterceptor getServiceContextInterceptor() {
    return new ServiceContextInterceptor();
  }

  @Override
  public void addInterceptors(InterceptorRegistry registry) {
    registry.addInterceptor(getServiceContextInterceptor()).addPathPatterns("/request-context/**");
  }
 
}
```

用于测试的RequestContextTestController

```java
@RestController
@RequestMapping("request-context")
@Slf4j
public class RequestContextTestController {

  @RequestMapping(value = "test", method = RequestMethod.GET)
  public String test() {
    System.out.println("请求的用户id:" + ServiceContextHolder.getServiceContext().getUserId() + "");

    HystrixContextRunnable runnable =
        new HystrixContextRunnable(() -> {
          //从新的线程中获取当前用户id
          ServiceContext context = ServiceContextHolder.getServiceContext();
          System.out.println("新线程的用户id：" + context.getUserId());
          context.setUserId(110L);
        });

    new Thread(runnable).start();

    try {
      Thread.sleep(100);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    return ServiceContextHolder.getServiceContext().getUserId() + "";
  }
}
```

**注意：** 只有使用HystrixContextRunnable或HystrixContextCallable创建线程才能在线程间传递数据，JDK自带的是无效的。

## 2.2测试

使用postman发送请求,请求示例

![img](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9pbWcyMDE4LmNuYmxvZ3MuY29tL2Jsb2cvMTE2NzA4Ni8yMDE5MDkvMTE2NzA4Ni0yMDE5MDkwODEwMjA0MTU0My0xOTU3MzQ1MDkyLnBuZw?x-oss-process=image/format,png)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)![img](https://img-blog.csdnimg.cn/2020051114330971.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3l1NzU3MzcxMzE2,size_16,color_FFFFFF,t_70)![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)
请求头中的userId是22，返回结果却变成110，说明在新线程中改变了ServiceContextHolder中保存的userId。

控制台日志如下：

```shell
请求的用户id:22
2019-08-31 14:25:29.787 [http-nio-80-exec-1] WARN  c.n.c.sources.URLConfigurationSource - No URLs will be polled as dynamic configuration sources.
2019-08-31 14:25:29.787 [http-nio-80-exec-1] INFO  c.n.c.sources.URLConfigurationSource - To enable URLs as dynamic configuration sources, define System property archaius.configurationSource.additionalUrls or make config.properties available on classpath.
2019-08-31 14:25:29.798 [http-nio-80-exec-1] INFO  c.n.config.DynamicPropertyFactory - DynamicPropertyFactory is initialized with configuration sources: com.netflix.config.ConcurrentCompositeConfiguration@a6f6807
新线程的用户id：22
```

说明新线程也能获取到ServiceContextHolder中的数据，这种又是怎么实现的呢？下面介绍原理。

# 三、原理

上下文信息其实是保存在HystrixRequestVariableDefault类型的变量中，所以先看看这个类的源码。
HystrixRequestVariableDefault是HystrixRequestVariable接口的实现类，HystrixRequestVariable接口表示request level的属性，仅提供了get()来获取属性。

```java
public interface HystrixRequestVariable<T> extends HystrixRequestVariableLifecycle<T> {

    public T get();

}
```

HystrixRequestVariableDefault和ThreadLocal一样，提供了 T get() 和 set(T value) 两个工具方法。

```java
public class HystrixRequestVariableDefault<T> implements HystrixRequestVariable<T> {
    static final Logger logger = LoggerFactory.getLogger(HystrixRequestVariableDefault.class);

    @SuppressWarnings("unchecked")
    public T get() {
        if (HystrixRequestContext.getContextForCurrentThread() == null) {
            throw new IllegalStateException(HystrixRequestContext.class.getSimpleName() + ".initializeContext() must be called at the beginning of each request before RequestVariable functionality can be used.");
        }
        // 拿到当前线程的存储结构，以自己为key索引数据
        ConcurrentHashMap<HystrixRequestVariableDefault<?>, LazyInitializer<?>> variableMap = HystrixRequestContext.getContextForCurrentThread().state;

        // short-circuit the synchronized path below if we already have the value in the ConcurrentHashMap
        LazyInitializer<?> v = variableMap.get(this);
       ...
    }
   
    public void set(T value) {
    // 拿到当前线程的存储结构，以自己为key来存储实际的数据。
        HystrixRequestContext.getContextForCurrentThread().state.put(this, new LazyInitializer<T>(this, value));
    }
    
}
```

set/get方法都调用了HystrixRequestContext的方法完成的，HystrixRequestContext的部分源码如下：

```java
public class HystrixRequestContext implements Closeable {


   //每个线程的ThreadLocal将保存HystrixRequestVariableState
    private static ThreadLocal<HystrixRequestContext> requestVariables = new ThreadLocal<HystrixRequestContext>();

    // 当前线程是否初始化了HystrixRequestContext
    public static boolean isCurrentThreadInitialized() {
        HystrixRequestContext context = requestVariables.get();
        return context != null && context.state != null;
    }

    // 从当前线程获取HystrixRequestContext
    public static HystrixRequestContext getContextForCurrentThread() {
        HystrixRequestContext context = requestVariables.get();
        if (context != null && context.state != null) {
         
            return context;
        } else {
            return null;
        }
    }

    public static void setContextOnCurrentThread(HystrixRequestContext state) {
        requestVariables.set(state);
    }

     // 在每个请求开始的时候调用此方法，创建一个HystrixRequestContext,并与当前线程关联
    public static HystrixRequestContext initializeContext() {
        HystrixRequestContext state = new HystrixRequestContext();
        requestVariables.set(state);
        return state;
    }


 ConcurrentHashMap<HystrixRequestVariableDefault<?>, HystrixRequestVariableDefault.LazyInitializer<?>> state = new ConcurrentHashMap<HystrixRequestVariableDefault<?>, HystrixRequestVariableDefault.LazyInitializer<?>>();

   
}
```

可以看出实际数据是存储在state这个ConcurrentHashMap中的，每个线程关联一个HystrixRequestContext，每个HystrixRequestContext有个Map结构存储数据，key就是HystrixRequestVariableDefault。

## 如何实现request level context?

HystrixContextRunnable源码如下：

```java
// HystrixContextRunnable是个Runnable,一个可用于执行的任务
public class HystrixContextRunnable implements Runnable {

    private final Callable<Void> actual;
    private final HystrixRequestContext parentThreadState;

    public HystrixContextRunnable(Runnable actual) {
        this(HystrixPlugins.getInstance().getConcurrencyStrategy(), actual);
    }
    
    public HystrixContextRunnable(HystrixConcurrencyStrategy concurrencyStrategy, final Runnable actual) {
        // 获取当前线程的HystrixRequestContext
        this(concurrencyStrategy, HystrixRequestContext.getContextForCurrentThread(), actual);
    }

    // 关键的构造器
    public HystrixContextRunnable(final HystrixConcurrencyStrategy concurrencyStrategy, final HystrixRequestContext hystrixRequestContext, final Runnable actual) {
        
        // 将原始任务Runnable包装成Callable, 创建了一个新的callable
        this.actual = concurrencyStrategy.wrapCallable(new Callable<Void>() {
            @Override
            public Void call() throws Exception {
                actual.run();
                return null;
            }
        });
        // 存储当前线程的hystrixRequestContext
        this.parentThreadState = hystrixRequestContext;
    }

    @Override
    public void run() {
        // 运行实际的Runnable之前先保存当前线程已有的HystrixRequestContext
        HystrixRequestContext existingState = HystrixRequestContext.getContextForCurrentThread();
        try {
            // 设置当前线程的HystrixRequestContext,来自上一级线程,因此两个线程是同一个HystrixRequestContext
            HystrixRequestContext.setContextOnCurrentThread(parentThreadState);
            try {
                actual.call();
            } catch (Exception e) {
                throw new RuntimeException(e);
            }
        } finally {
            // 还原当前线程的HystrixRequestContext
            HystrixRequestContext.setContextOnCurrentThread(existingState);
        }
    }
}
```

![点击并拖拽以移动](data:image/gif;base64,R0lGODlhAQABAPABAP///wAAACH5BAEKAAAALAAAAAABAAEAAAICRAEAOw==)

 