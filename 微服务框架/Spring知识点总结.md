##### Spring 提供了以下 5 种标准的事件：

1.上下文更新事件（ContextRefreshedEvent） ： 该事件会在 ApplicationContext 被初始化或者更
新时发布。 也可以在调用 ConfigurableApplicationContext 接口中的 refresh()方法时被触发。
2.上下文开始事件（ContextStartedEvent） ： 当容器调用 ConfigurableApplicationContext 的
Start()方法开始/重新开始容器时触发该事件。
3.上下文停止事件（ContextStoppedEvent） ： 当容器调用 ConfigurableApplicationContext 的
Stop()方法停止容器时触发该事件。
4.上下文关闭事件（ContextClosedEvent） ： 当 ApplicationContext 被关闭时触发该事件。 容器
被关闭时， 其管理的所有单例 Bean 都被销毁。
5.请求处理事件（RequestHandledEvent） ： 在 Web 应用中， 当一个 http 请求（request） 结束触发
该事件。

##### Spring 框架中都用到了哪些设计模式？

Spring 框架中使用到了大量的设计模式， 下面列举了比较有代表性的：
1、 代理模式：AOP 思想的底层实现技术， Spring 中采用 JDK Proxy 和 CgLib 类库。
2、 单例模式： 在 spring 配置文件中定义的 bean 默认为单例模式。
3、 模板模式： 用来解决代码重复的问题。比如. RestTemplate, JmsTemplate, JpaTemplate。
4、 委派模式： Srping 提供了 DispatcherServlet 来对请求进行分发。
5、 工厂模式： BeanFactory 用来创建对象的实例， 贯穿于 BeanFactory / ApplicationContext 接
口的核心理念。
6、原型模式：prototype作用域的类，每个线程都会创建一个新类。

##### IOC 是什么？

Ioc—Inversion of Control，即“控制反转”，不是什么技术，而是一种设计思想。在Java开发中，Ioc意味着将你设计好的对象交给容器控制，而不是传统的在你的对象内部直接控制。

●谁控制谁，控制什么：传统Java SE程序设计，我们直接在对象内部通过new进行创建对象，是程序主动去创建依赖对象；而IoC是有专门一个容器来创建这些对象，即由Ioc容器来控制对象的创建；谁控制谁？当然是IoC 容器控制了对象；控制什么？那就是主要控制了外部资源获取（不只是对象包括比如文件等）。

●为何是反转，哪些方面反转了：有反转就有正转，传统应用程序是由我们自己在对象中主动控制去直接获取依赖对象，也就是正转；而反转则是由容器来帮忙创建及注入依赖对象；为何是反转？因为由容器帮我们查找及注入依赖对象，对象只是被动的接受依赖对象，所以是反转；哪些方面反转了？依赖对象的获取被反转了。

##### 构造方法注入和设值注入有什么区别？

1、设值注入和传统的JavaBean的写法更相似、更加的直观和自然，更容易理解、接受

2、对于复杂的依赖关系，如果采用构造注入，会导致构造器过于臃肿，难以阅读。Spring在创建Bean实例时，需要同时实例化其依赖的全部实例，因而导致性能下降。而是用设置注入可以避免这些问题。

3、属性可选的情况下，多参数的构造器更加笨重

4、构造注入可以再构造器中决定依赖关系的注入顺序，有依赖的优先注入

5、对于依赖关系无需变化的Bean，构造注入因为没有setter方法，所有的依赖关系全部在构造器内设定。无需担心后续代码对依赖关系的破坏。

##### 自动装配有哪些局限性？

1、重写： 你仍然需要使用 和< property>设置指明依赖， 这意味着总要重写自动装配。
2、原生数据类型:你不能自动装配简单的属性， 如原生类型、 字符串和类。
3、模糊特性： 自动装配总是没有自定义装配精确， 因此， 如果可能尽量使用自定义装配

##### Spring Bean 的生命周期？

Bean 的生命周期由两组回调（call back） 方法组成。
1.初始化之后调用的回调方法。 2.销毁之前调用的回调方法。
Spring 框架提供了以下四种方式来管理 bean 的生命周期事件：
1、 InitializingBean 和 DisposableBean 回调接口
2、 针对特殊行为的其他 Aware 接口
3、 Bean 配置文件中的 Custom init()方法和 destroy()方法
4、 @PostConstruct 和@PreDestroy 注解方式

##### Spring 提供几种配置方式来设置元数据 ？

1.基于 XML 的配置 2.基于注解的配置	 3.基于 Java 的配置  

##### BeanFactory 和 ApplicationContext 有什么区别？  

BeanFactory 可以理解为含有 bean 集合的工厂类。 BeanFactory 包含了种 bean 的定义，协作类之间的关系， bean 生命周期的控制。
application context扩展了bean factory的功能。从表面上看， application context一样具有bean定义、bean关联关系的设置，根据请求分发 bean 的功能。 但 application context 在此基础上还提供了其他的功能。
1.提供了支持国际化的文本消息
2.统一的资源文件读取方式（实现了ResourceLoader）
3.已在监听器中注册的 bean 的事件

