##### let扩展函数
实际上是一个作用域函数，当你需要去定义一个变量在一个特定的作用域范围内，let函数的是一个不错的选择；let函数另一个作用就是可以避免写一些判断null的操作。

```
mVideoPlayer?.let {
       it.setVideoView(activity.course_video_view)
       it.setControllerView(activity.course_video_controller_view)
       it.setCurtainView(activity.course_video_curtain_view)
}
```

##### with函数
将某对象作为函数的参数，在函数块内可以通过 this 指代该对象。返回值为函数块的最后一行或指定return表达式。

```
val result = with(user) {
        println("my name is $name, I am $age years old, my phone number is $phoneNum")
        1000
    }
```

##### run函数
实际上可以说是let和with两个函数的结合体，run函数只接收一个lambda函数为参数，以闭包形式返回，返回值为最后一行的值或者指定的return的表达式。   

适用于let,with函数任何场景。因为run函数是let,with两个函数结合体，准确来说它弥补了let函数在函数体内必须使用it参数替代对象，在run函数中可以像with函数一样可以省略，直接访问实例的公有属性和方法，另一方面它弥补了with函数传入对象判空问题，在run函数中可以像let函数一样做判空处理

```
getItem(position)?.run{
      holder.tvNewsTitle.text = StringUtils.trimToEmpty(titleEn)
       holder.tvNewsSummary.text = StringUtils.trimToEmpty(summary)
       holder.tvExtraInf = "难度：$gradeInfo | 单词数：$length | 读后感: $numReviews"
       ...   

   }
```

##### apply函数
和run函数很像，唯一不同点就是它们各自返回的值不一样，run函数是以闭包形式返回最后一行代码的值，而apply函数的返回的是传入对象的本身。


##### also函数
实际上和let很像唯一的区别就是返回值的不一样，let是以闭包的形式返回，返回函数体内最后一行的值，如果最后一行为空就返回一个Unit类型的默认值。而also函数返回的则是传入对象的本身

##### 协程 

```
delay：特殊的挂起函数，它不会造成线程阻塞，但是会挂起协程，并且只能在协程中使用
GlobalScope.launch：在后台启动一个新的协程并继续,在 GlobalScope 中启动的活动协程并不会使进程保活。它们就像守护线程。
runBlocking：声明一个协程作用域，会阻塞当前主线程，直到在其作用域中启动的所有协程都执行完毕后才会结束
coroutineScope：创建一个协程作用域并且在所有已启动子协程执行完毕之前不会结束；runBlocking 与 coroutineScope 的主要区别在于后者在等待所有子协程执行完毕时不会阻塞当前线程。
cancel：取消该任务
join：等待任务执行结束
isActive：一个可以被使用在CoroutineScope中的扩展属性，检测当前协程是否被取消
withTimeout：等待指定的延迟后取消追踪

suspend：用于修饰挂起函数，在协程内部可以像普通函数一样使用挂起函数
```


