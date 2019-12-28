##### 配置扩展

```java
public abstract class WebMvcConfigurerAdapter implements WebMvcConfigurer

支持：Interceptor、Formatter、ResourceHandler、ViewController、ViewResolver、ArgumentResolver、MessageConverter等等
```

##### Spring事件机制

![image-20181221175634020](https://ws3.sinaimg.cn/large/006tNbRwgy1fyeip8t8ebj31fn0g9zln.jpg)

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