##### 线程私有
```
1.程序计数器（Program Counter Register） 可看作当前线程所执行的字节码的行号的标识器

2.虚拟机栈（VM Stack）：一个线程的每个方法在执行的时候都会创造一个栈帧，存储局部变量表，操作数栈，动态链接，方法入口，当每个方法被调用的时候，栈帧入栈，方法执行完后，栈帧出栈。

3.本地方法栈：本地方法栈在作用，运行机制，异常类型等方面和虚拟机栈相同，区别是：虚拟机栈执行的是Java方法，而本地方法栈执行native方法，
```


##### 线程共享
      
```
1.堆（Heap）：存放对象实例，几乎所有对象实例都在这里分配内存
      
2.方法区（Method Area）：方法区是线程共享，用于存储已经被虚拟机加载的类信息，包括版本，field，方法，接口等信息，final常量，静态变量，编译器及时编译的代码等。方法区上执行垃圾回收很少，所以方法区也被称为永久代。
```

##### [CMS的过程问题解决](https://blog.ouyangsihai.cn/shen-ru-li-jie-java-xu-ni-ji-cms-la-ji-hui-shou-qi.html)

```
过程：
1、初始标记：仅仅只是标记一下GCRoots能直接关联到的对象，速度很快，需要“Stop The World”。
2、并发标记：进行GCRoots Tracing的过程，在整个过程中耗时最长。
3、重新标记：为了修正并发标记期间因用户程序继续运作而导致标记产生变动的那一部分对象的标记记录，这个阶段的停顿时间一般会比初始标记阶段稍长一些，但远比并发标记的时间短。此阶段也需要“Stop The World”。
4、并发清除：

问题：
1、内存碎片：由于使用的是标记清除算法
2、remark重新标记时间长：remark阶段停顿时间会很长，在CMS的这四个主要的阶段中，最费时间的就是重新标记阶段。
3、concurrentmodefailure：执行CMSGC的过程中,业务线程也在执行,当年轻代空间满了,执行ygc,需要将存活的对象放入到老年代,而此时老年代空间不足,这时CMS还没有机会回收老年代产生的，会导致退化为Serial old回收
4、promotion failed：在进行MinorGC时，Survivor空间不足，对象只能放入老年代，而此时老年代也放不下造成的，多数是由于老年代有足够的空闲空间，但是由于碎片较多，新生代要转移到老年带的对象比较大,找不到一段连续区域存放这个对象导致的，会导致退化为Serial old回收

解决：
1、设置-XX:CMSFullGCsBeforeCompaction=n -XX:+UseCMSCompactAtFullCollection设置上一次CMS并发GC执行过后，到底还要再执行多少次fullGC才会做压缩。默认是0，即每次都压缩
2、mark操作之前先做一次YoungGC：-XX:+CMSScavengeBeforeRemark
3、提前执行GC，预留足够内存给业务线程：-XX:+UseCMSInitiatingOccupancyOnly -XX:CMSInitiatingOccupancyFraction=60：是指设定CMS在对内存占用率达到60%的时候开始GC。
```
