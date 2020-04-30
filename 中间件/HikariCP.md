##### HikariCP优化点

**字节码精简:**    优化代码,直到编译后的字节码最少,这样CPU缓存可以加载更多的程序代码   
**优化代理和拦截器:** 减少代码,例如HikariCP的Statement proxy只有100行代码,只有BoneCP的十分之一   
**自定义数组类型(FastStatementList)代替ArrayList:** 避免每次get()调用都要进行range    check，避免调用remove()时的从头到尾的扫描；      
**自定义集合类型(ConcurrentBag):** 提高并发读写的效率;其他针对BoneCP缺陷的优化，比如对于耗时超过一个CPU时间片的方法调用的研究(但没说具体怎么优化)
---

