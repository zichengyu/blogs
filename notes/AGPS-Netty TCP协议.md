1、TCP粘包和拆包

- 熟悉TCP编程的可能都知道，无论是服务端还是客户端，当我们读取或者是发送消息的时候，都需要考虑TCP底层的粘包和拆包机制。
- TCP是个“流”协议，所谓流，就是没有界限的一串数据。大家可以想想河里的流水，它们是连成一片的，其间并没有分界线。再加上网络上MTU的往往小于在应用处理的消息数据，所以就会引发一次接收的数据无法满足消息的需要，导致粘包的存在。TCP底层并不了解上层业务数据的具体含义，它会根据TCP缓冲区的实现情况进行包的拆分，所以在业务上认为，一个完整的包可能会被TCP拆成多个包进行发送，也有可能把多个小的包封装成一个大的数据包发送，这就是所谓的TCP粘包和拆包问题。
- 处理粘包的唯一方法就是制定应用层的数据通讯协议，通过协议来规范现有接收的数据是否满足消息数据的需要。

2、解决办法

    2.1、消息定长，报文大小固定长度，不够空格补全，发送和接收方遵循相同的约定，这样即使粘包了通过接收方编程实现获取定长报文也能区分。


    2.2、包尾添加特殊分隔符，例如每条报文结束都添加回车换行符（例如FTP协议）或者指定特殊字符作为报文分隔符，接收方通过特殊分隔符切分报文区分。


    2.3、将消息分为消息头和消息体，消息头中包含表示消息总长度（或者消息体长度）的字段，通常设计思路为消息头的第一个字段使用int来表示消息的总长度

3、Netty ByteBuf


&emsp;&emsp;当我们进行数据传输的时候，往往需要使用到缓冲区，常用的缓冲区就是JDK NIO类库提供的java.nio.Buffer。从功能角度而言，ByteBuffer完全可以满足NIO编程的需要，但是NIO编程过于复杂，也存在局限性。ByteBuffer长度固定，一旦分配完成，不可动态修改。

&emsp;&emsp;JDK ByteBuffer由于只有一个位置指针用于处理读写操作，因此每次读写的时候都需要额外调用flip()，否则功能将出错。

&emsp;&emsp;Netty ByteBuf提供了两个指针用于支持顺序读取和写入操作：readerIndex用于标识读取索引，writerIndex用于标识写入索引。两个位置指针将ByteBuf缓冲区分割成三个区域。 
  （1） readerIndex到writerIndex之间的空间为可读的字节缓冲区  
  （2） writerIndex到capacity之间为可写的字节缓冲区  
  （3） 0到readerIndex之间是已经读取过的缓冲区


最近在做一个项目，遇到了自定义协议的粘包和拆包的问题。服务端使用Netty与客户端进行交互，协议为客户端自定义的协议，协议大致如下。

整个数据包的结构
2*byte的消息头+数据长度+数据体

magic   |   magic   |   length   |   [data]
1
magic(byte): 0x46 
length(int): data的长度 
data(byte[]): data数组

data数组的结构
 key | length | data | key | length | data | key | length | data | key | length | data   
1
key: 键名 
length: data的长度 
data: 值

下面为自定义协议粘包和拆包处理的大致实现，用到了Netty ByteBuf的几个方法。 
isReadable: 缓冲区是否可读 
markReaderIndex: 记录当前缓冲区读指针的位置 
resetReaderIndex: 重置缓冲区至markReaderIndex的位置处（markReaderIndex的初始位置为0） 
readerIndex: 当前缓冲区读指针的位置 
readableBytes: 当前缓冲区可读的字节数 
read*: 读取数据

备注: 当一开始使用resetReaderIndex重置缓冲区读指针的位置时候，读指针会被重置0； 
当使用markReaderIndex记录过当前缓冲区读指针的位置时，再使用resetReaderIndex重置缓冲区读指针的位置，读指针会被重置到markReaderIndex记录的位置处。   
[link](http://blog.csdn.net/yu757371316/article/details/78955412)