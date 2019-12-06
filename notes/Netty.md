##### 多路复用

```
IO多路复用模型是建立在内核提供的多路分离函数select基础之上的，使用select函数可以避免同步非阻塞IO模型中客户端轮询等待的问题
```


##### netty的优点

```
1、封装繁琐的NIO操作，基于多路复用机制
2、接受和发送缓冲区使用直接堆外内存进行socket读写
3、提供了组合buffer，可以对多个bytebuffer进行聚合
4、transferTo直接将文件缓冲区的数据发起送到目标channel
```

##### Reactor多线程模型

```
单线程模型：一个线程既处理连接，又处理读写(Acceptor和Handler处理在同一个线程中)
多线程模型：一个reactor线程处理连接(Acceptor)，再有一个ReactorThreadPool处理读写(多个Handler)
主从线程模型：acceptor接收连接，将请求转发给MainReactorThreadPool, MainReactorThreadPool处理连接后(鉴权、登录、加解密等) ，将请求派发给SubReactorThreadPool进行数据读写
```

##### Netty基础

```
一个channel有且仅有一个pipeline
一个pipeline就是一个双向链表，顺序为：HandlerHead 自定义的一个或多个Handler HandlerTail
```


