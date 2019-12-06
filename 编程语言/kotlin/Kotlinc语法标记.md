1、let扩展函数的实际上是一个作用域函数，当你需要去定义一个变量在一个特定的作用域范围内，let函数的是一个不错的选择；let函数另一个作用就是可以避免写一些判断null的操作。

```
mVideoPlayer?.let {
       it.setVideoView(activity.course_video_view)
       it.setControllerView(activity.course_video_controller_view)
       it.setCurtainView(activity.course_video_curtain_view)
}
```

2、with函数，将某对象作为函数的参数，在函数块内可以通过 this 指代该对象。返回值为函数块的最后一行或指定return表达式。

```
val result = with(user) {
        println("my name is $name, I am $age years old, my phone number is $phoneNum")
        1000
    }
```

3、run函数实际上可以说是let和with两个函数的结合体，run函数只接收一个lambda函数为参数，以闭包形式返回，返回值为最后一行的值或者指定的return的表达式。   

适用于let,with函数任何场景。因为run函数是let,with两个函数结合体，准确来说它弥补了let函数在函数体内必须使用it参数替代对象，在run函数中可以像with函数一样可以省略，直接访问实例的公有属性和方法，另一方面它弥补了with函数传入对象判空问题，在run函数中可以像let函数一样做判空处理

```
getItem(position)?.run{
      holder.tvNewsTitle.text = StringUtils.trimToEmpty(titleEn)
       holder.tvNewsSummary.text = StringUtils.trimToEmpty(summary)
       holder.tvExtraInf = "难度：$gradeInfo | 单词数：$length | 读后感: $numReviews"
       ...   

   }
```

4、从结构上来看apply函数和run函数很像，唯一不同点就是它们各自返回的值不一样，run函数是以闭包形式返回最后一行代码的值，而apply函数的返回的是传入对象的本身。


5、also函数的结构实际上和let很像唯一的区别就是返回值的不一样，let是以闭包的形式返回，返回函数体内最后一行的值，如果最后一行为空就返回一个Unit类型的默认值。而also函数返回的则是传入对象的本身