##### Spring 框架能带来哪些好处？  

1、 Spring DI机制降低了业务对象替换的复杂性。
2、 先进的AOP和IOC思想，降低了类之间的耦合，使开发人员可以将更多的精力集中于业务的开发
3、 Spring 对主流的框架提供了很好的集成支持、 logging 框架、 J2EE、 Quartz和 JDK Timer， 以及其他视图技术。可以很方便的集成。
4、 Spring的整个生态环境比较的充实，各种场景下各种功能都有支持

Spring不支持分布式、以前配置文件比较繁琐，现在结合基于注解的配置方式

##### IOC 容器初始化的基本步骤

1、初始化的入口在容器实现中的 refresh()调用来完成。
2、对 bean 定义载入 IOC 容器使用的方法是 loadBeanDefinition
其中的大致过程如下： 
通过 ResourceLoader 来完成资源文件位置的定位，DefaultResourceLoader是默认的实现，同时上下文本身就给出了 ResourceLoader 的实现，可以从类路径，文件系统,URL 等方式来定为资源位置。 如果是 XmlBeanFactory 作为 IOC 容器， 那么需要为它指定 bean 定义的资源，也 就 是 说 bean 定 义 文 件 时 通 过 抽 象 成 Resource 来 被 IOC 容 器 处 理 的 。 
容 器 通 过BeanDefinitionReader 来 完 成 定 义 信 息 的 解 析 和 Bean 信 息 的 注 册 , 往 往 使 用 的 XmlBeanDefinitionReader 来 解 析 bean 的 xml 定 义 文 件 - 实 际 的 处 理 过 程 是 委 托 给BeanDefinitionParserDelegate 来完成的， 从而得到 bean 的定义信息， 这些信息在 Spring 中使用BeanDefinition 对 象 来 表 示 - 这 个 名 字 可 以 让 我 们 想 到loadBeanDefinition,RegisterBeanDefinition 这些相关方法-他们都是为处理 BeanDefinitin 服务 的。 
容 器 解 析 得 到 BeanDefinition 以 后 ， 需 要 把 它 在 IOC 容 器 中 注 册 ， 这 由 IOC 实 现BeanDefinitionRegistry 接口来实现。 注册过程就是在 IOC 容器内部维护的一个 HashMap 来保存得到的 BeanDefinition 的过程。 这个 HashMap 是 IOC 容器持有 Bean 信息的场所， 以后对 Bean 的操作都是围绕这个 HashMap 来实现的。

##### bean 依赖注入的时机

当 Spring IOC 容器完成了 Bean 定义资源的定位、 载入和解析注册以后， IOC 容器中已经管理了 Bean定义的相关数据， 但是此时 IOC 容器还没有对所管理的 Bean 进行依赖注入， 依赖注入在以下两种情况发生： 
1、用户第一次通过 getBean 方法向 IOC 容索要 Bean 时， IOC 容器触发依赖注入
2、当用户在 Bean 定义资源中为<bean>元素配置了 lazy-init为false（默认为false） 属性，即让容器在解析注册 Bean 定义时进行预实例化， 触发依赖注入 

##### SpringMVC初始化和请求处理原理

1、在容器初始化时会建立所有 url 和 Controller 的对应关系（HandlerMapping）,保存到 Map<url,Controller>中.Tomcat 启动时会通知 Spring 初始化容器(加载 Bean 的定义信息和初始化所有单例 Bean),然后SpringMVC 会遍历容器中的 Bean,获取每一个 Controller 中的所有方法访问的 url,然后将 url 和Controller 保存到一个 Map 中;

2、请求到达DispatchServlet后，会调用service方法-> doDispatch方法，会根据 Request 快速定位到 Controller,因为最终处理 Request 的是Controller 中的方法,Map 中只保留了 url 和 Controller 中的对应关系,所以要根据 Request 的 url 进一步确认Controller 中 的 Method, 这 一 步工作的原理就是拼接 Controller 的 url(Controller 上@RequestMapping 的值)和方法的 url(Method 上@RequestMapping 的值),与 request 的 url 进行匹配,找到匹配的那个方法;

3、确定处理请求的 Method后,接下来的任务就是参数绑定（HandlerAdapter）,把 Request中参数绑定到方法的形式参数上,执行方法处理请求,之后返回一个ModeAndView对象

4、ModeAndView对象最终会交给一个ViewResolver类解析，得到View（xml、json、html等），然后返回给前端

web.xml中定义有ContextLoaderListener监听器，该监听器在会容器启动的时候调用初始化webApplicationContext的方法，而DispatchServlet类的父类（FrameworkServlet）实现了ApplicationContextAware，会在webApplicationContext初始化完成后，将webApplicationContext注入到servlet容器中。

DispatchServlet初始化最终都会在FrameworkServlet的onRefresh方法，其调用位置有两个地方
1、HttpServletBean的init()，最终实现在FrameworkServlet的initServletBean()方法
2、FrameworkServlet的内部类ContextRefreshListener的onApplicationEvent方法

