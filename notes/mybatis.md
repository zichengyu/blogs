- like的写法

```
<if test="customerPhoneNumber != null">
    <bind name="likePhoneNumber" value="'%' + customerPhoneNumber + '%'"/>
    AND `customer_phone_number` LIKE #{likePhoneNumber}
</if>
```

- mybatis缓存

```
一级缓存和二级缓存都是在commit操作之后，才会写入缓存。没有commit的操作不会进入缓存中
请求先查询二级缓存，再查询一级缓存
一级缓存：
    打开：默认打开
    关闭：
    存放位置：BaseExector执行器中()
    作用域：SqlSession
    作用条件：同一个session，多次相同的查询
    失效条件：数据修改操作(增删改操作)，原因是mappe.xml中select标签的flushCache的属性默认是false，而update/delete/insert标签的flushCache属性默认是true
    缺陷：如果其他sqlSession更新了一级缓存缓存的值，一级缓存并不能感知，会读取到旧的数据库(脏数据)。二级缓存解决了此缺陷
二级缓存：
    打开：mybatis的全局config配置文件中 cacheEnabled(默认值为true)为true；同时在需要开启二级缓存的mapper.xml文件中写一个 <cache/> 标签(<cache/>; 另外select标签的useCache属性设置为true(默认为true) 标签中可以指定缓存的类型、大小、淘汰算法等等)
    关闭：mybatis的config配置文件中 cacheEnabled为false
    存放位置：一级缓存的装饰器中(CacheingExector)，他会对BaseExector进行包装
    作用域：nameSpace
    淘汰算法：LRU、FIFO、WEAK(JVM弱引用)、SOFT(JVM软引用)
    作用条件：一个mapper文件中相同方法的调用，共享二级缓存，不管他们是不是一个sqlSession
    失效条件：update/delete/insert
    使用：推荐在已查询为主的应用中，如果增删改比较多，会频繁清空二级缓存，那样缓存就失去了意义
```
- 执行器

```
顶层是BaseExector

BatchExctor: 同ReuseExector，不过缓存的是prepareStatement
ReuseExector：拿到缓存的Statement，用完放回，可重用
SimpleExector：基本功能，每次拿到Statement，用完即关
```

- 事务配置

```
transactionManager的type
JDBC：使用jdbc的事务
MANAGER：托管给容器控制，比如spring容器
```

- 为什么引入一个mapper对象

```
解决statementId(xml中的每一个增删改查对应的ID)硬编码问题
MapperProxy的动态代理实现，但是没有实现类，原因是只需要根据接口找到xml中配置的SQL，所以只需要知道方法名就能根据方法名到nameSpace中找到对应的SQL，并不需要实现类
```

