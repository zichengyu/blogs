##### 缓存

```
一级缓存：
    1、sqlSession级别，默认开启
    2、缓存在 Executor(SimpleExecutor/ReuseExecutor/BatchExecutor)里面维护
    3、一级缓存在 BaseExecutor 的 query()——queryFromDatabase()中存入.在queryFromDatabase()之前会get()。
    4、同一个会话中update、delete会导致clearLocalCache()清一级缓存
    
    不足：其他会话更新了数据,导致读取到脏数据(一级缓存不能跨会话共享)

二级缓存：
    1、namespace级别,可以被多个SqlSession共享(只要是同一个接口里面的相同方法,都可以共享)
    2、生命周期和应用同步
    3、作用范围在sqlSession之外,只有取不到二级缓存的情况下才到一个会话中去取一级缓存
    4、如果启用了二级缓存,MyBatis在创建Executor对象的时候会对 Executor 进行装饰。生成CachingExecutor
    5、增删改依旧会刷新掉缓存(增删改操作的xml中flushCache 属性默认为 true)
    6、二级缓存使用TransactionalCacheManager(TCM)来管理,事务不提交,缓存不生效
    
CachingExecutor对于查询请求，会判断二级缓存是否有缓存结果，如果有就直接返回，如果没有委派交给真正的查询器Executor实现类，比如 SimpleExecutor来执行查询，再走到一级缓存的流程。最后会把结果缓存起来，并且返回给用户。
```

##### 执行器Executor

```
继承了抽象类 BaseExecutor

SIMPLE:默认执行器；每执行一次update或select，就开启一个Statement 对象，用 完立刻关闭 Statement 对象。
BATCH:执行 update或select，以sql作为key查找Statement对象存在就使用，不存在就创建，用完后，不关闭Statement对象，而是放置于 Map 内， 供下一次使用。简言之，就是重复使用 Statement 对象。
REUSE：执行update(没有select,JDBC批处理不支持select)将所有sql都添加到批处理中(addBatch()),等待统一执行(executeBatch()),它缓存了多个Statement对象，每个Statement对象都是addBatch()完毕后,等待逐一执行executeBatch()批处理.与JDBC批处理相同。
```

##### mybatis动态代理和jdk动态代理

```
JDK 动态代理代理，在实现了InvocationHandler的代理类里面，需要传入一个被 代理对象的实现类。

不需要实现类的原因：我们只需要根据接口类型+方法的名称，就可以找到 StatementID了，而唯一要做的一件事情也是这件，所以不需要实现类。在MapperProxy里面直接执行逻辑(也就是执行SQL)就可以。
```
