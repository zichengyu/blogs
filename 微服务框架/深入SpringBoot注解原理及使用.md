## SpringBoot的主配置类

```java
@SpringBootApplication
public class StartEurekaApplication
{
    public static void main(String[] args)
    {
        SpringApplication.run(StartEurekaApplication.class, args);
    }
}
```

点进@SpringBootApplication来看，发现@SpringBootApplication是一个组合注解。

```java
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@SpringBootConfiguration
@EnableAutoConfiguration
@ComponentScan(excludeFilters = {
      @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class),
      @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })
public @interface SpringBootApplication {
}
```

## @SpringBootConfiguration

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Configuration
public @interface SpringBootConfiguration {
}
```

可以看到这个注解除了元注解以外，就只有一个@Configuration，那也就是说这个注解相当于@Configuration，所以这两个注解作用是一样的，它让我们能够去注册一些额外的Bean，并且导入一些额外的配置。那@Configuration还有一个作用就是把该类变成一个配置类，不需要额外的XML进行配置。所以@SpringBootConfiguration就相当于@Configuration。进入@Configuration，发现@Configuration核心是@Component，说明Spring的配置类也是Spring的一个组件。

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Component
public @interface Configuration {
    @AliasFor(
        annotation = Component.class
    )
    String value() default "";
}
```

## @EnableAutoConfiguration

EnableAutoConfiguration这个注解是开启自动配置的功能。

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@AutoConfigurationPackage
@Import({AutoConfigurationImportSelector.class})
public @interface EnableAutoConfiguration {
    String ENABLED_OVERRIDE_PROPERTY = "spring.boot.enableautoconfiguration";

    Class<?>[] exclude() default {};

