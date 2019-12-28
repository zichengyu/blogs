		三大器在springboot中使用时，首先实现相应的接口定义类，然后通过配置类将其加入到spring容器中，从而实现相应的功能。

### 监听器

​		listener是servlet规范中定义的一种特殊类。用于监听servletContext、HttpSession和servletRequest等域对象的创建和销毁事件。监听域对象的属性发生修改的事件。用于在事件发生前、发生后做一些必要的处理。其主要可用于以下方面：**1**、统计在线人数和在线用户	**2**、系统启动时加载初始化信息	**3**、统计网站访问量	**4**、记录用户访问路径。

##### 	1 实现指定Listener接口

```java
// 实现listener接口后，在通过WebMvcConfigurer实现类注册
public class MyHttpSessionListener implements HttpSessionListener {

    public static int online = 0;
    @Override
    public void sessionCreated(HttpSessionEvent se) {
        System.out.println("创建session");
        online ++;
    }

    @Override
    public void sessionDestroyed(HttpSessionEvent se) {
        System.out.println("销毁session");   
    }
}
```

##### 	2 @WebListener

```java
@WebListener
public class MyServletContextListener implements ServletContextListener {
     @Override
        public void contextDestroyed(ServletContextEvent sce) {
            System.out.println("=====MyServletContextListener销毁");
        }
 
        @Override
        public void contextInitialized(ServletContextEvent sce) {
            System.out.println("=====MyServletContextListener初始化");
            System.out.println(sce.getServletContext().getServerInfo());
        }
}
```

### 过滤器

​		Filter是Servlet技术中最实用的技术，Web开发人员通过Filter技术，对web服务器管理的所有web资源：例如Jsp, Servlet, 静态图片文件或静态 html 文件等进行拦截，从而实现一些特殊的功能。例如实现URL级别的权限访问控制、过滤敏感词汇、压缩响应信息等一些高级功能。它主要用于对用户请求进行**预处理**，也可以对HttpServletResponse进行**后处理**。使用Filter的完整流程：Filter对用户请求进行预处理，接着将请求交给Servlet进行处理并生成响应，最后Filter再对服务器响应进行后处理。

##### 		1 @WebFilter

​		配置过滤器名和url策略，但是不支持设置Filter的优先级顺序 

##### 		2 通过FilterRegistrationBean实例注册

```java
		@Bean
    public FilterRegistrationBean filterRegist() {
        FilterRegistrationBean frBean = new FilterRegistrationBean();
        frBean.setOrder(1);
        frBean.setName("myFilter");
        // MyFilter实现Filte接口
        frBean.setFilter(new MyFilter());
        frBean.addUrlPatterns("/*");
        System.out.println("filter");
        return frBean;
    }
```

#### Filter与OncePerRequestFilter区别

OncePerRequestFilter过滤器保证一次请求只调用一次doFilterInternal方法;如内部的forward不会再多执行一次；通常一次请求本来就只filter一次，但并不是所有的container都如我们期望的只过滤一次，servlet版本不同，执行过程也不同，此方法是就是为了兼容不同的web container

### 拦截器

​	Interceptor 在AOP（Aspect-Oriented Programming）中用于在某个方法或字段被访问之前，进行拦截然后在之前或之后加入某些操作。比如日志，安全等。一般拦截器方法都是通过动态代理的方式实现。可以通过它来进行权限验证，或者判断用户是否登陆，或者是像12306 判断当前时间是否是购票时间。

代码如下：

```java
// 实现listener接口后，在通过WebMvcConfigurer实现类注册
public class MyInterceptor implements HandlerInterceptor {
    // 在请求处理之前进行调用(Controller方法调用之前)
    @Override
    public boolean preHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o) throws Exception {
        System.out.println("preHandle被调用");
        System.out.println(httpServletRequest.getParameter("username"));
        if(map.get("name").equals("zhangsan")) {
            return true;    // 如果false，停止流程，api被拦截
        } else {
            PrintWriter printWriter = httpServletResponse.getWriter();    
            printWriter.write("please login again!");    
            return false; 
        }
    }
    @Override
    public void postHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, ModelAndView modelAndView) throws Exception {
        System.out.println("postHandle被调用");
    }

    @Override
    public void afterCompletion(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, Exception e) throws Exception {
        System.out.println("afterCompletion被调用");
    }
}
```



