##### protobuf压缩算法

```
varint和zigzag
```

##### protobuf 的T-L-V 存储方式

```
tag：字段标识符，用于标识字段
length：value的字节长度
value：消息字段经过编码后的值
```

##### 

```
Protocol Buffer 的性能好，主要体现在 序列化后的数据体积小 & 序列化速度快，最终使得传输效率高，其原因如下：
序列化速度快的原因：
a. 编码 / 解码 方式简单（只需要简单的数学运算 = 位移等等）
b. 采用 Protocol Buffer 自身的框架代码 和 编译器 共同完成
序列化后的数据量体积小（即数据压缩效果好）的原因：
a. 采用了独特的编码方式，如 Varint、Zigzag 编码方式等等
b. 采用 T - L - V 的数据存储方式：减少了分隔符的使用 & 数据存储得紧凑
```