    String[] excludeName() default {};
}
```

可以看到它是由 `@AutoConfigurationPackage，@Import(EnableAutoConfigurationImportSelector.class)`这两个而组成的，我们先说`@AutoConfigurationPackage`；`@AutoConfigurationPackage`的功能是让包中的类以及子包中的类能够被自动扫描到spring容器中。

```java
@Target({ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
@Inherited
@Import({Registrar.class})
public @interface AutoConfigurationPackage {
}
```

使用`@Import`来给Spring容器中导入一个组件 ，这里导入的是`Registrar.class`。来看下这个Registrar：

```java
static class Registrar implements ImportBeanDefinitionRegistrar, DeterminableImports {
        Registrar() {
        }

        public void registerBeanDefinitions(AnnotationMetadata metadata, BeanDefinitionRegistry registry) {
            AutoConfigurationPackages.register(registry, (new AutoConfigurationPackages.PackageImport(metadata)).getPackageName());
        }

        public Set<Object> determineImports(AnnotationMetadata metadata) {
            return Collections.singleton(new AutoConfigurationPackages.PackageImport(metadata));
        }
    }
```

就是通过以上这个方法获取扫描的包路径，可以debug查看具体的值：

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwpicWQCVUxqjDicccR4rbvib9gMsSS0JyLwiazGsRyX7PMvCH30dUNjKNpQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

那metadata是什么呢，可以看到是标注在`@SpringBootApplication`注解上的DemosbApplication，也就是我们的主配置类Application：

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwicpicYltfaCiaOL2HHyzkrbMzNBxeRZ3YyVrFz27JvcaURskqCicBxibRRw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

其实就是将主配置类（即`@SpringBootApplication`标注的类）的**所在包及子包里面所有组件扫描加载到Spring容器**。因此我们要把DemoApplication放在项目的最高级中（最外层目录）。

看看注解`@Import(AutoConfigurationImportSelector.class)`，`@Import`注解就是给Spring容器中导入一些组件，这里传入了一个组件的选择器:`AutoConfigurationImportSelector`。

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwxCnZJ0AvNJtfbL2kY3vXZCgayT19CDXwZniaFCR6ZUGjkxj01Fob4ug/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

可以从图中看出`AutoConfigurationImportSelector` 继承了 `DeferredImportSelector` 继承了 `ImportSelector`，`ImportSelector`有一个方法为：`selectImports`。将所有需要导入的组件以全类名的方式返回，这些组件就会被添加到容器中。

```java
public String[] selectImports(AnnotationMetadata annotationMetadata) {
    if (!this.isEnabled(annotationMetadata)) {
        return NO_IMPORTS;
    } else {
        AutoConfigurationMetadata autoConfigurationMetadata = AutoConfigurationMetadataLoader.loadMetadata(this.beanClassLoader);
        AutoConfigurationImportSelector.AutoConfigurationEntry autoConfigurationEntry = 
　　　　　　　　this.getAutoConfigurationEntry(autoConfigurationMetadata, annotationMetadata);
        return StringUtils.toStringArray(autoConfigurationEntry.getConfigurations());
    }
}
```

会给容器中导入非常多的自动配置类（`xxxAutoConfiguration`）；就是给容器中导入这个场景需要的所有组件，并配置好这些组件。

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwxxfWgRWHBgzRhnVW3bcn4j2m18RfYDsajDhj0iblicCuqqNVM11nJ9lQ/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

有了自动配置类，免去了我们手动编写配置注入功能组件等的工作。那是如何获取到这些配置类的呢，看看下面这个方法：

```java
protected AutoConfigurationImportSelector.AutoConfigurationEntry 
　　getAutoConfigurationEntry(AutoConfigurationMetadata autoConfigurationMetadata, AnnotationMetadata annotationMetadata) {
    if (!this.isEnabled(annotationMetadata)) {
        return EMPTY_ENTRY;
    } else {
        AnnotationAttributes attributes = this.getAttributes(annotationMetadata);
        List<String> configurations = this.getCandidateConfigurations(annotationMetadata, attributes);
        configurations = this.removeDuplicates(configurations);
        Set<String> exclusions = this.getExclusions(annotationMetadata, attributes);
        this.checkExcludedClasses(configurations, exclusions);
        configurations.removeAll(exclusions);
        configurations = this.filter(configurations, autoConfigurationMetadata);
        this.fireAutoConfigurationImportEvents(configurations, exclusions);
        return new AutoConfigurationImportSelector.AutoConfigurationEntry(configurations, exclusions);
    }
}
```

我们可以看到getCandidateConfigurations()这个方法，他的作用就是引入系统已经加载好的一些类，到底是那些类呢：

```java
protected List<String> getCandidateConfigurations(AnnotationMetadata metadata, AnnotationAttributes attributes) {
    List<String> configurations = SpringFactoriesLoader.loadFactoryNames(this.getSpringFactoriesLoaderFactoryClass(), this.getBeanClassLoader());
    Assert.notEmpty(configurations, 
　　　　"No auto configuration classes found in META-INF/spring.factories. If you are using a custom packaging, make sure that file is correct.");
    return configurations;
}

public static List<String> loadFactoryNames(Class<?> factoryClass, @Nullable ClassLoader classLoader) {
    String factoryClassName = factoryClass.getName();
    return (List)loadSpringFactories(classLoader).getOrDefault(factoryClassName, Collections.emptyList());
}
```

会从META-INF/spring.factories中获取资源，然后通过Properties加载资源：

```java
private static Map<String, List<String>> loadSpringFactories(@Nullable ClassLoader classLoader) {
    MultiValueMap<String, String> result = (MultiValueMap)cache.get(classLoader);
    if (result != null) {
        return result;
    } else {
        try {
            Enumeration<URL> urls = classLoader != 
　　　　　　　　　　null ? classLoader.getResources("META-INF/spring.factories") : ClassLoader.getSystemResources("META-INF/spring.factories");
            LinkedMultiValueMap result = new LinkedMultiValueMap();

            while(urls.hasMoreElements()) {
                URL url = (URL)urls.nextElement();
                UrlResource resource = new UrlResource(url);
                Properties properties = PropertiesLoaderUtils.loadProperties(resource);
                Iterator var6 = properties.entrySet().iterator();

                while(var6.hasNext()) {
                    Map.Entry<?, ?> entry = (Map.Entry)var6.next();
                    String factoryClassName = ((String)entry.getKey()).trim();
                    String[] var9 = StringUtils.commaDelimitedListToStringArray((String)entry.getValue());
                    int var10 = var9.length;

                    for(int var11 = 0; var11 < var10; ++var11) {
                        String factoryName = var9[var11];
                        result.add(factoryClassName, factoryName.trim());
                    }
                }
            }

            cache.put(classLoader, result);
            return result;
        } catch (IOException var13) {
            throw new IllegalArgumentException("Unable to load factories from location [META-INF/spring.factories]", var13);
        }
    }
}
```

可以知道SpringBoot在启动的时候从类路径下的`META-INF/spring.factories`中获取`EnableAutoConfiguration`指定的值，将这些值作为自动配置类导入到容器中，自动配置类就生效，帮我们进行自动配置工作。以前我们需要自己配置的东西，自动配置类都帮我们完成了。如下图可以发现Spring常见的一些类已经自动导入。

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwVhvUibqMqVBSF1eUOT5F5MrWBl2ezBAX3KWvr4htuB9ZbnEByqiauxag/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

接下来看`@ComponentScan`注解，`@ComponentScan(excludeFilters = { @Filter(type = FilterType.CUSTOM, classes = TypeExcludeFilter.class), @Filter(type = FilterType.CUSTOM, classes = AutoConfigurationExcludeFilter.class) })`，这个注解就是扫描包，然后放入spring容器。

```java
@ComponentScan(excludeFilters = {
　　@Filter(type = FilterType.CUSTOM,classes = {TypeExcludeFilter.class}), 
　　@Filter(type = FilterType.CUSTOM,classes = {AutoConfigurationExcludeFilter.class})})
public @interface SpringBootApplication {}
```

总结下`@SpringbootApplication`：就是说，他已经把很多东西准备好，具体是否使用取决于我们的程序或者说配置。

## run方法

```java
public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
}
```

来看下在执行run方法到底有没有用到哪些自动配置的东西，我们点进run：

```java
public ConfigurableApplicationContext run(String... args) {
    //计时器
    StopWatch stopWatch = new StopWatch();
    stopWatch.start();
    ConfigurableApplicationContext context = null;
    Collection<SpringBootExceptionReporter> exceptionReporters = new ArrayList();
    this.configureHeadlessProperty();
    //监听器
    SpringApplicationRunListeners listeners = this.getRunListeners(args);
    listeners.starting();

    Collection exceptionReporters;
    try {
        ApplicationArguments applicationArguments = new DefaultApplicationArguments(args);
        ConfigurableEnvironment environment = this.prepareEnvironment(listeners, applicationArguments);
        this.configureIgnoreBeanInfo(environment);
        Banner printedBanner = this.printBanner(environment);
        //准备上下文
        context = this.createApplicationContext();
        exceptionReporters = this.getSpringFactoriesInstances(SpringBootExceptionReporter.class, 
　　　　　　　　　　　　　　　　　　　　　　new Class[]{ConfigurableApplicationContext.class}, context);
        //预刷新context
        this.prepareContext(context, environment, listeners, applicationArguments, printedBanner);
        //刷新context
        this.refreshContext(context);
        //刷新之后的context
        this.afterRefresh(context, applicationArguments);
        stopWatch.stop();
        if (this.logStartupInfo) {
            (new StartupInfoLogger(this.mainApplicationClass)).logStarted(this.getApplicationLog(), stopWatch);
        }

        listeners.started(context);
        this.callRunners(context, applicationArguments);
    } catch (Throwable var10) {
        this.handleRunFailure(context, var10, exceptionReporters, listeners);
        throw new IllegalStateException(var10);
    }

    try {
        listeners.running(context);
        return context;
    } catch (Throwable var9) {
        this.handleRunFailure(context, var9, exceptionReporters, (SpringApplicationRunListeners)null);
        throw new IllegalStateException(var9);
    }
}
```

那我们关注的就是 refreshContext(context); 刷新context，我们点进来看。

```java
private void refreshContext(ConfigurableApplicationContext context) {
   refresh(context);
   if (this.registerShutdownHook) {
      try {
         context.registerShutdownHook();
      }
      catch (AccessControlException ex) {
         // Not allowed in some environments.
      }
   }
}
```

我们继续点进refresh(context);

```java
protected void refresh(ApplicationContext applicationContext) {
   Assert.isInstanceOf(AbstractApplicationContext.class, applicationContext);
   ((AbstractApplicationContext) applicationContext).refresh();
}
```

他会调用 `((AbstractApplicationContext) applicationContext).refresh();`方法，我们点进来看：

```java
public void refresh() throws BeansException, IllegalStateException {
   synchronized (this.startupShutdownMonitor) {
      // Prepare this context for refreshing.
      prepareRefresh();
      // Tell the subclass to refresh the internal bean factory.
      ConfigurableListableBeanFactory beanFactory = obtainFreshBeanFactory();
      // Prepare the bean factory for use in this context.
      prepareBeanFactory(beanFactory);

      try {
         // Allows post-processing of the bean factory in context subclasses.
         postProcessBeanFactory(beanFactory);
         // Invoke factory processors registered as beans in the context.
         invokeBeanFactoryPostProcessors(beanFactory);
         // Register bean processors that intercept bean creation.
         registerBeanPostProcessors(beanFactory);
         // Initialize message source for this context.
         initMessageSource();
         // Initialize event multicaster for this context.
         initApplicationEventMulticaster();
         // Initialize other special beans in specific context subclasses.
         onRefresh();
         // Check for listener beans and register them.
         registerListeners();
         // Instantiate all remaining (non-lazy-init) singletons.
         finishBeanFactoryInitialization(beanFactory);
         // Last step: publish corresponding event.
         finishRefresh();
      }catch (BeansException ex) {
         if (logger.isWarnEnabled()) {
            logger.warn("Exception encountered during context initialization - " +
                  "cancelling refresh attempt: " + ex);
         }
         // Destroy already created singletons to avoid dangling resources.
         destroyBeans();
         // Reset 'active' flag.
         cancelRefresh(ex);
         // Propagate exception to caller.
         throw ex;
      }finally {
         // Reset common introspection caches in Spring's core, since we
         // might not ever need metadata for singleton beans anymore...
         resetCommonCaches();
      }
   }
}
```

由此可知，就是一个spring的bean的加载过程。继续来看一个方法叫做 onRefresh()：

```java
protected void onRefresh() throws BeansException {
   // For subclasses: do nothing by default.
}
```

他在这里并没有直接实现，但是我们找他的具体实现：

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwy0FTpkYmV9v19qeeoXyWu64NkrAD0EIiaw63M02H3H0WZu8DNufGA1A/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

比如Tomcat跟web有关，我们可以看到有个`ServletWebServerApplicationContext`：

```java
@Override
protected void onRefresh() {
   super.onRefresh();
   try {
      createWebServer();
   }
   catch (Throwable ex) {
      throw new ApplicationContextException("Unable to start web server", ex);
   }
}
```

可以看到有一个createWebServer();方法他是创建web容器的，而Tomcat不就是web容器，那是如何创建的呢，我们继续看：

```java
private void createWebServer() {
   WebServer webServer = this.webServer;
   ServletContext servletContext = getServletContext();
   if (webServer == null && servletContext == null) {
      ServletWebServerFactory factory = getWebServerFactory();
      this.webServer = factory.getWebServer(getSelfInitializer());
   }
   else if (servletContext != null) {
      try {
         getSelfInitializer().onStartup(servletContext);
      }
      catch (ServletException ex) {
         throw new ApplicationContextException("Cannot initialize servlet context",
               ex);
      }
   }
   initPropertySources();
}
```

`factory.getWebServer(getSelfInitializer());`他是通过工厂的方式创建的。

```java
public interface ServletWebServerFactory {
   WebServer getWebServer(ServletContextInitializer... initializers);
}
```

可以看到 它是一个接口，为什么会是接口。因为我们不止是Tomcat一种web容器。

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYw9dGsuHjw3MJFrMj1GDibjHO14OBaHNk727N9u5Lk03Hplo7IKTWGwzA/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

我们看到还有Jetty，那我们来看TomcatServletWebServerFactory：

```java
@Override
public WebServer getWebServer(ServletContextInitializer... initializers) {
   Tomcat tomcat = new Tomcat();
   File baseDir = (this.baseDirectory != null) ? this.baseDirectory
         : createTempDir("tomcat");
   tomcat.setBaseDir(baseDir.getAbsolutePath());
   Connector connector = new Connector(this.protocol);
   tomcat.getService().addConnector(connector);
   customizeConnector(connector);
   tomcat.setConnector(connector);
   tomcat.getHost().setAutoDeploy(false);
   configureEngine(tomcat.getEngine());
   for (Connector additionalConnector : this.additionalTomcatConnectors) {
      tomcat.getService().addConnector(additionalConnector);
   }
   prepareContext(tomcat.getHost(), initializers);
   return getTomcatWebServer(tomcat);
}
```

那这块代码，就是我们要寻找的内置Tomcat，在这个过程当中，我们可以看到创建Tomcat的一个流程。

## 扩展：自定义stater

首先自定义一个stater。

```
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>2.1.4.RELEASE</version>
    <relativePath/>
</parent>
<groupId>com.zgw</groupId>
<artifactId>gw-spring-boot-starter</artifactId>
<version>1.0-SNAPSHOT</version>

<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-autoconfigure</artifactId>
    </dependency>
</dependencies>
```

我们先来看maven配置写入版本号，如果自定义一个stater的话必须依赖`spring-boot-autoconfigure`这个包,我们先看下项目目录。

![img](https://mmbiz.qpic.cn/mmbiz_png/tO7NEN7wjr6mjiabpOh7lA3gU57QdIVYwHOIdxYv6wFzo8NuAibLuAz394ibnbd7xqHt93XTlMrvNcULkxbwt3LKw/640?wx_fmt=png&wxfrom=5&wx_lazy=1&wx_co=1)

```java
public class GwServiceImpl  implements GwService{
    @Autowired
    GwProperties properties;

    @Override
    public void Hello()
    {
        String name=properties.getName();
        System.out.println(name+"说:你们好啊");
    }
}
```

我们做的就是通过配置文件来定制name这个是具体实现。

```java
@Component
@ConfigurationProperties(prefix = "spring.gwname")
public class GwProperties {

    String name="zgw";

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}
```

这个类可以通过`@ConfigurationProperties`读取配置文件。

```java
@Configuration
@ConditionalOnClass(GwService.class)  //扫描类
@EnableConfigurationProperties(GwProperties.class) //让配置类生效
public class GwAutoConfiguration {

    /**
    * 功能描述 托管给spring
    * @author zgw
    * @return
    */
    @Bean
    @ConditionalOnMissingBean
    public GwService gwService()
    {
        return new GwServiceImpl();
    }
}
```

这个为配置类，为什么这么写因为，spring-boot的stater都是这么写的，我们可以参照他仿写stater，以达到自动配置的目的，然后我们在通过spring.factories也来进行配置。

```java
org.springframework.boot.autoconfigure.EnableAutoConfiguration=com.gw.GwAutoConfiguration
```

然后这样一个简单的stater就完成了，然后可以进行maven的打包，在其他项目引入就可以使用。