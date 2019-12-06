- 远程配置管理
```
ConfigurableEnvironment 核心配置类对象，管理profile、PropertySource、配置类型转换
CompositePropertySource 组合模式,包装PropertySource,存放所有的配置信息
PropertySource 每一个配置属性都是一个PropertySource，包含name和source
PropertySourceLocator 定位配置需要实现的类 -> PropertySource<?> locate(Environment environment);
ConversionService 配置参数类型的转换
```
- @EnableConfigurationProperties

```
如果一个配置类只配置@ConfigurationProperties注解，而没有使用@Component，那么在IOC容器中是获取不到properties 配置文件转化的bean。说白了 @EnableConfigurationProperties 相当于把使用 @ConfigurationProperties 的类进行了一次注入
```
