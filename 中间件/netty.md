netty线程模型

```
Netty通过Reactor模型基于多路复用器接收并处理用户请求，内部实现了两个线程池，boss线程池和work线程池
boss线程池：负责处理请求的accept事件，当接收到accept事件的请求时，把对应的socket封装到一个NioSocketChannel中，并交给work线程池
work线程池：负责请求的read和write事件，由对应的Handler处理。
```

##### Netty 的“零拷贝”

```
1、Netty的接收和发送ByteBuffer采用DIRECT BUFFERS，使用堆外直接内存进行Socket读写，不需要进行字节缓冲区的二次拷贝。如果使用传统的堆内存（HEAP BUFFERS）进行Socket读写，JVM会将堆内存Buffer拷贝一份到直接 内存中，然后才写入Socket中。相比于堆外直接内存，消息在发送过程中多了一次缓冲区的内存拷贝。
2、Netty 提供了组合 Buffer 对象，可以聚合多个 ByteBuffer 对象，用户可以像操作一个 Buffer 那样方便的对组合 Buffer 进行操作，避免了传统通过内存拷贝的方式将几个小 Buffer 合并成一个大的 Buffer。
3、Netty 的文件传输采用了transferTo()方法，它可以直接将文件缓冲区的数据发送到目标Channel，避免了传统通过循环write()方式导致的内存拷贝问题。
```

##### 内存池

```
Netty提供了基于内存池的缓冲区重用机制，循环使用ByteBuf对象，如果是非内存池实现，则直接创建一个新的 ByteBuf 对象

```
##### 高效的 Reactor 线程模型(同步非阻塞)
```
Reactor 单线程模型：所有的IO操作都在同一个NIO线程上面完成，包括处理连接、请求、应答
Reactor 多线程模型：
    1、一个NIO线程-Acceptor线程用于监听服务端，接收客户端的 TCP 连接请求
    2、网络 IO 操作-读、写等由一个NIO线程池负责，它包含一个任务队列和N个可用的线程
    3、1 个 NIO 线程可以同时处理 N 条链路，但是 1 个链路只对应 1 个 NIO 线程，防止发生并发操作问题
主从 Reactor 多线程模型：
    1、一个独立的 NIO 线程池处理握手、链接、认证等
    2、后端 subReactor 线程池负责后续的 IO 操作
```

##### 无锁化的串行设计

```
Netty 采用了串行无锁化设计，在IO线程内部进行串行操作，避免多线程竞争导致的性能下降。表面上看，串行化设计似乎CPU利用率不高，并发程度不够。但是，通过调整NIO线程池的线程参数，可以同时启动多个串行化的线程并行运行，这种局部无锁化的串行线程设计相比一个队列-多个工作线程模型性能更优。
这种串行化处理方式避免了多线程操作导致的锁的竞争，从性能角度看是最优的。
```
##### 高性能的序列化
```
Netty默认提供了对Google Protobuf的支持，通过扩展Netty的编解码接口，用户可以实现其它的高性能序列化框架
```

##### ByteBuf 的基本结构

```
readerIndex(记录读指针的开始位置)
writerIndex(记录写指针的开始位置)
capacity(缓冲区的总长度)
maxCapacity，这就相当于是 ByteBuf 扩容的最大阈值
从 0 到 readerIndex 为 discardable bytes 表示是无效的，从 readerIndex到writerIndex为readable bytes表示可读数据区，从 writerIndex到capacity为writable bytes表示这段区间空闲可以往里面写数据
```

##### ByteBuf 的基本分类

```
AbstractByteBuf之下有众多子类，大致可以从三个维度来进行分类，分别如下： 
Pooled：池化内存，就是从预先分配好的内存空间中提取一段连续内存封装成一个 ByteBuf 分给应用程序使用。 
Unsafe：是 JDK 底层的一个负责IO操作的对象，可以直接拿到对象的内存地址，基于内存地址进行读写操作。
Direct：堆外内存，是直接调用JDK的底层API进行物理内存分配，不在 JVM 的堆内存中，需要手动释放。
```
##### TCP 粘包和拆包

```
TCP 是一个“流”协议，所谓流，就是没有界限的一长串二进制数据。  
TCP 作为传输层协议并不不了解上层业务数据的具体含义，它会根据TCP缓冲区的实际情况进行数据包的划分，所以在业务上认为是一个完整的包，可能会被TCP拆分成多个包进行发送，也有可能把多个小的包封装成一个大的数据包发送
半包：一次读取到一个完整数据包的一部分(解析到半包)
沾包：一次读取到超过一个完整数据包的长度
```
##### 粘包问题的解决策略

```
底层是无法保证数据包不被拆分和重组的，只能通过上层的应用协议栈设计来解决
1、消息定长,报文大小固定长度,例如每个报文的长度固定为 200 字节,如果不够空位补空格
2、包尾添加特殊分隔符,例如每条报文结束都添加回车换行符(例如 FTP 协议)或者指定特殊字符作为报文分隔符,接收方通过特殊分隔符切分报文区分
3、将消息分为消息头和消息体,消息头中包含表示信息的总长度(或者消息体长度)的字段
4、更复杂的自定义应用层协议
netty处理：不是一个完整的数据包,则解析失败,将这块数据包进行保存,等下次解析时再和这个数据包进行组装解析,直到解析到完整的数据包, 才会将数据包向下传递。
```
##### pipeline结构

```
链式结构，首节点HeadContext，尾结点TailContext,中间就是一些列handler，读数据时从HeadContext到TailContext，写数据时从TailContext到HeadContext
```
##### netty总体设计

```
总体是责任链模式；
有一个顶层责任处理接口(ChannelHandler)；
有动态创建链、添加和删除责任处理器的接口(ChannelPipeline);有上下文机制(ChannelHandlerContext); 
有责任终止机制(不调用 ctx.fireXXX()方法,则终止传播)
```
##### Netty 定位

```
A、作为开源码框架的底层框架（TCP通信):SpringBoot内置的容器(Tomcat/Jerry)、Zookeper数据交互、Dubbo多协议RPC的支持
B、直接做服务器(消息推送服务、游戏后台)
```
##### Netty 中大文件上传的那个handler是怎么做到防止内存撑爆的
```
ByteBuf分片;直接缓冲区; 0拷贝,提高内存的利用率;加内存
```
##### Selector 客户端与服务端之间关系

```
客户端：CONNECT READ WRITE 
服务端：ACCEPT  READ WRITE
```

