##### 配置扩展

```java
public abstract class WebMvcConfigurerAdapter implements WebMvcConfigurer

支持：Interceptor、Formatter、ResourceHandler、ViewController、ViewResolver、ArgumentResolver、MessageConverter等等
```

##### Spring事件机制

![image-20181221175634020](https://github.com/yu757371316/blogs/blob/master/images/Spring%E4%BA%8B%E4%BB%B6%E6%9C%BA%E5%88%B6%E5%9B%BE.jpg)

##### SpringApplication继承机制

![Spring ApplicationContext继承结构图](https://ws3.sinaimg.cn/large/006tNbRwgy1fyejdraxr1j310009sdhx.jpg)

![image-20181221185625164](https://ws3.sinaimg.cn/large/006tNbRwgy1fyekf9eocjj31ct0ekq54.jpg)

##### Spring Boot 事件监听器

`ConfigFileApplicationListener` 监听 `ApplicationEnvironmentPreparedEvent` 事件从而加载 `application.properties` 或者 `application.yml` 文件

Spring Boot 很多组件依赖于 Spring Boot 事件监听器实现，本质是 Spring Framework 事件/监听机制

`SpringApplication` 利用

- Spring 应用上下文（`ApplicationContext）`生命周期控制 注解驱动 Bean 
- Spring 事件/监听（`ApplicationEventMulticaster`）机制加载或者初始化组件

```properties
org.springframework.context.ApplicationListener=\
org.springframework.boot.ClearCachesApplicationListener,\
org.springframework.boot.builder.ParentContextCloserApplicationListener,\
org.springframework.boot.context.FileEncodingApplicationListener,\
org.springframework.boot.context.config.AnsiOutputApplicationListener,\
org.springframework.boot.context.config.ConfigFileApplicationListener,\
org.springframework.boot.context.config.DelegatingApplicationListener,\
org.springframework.boot.context.logging.ClasspathLoggingApplicationListener,\
org.springframework.boot.context.logging.LoggingApplicationListener,\
org.springframework.boot.liquibase.LiquibaseServiceLocatorApplicationListener
```

##### Spring事件机制

Spring 事件的类型 `ApplicationEvent`         				相当于消息内容

Spring 事件监听器 `ApplicationListener`    				相当于消息消费者、订阅者

Spring 事件广播器 `ApplicationEventMulticaster`	相当于消息生产者、发布者

- 实现类：`SimpleApplicationEventMulticaster`  使用Java.util.concurrent.Executor

  ![image-20181222120130865](https://ws1.sinaimg.cn/large/006tNbRwgy1fyfe1ue49rj30ni09b75i.jpg)

##### @ServletComponentScan

SpringBootApplication 上使用@ServletComponentScan 注解后，Servlet、Filter、Listener 可以直接通过 @WebServlet、@WebFilter、@WebListener 注解自动注册，无需其他代码

##### 元注解

**@Target**：用于描述注解的使用范围. CONSTRUCTOR FIELD LOCAL_VARIABLE METHOD PACKAGE PARAMETER TYPE

**@Retention**：定义了该Annotation的生命周期. SOURCE CLASS RUNTIME

**@Documented**：标记注解，文档化

**@Inherited**：标记注解，被标注的类型是被继承的，@Inherited annotation类型是被标注过的class的子类所继承。类并不从它所实现的接口继承annotation，方法并不从它所重载的方法继承annotation。可以用反射增强

##### [EnableDiscoveryClient与EnableEurekaClient](https://blog.csdn.net/boling_cavalry/article/details/82668480)

- 在Spring Cloud的Dalston及其之前的版本中： 
  - 新版本官方就推荐使用EnableDiscoveryClient来取代EnableEurekaClient；
  - EnableEurekaClient源码中使用了注解EnableDiscoveryClient，因此如果要使用eureka的注册发现服务，两者功能是一样的；
  - EnableDiscoveryClient注解在spring.factories配置中通过配置项EurekaDiscoveryClientConfiguration来开启服务注册发现功能；
- 在Dalston之后的版本中（不含Dalston）： 
  - 在spring.factories配置中，配置类EurekaDiscoveryClientConfiguration被配置到springboot的自动配置注解中，与EnableDiscoveryClient注解没有关系了,也就是说只要开启了springboot的自动配置，服务注册发现功能就会启用； 
  - EnableEurekaClient源码中没有使用注解EnableDiscoveryClient，此时EnableEurekaClient已经没用了；
 
##### [SpringBoot的EnableAutoConfiguration](https://blog.csdn.net/yu757371316/article/details/106786665)

```
@import 注解就是把多个分开的容器配置合并在一个配置中
@Import 注解可以配置三种不同的 class
1. 第一种就是基于普通 bean 或者带有 @Configuration 的 bean 进行注入(导入其他配置类)
2. 实现 ImportSelector 接口进行动态注入(该接口 selectImports 方法返回的数组(类的全类名)都会被纳入到 spring 容器中)
3. 实现 ImportBeanDefinitionRegistrar 接口进行动态注入

本质上来说，其实 EnableAutoConfiguration 会帮助springboot 应用把所有符合@Configuration配置都加载到当前SpringBoot创建的IoC容器，而这里面借助了Spring框架提供的一个工具类SpringFactoriesLoader的支持。以及用到了Spring提供的条件注解 @Conditional，选择性的针对需要加载的bean进行条件过滤

EnableAutoConfiguration = @AutoConfigurationPackage() + @Import(EnableAutoConfigurationImportSelector.class)

```

##### AutoConfigurationImportSelector原理

```
最终实现ImportSelector，覆盖selectImports方法，通过SpringFactoriesLoader从classpath/META-INF/spring.factories 文件中，根据key来加载对应的类到spring IoC容器中。

在分析 AutoConfigurationImportSelector的源码时，会先扫描spring-autoconfiguration-metadata.properties(通过AutoConfigurationMetadataLoader)文件，最后再扫描spring.factories(通过SpringFactoriesLoader)对应的类时，会结合前面的元数据进行过滤，为什么要过滤呢? 原因是很多的@Configuration其实是依托于其他的框架来加载的，如果当前的 classpath环境下没有相关联的依赖，则意味着这些类没必要进行加载，所以，通过这种条件过滤可以有效的减少@configuration 类的数量从而降低 SpringBoot 的启动时间。
```

##### 条件注入Conditional

```
@ConditionalOnBean  在存在某个 bean 的时候
@ConditionalOnMissingBean   不存在某个 bean 的时候
@ConditionalOnClass 当前 classpath 可以找到某个类型的类时
@ConditionalOnMissingClass  当前classpath不可以找到某个类型的类时
@ConditionalOnResource  当前classpath是否存在某个资源文件
@ConditionalOnProperty 当前jvm是否包含某个系统属性为某个值
@ConditionalOnWebApplication    当前 spring context 是否是 web 应用程序
```

##### 处理函数参数的分解器

```
HandlerMethodArgumentResolver实际就是一个切面，它能对前端传过来的请求进行拦截，然后动态的对请求中的实参进行调整。
```
##### @Transactional坑

```
http://blog.timmattison.com/archives/2012/04/19/tips-for-debugging-springs-transactional-annotation/
@Transactional是经过cglib创建的代理对象，代理逻辑为我们管理事务开闭逻辑。代理对象在执行时还会找具体方法是否有@Transactional注解标注
jdk是代理接口，私有方法必然不会存在在接口里，所以就不会被拦截到； 
cglib是子类，private的方法照样不会出现在子类里，也不能被拦截。 
```

##### spring初始化三部曲
```
定位 加载 注册
```

##### 依赖注入发生的时间
```
用户第一次getBean方法时
bean设置为lazy-init=false时，则让容器在解析bean定义时就触发注入
```

##### spring事务原理

```
核心类：PlatformTransactionManager
原理：封装DataSource，对DataSource代理,DataSource包含了jdbc的Connection
步骤：加载驱动、关闭自动提交、创建Connection、创建Statement、执行Statement、获取结果、commit/rollback、关闭各种资源
```