# 什么是拦截器

​        拦截器(Interceptor): 用于在某个方法被访问之前进行拦截，然后在方法执行之前或之后加入某些操作，其实就是AOP的一种实现策略。它通过动态拦截Action调用的对象，允许开发者定义在一个action执行的前后执行的代码，也可以在一个action执行前阻止其执行。同时也是提供了一种可以提取action中可重用的部分的方式。

# 拦截器作用

​        拦截用户的请求并进行相应的处理，比如：判断用户是否登陆，是否在可购买时间内，记录日志信息等。

# Spring中两种实现方式

## 实现HandlerInterceptor接口

​         通过实现HandlerInterceptor接口, 一般通过继承HandlerInterceptorAdapter抽象类实现。

**handlerInterceptor接口实现** 展开原码

```
DispatcherServlet处理流程：DispatcherServlet处理请求时会构造一个Excecution Chain，即(可能多个)拦截器和真正处理请求的Handler
即Interceptor是链式调用的。
```

preHandle: 在执行Handler之前进行，即Controller方法调用之前执行，主要进行初始化操作。

postHandle: 在执行Handler之后进行，即Controller 方法调用之后执行，主要对ModelAndView对象进行操作。

afterCompletion: 在整个请求结束之后，即渲染对应的视图之后执行, 主要进行资源清理工作。

注意事项： 每个Interceptor的调用会依据它在xml文件中声明顺序依次执行。

### DispatcherServlet中拦截器相关

**DispatcherServlet中doDispatch** 

```java
protected void doDispatch(HttpServletRequest request, HttpServletResponse response) throws Exception {
        HttpServletRequest processedRequest = request;
        HandlerExecutionChain mappedHandler = null;
        boolean multipartRequestParsed = false;
 
        WebAsyncManager asyncManager = WebAsyncUtils.getAsyncManager(request);
 
        try {
            ModelAndView mv = null;
            Exception dispatchException = null;
 
            try {
                //检查是否是请求multipart,如文件上传
                processedRequest = checkMultipart(request);
                multipartRequestParsed = processedRequest != request;
 
                // Determine handler for the current request.
                //请求到处理器(页面控制器)的映射，通过HanMapping进行映射
                mappedHandler = getHandler(processedRequest, false);
                if (mappedHandler == null || mappedHandler.getHandler() == null) {
                    noHandlerFound(processedRequest, response);
                    return;
                }
 
                // Determine handler adapter for the current request.
                //处理适配，将处理器包装成相应的适配器
                HandlerAdapter ha = getHandlerAdapter(mappedHandler.getHandler());
 
                // Process last-modified header, if supported by the handler.
                String method = request.getMethod();
                boolean isGet = "GET".equals(method);
                if (isGet || "HEAD".equals(method)) {
                    long lastModified = ha.getLastModified(request, mappedHandler.getHandler());
                    if (logger.isDebugEnabled()) {
                        String requestUri = urlPathHelper.getRequestUri(request);
                        logger.debug("Last-Modified value for [" + requestUri + "] is: " + lastModified);
                    }
                    if (new ServletWebRequest(request, response).checkNotModified(lastModified) && isGet) {
                        return;
                    }
                }
                //这里是关键，执行处理器相关的拦截器的预处理
                if (!mappedHandler.applyPreHandle(processedRequest, response)) {
                    return;
                }
 
                try {
                    // Actually invoke the handler.
                    //由适配器执行处理器（调用处理器相应功能处理方法）
                    mv = ha.handle(processedRequest, response, mappedHandler.getHandler());
                }
                finally {
                    if (asyncManager.isConcurrentHandlingStarted()) {
                        return;
                    }
                }
 
                applyDefaultViewName(request, mv);
                //执行处理器相关的拦截器的后处理
                mappedHandler.applyPostHandle(processedRequest, response, mv);
            }
            catch (Exception ex) {
                dispatchException = ex;
            }
            //该方法中会调用triggerAfterCompletion,执行处理器相关的拦截器的完成后处理
            processDispatchResult(processedRequest, response, mappedHandler, mv, dispatchException);
        }
        catch (Exception ex) {
            triggerAfterCompletion(processedRequest, response, mappedHandler, ex);
        }
        catch (Error err) {
            triggerAfterCompletionWithError(processedRequest, response, mappedHandler, err);
        }
        finally {
            if (asyncManager.isConcurrentHandlingStarted()) {
                // Instead of postHandle and afterCompletion
                mappedHandler.applyAfterConcurrentHandlingStarted(processedRequest, response);
                return;
            }
            // Clean up any resources used by a multipart request.
            if (multipartRequestParsed) {
                cleanupMultipart(processedRequest);
            }
        }
    }
```

**HandlerExecutionChain中applyPreHandle**

```java
boolean applyPreHandle(HttpServletRequest request, HttpServletResponse response) throws Exception {
        if (getInterceptors() != null) {
            //顺序执行拦截器的preHandle方法，如果返回false,则调用triggerAfterCompletion方法
            for (int i = 0; i < getInterceptors().length; i++) {
                HandlerInterceptor interceptor = getInterceptors()[i];
                if (!interceptor.preHandle(request, response, this.handler)) {
                    triggerAfterCompletion(request, response, null);
                    return false;
                }
                this.interceptorIndex = i;
            }
        }
        return true;
    }
```

**applyPostHandle**

```java
void applyPostHandle(HttpServletRequest request, HttpServletResponse response, ModelAndView mv) throws Exception {
    if (getInterceptors() == null) {
        return;
    }
    //逆序执行拦截器的postHandle方法
    for (int i = getInterceptors().length - 1; i >= 0; i--) {
        HandlerInterceptor interceptor = getInterceptors()[i];
        interceptor.postHandle(request, response, this.handler, mv);
    }
}
```

**triggerAfterCompletion** 

```java
void triggerAfterCompletion(HttpServletRequest request, HttpServletResponse response, Exception ex)
        throws Exception {
 
    if (getInterceptors() == null) {
        return;
    }
    //逆序执行拦截器的afterCompletion方法
    for (int i = this.interceptorIndex; i >= 0; i--) {
        HandlerInterceptor interceptor = getInterceptors()[i];
        try {
            interceptor.afterCompletion(request, response, this.handler, ex);
        }
        catch (Throwable ex2) {
            logger.error("HandlerInterceptor.afterCompletion threw exception", ex2);
        }
    }
```

## 实现WebRequestInterceptor接口    

**WebRequestInterceptor接口定义** 折叠原码

```java
//与HandlerInterceptor的区别在于无法终止访问请求
public interface WebRequestInterceptor {
 
    //返回类行为void，与HandlerInterceptor区别就体现在这里
    void preHandle(WebRequest request) throws Exception;
 
    void postHandle(WebRequest request, ModelMap model) throws Exception;
 
    void afterCompletion(WebRequest request, Exception ex) throws Exception;
}
```

​       

\------------------------------------------------

SpringMVC的拦截器Interceptor和过滤器Filter功能非常相似，使用场景也差不多，看起来难以区分。比如两者都能在代码前后插入执行片段，都可以用来实现一些公共组件的功能复用（权限检查、日志记录等），其实它们并不一样，首先了解一下Interceptor和Filter。

## 一.Interceptor

Interceptor是Spring拦截器，要实现一个拦截器功能可以继承Spring的HandlerInterceptor接口：

```java
package com.hpx.xiyou.wuKong.aop;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;
import org.springframework.web.servlet.ModelAndView;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


@Component
public class sanZangInterceptor implements HandlerInterceptor{
    static public final Logger logger = LoggerFactory.getLogger(sanZangInterceptor.class);

    @Override
    public boolean preHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o) throws Exception {
        //System.out.println("interceptortest pre");
        logger.info("interceptortest pre");
        return true;
    }

    @Override
    public void postHandle(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, ModelAndView modelAndView) throws Exception {
        //System.out.println("interceptortest post");
        logger.info("interceptortest post");
    }

    @Override
    public void afterCompletion(HttpServletRequest httpServletRequest, HttpServletResponse httpServletResponse, Object o, Exception e) throws Exception {
        //System.out.println("interceptortest after");
        logger.info("interceptortest after");
    }
}
```

HandlerInterceptor接口有三个需要实现的方法：preHandle()，postHandle()和afterCompletion()。

preHandle方法将在请求处理之前调用，SpringMVC中的Interceptor是链式调用的，每个Interceptor的调用都根据它的声明顺序依次执行，且最先执行其preHandle方法，所以可以在该方法中进行一些前置初始化操作或是预处理。该方法的返回值是布尔类型，如果返回false，表示请求结束，后续的Interceptor和Controller都不会再执行了，如果返回true就执行下一个拦截器的preHandle方法，一直到最后一个拦截器preHandle方法执行完成后调用当前请求的Controller方法。

postHandle方法是在当前请求进行处理之后，也就是Controller方法调用结束之后执行，但是它会在DispatcherServlet进行视图渲染之前被调用，所以可以在这个方法中可以对Controller处理之后的ModelAndView对象进行操作。postHandle方法被调用的方向跟preHandle是相反的，也就是说先声明的Interceptor的postHandle方法反而后执行。

afterCompletion方法需要当前对应的Interceptor的preHandle方法的返回值为true时才会执行。该方法会在整个请求结束之后，也就是在DispatcherServlet渲染了对应的视图之后执行，这个方法的主要作用是用于资源清理工作。

实现一个interceptor拦截器类后，需要在配置中配置使它生效：实现 WebMvcConfigurerAdapter并重写 addInterceptors，同时在这个方法里设置要过滤的URL。

```java
package com.hpx.xiyou.wuKong.Adapter;

import com.hpx.xiyou.wuKong.aop.sanZangInterceptor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurerAdapter;


@Configuration
public class WebConfigurerAdapter extends WebMvcConfigurerAdapter {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new sanZangInterceptor()).addPathPatterns("/wukong/**");

    }
}
```

以上配置生效后，当访问/wukong/***类型url时，控制台输出如下，其中controller为controller方法中的打印信息：*

interceptortest pre
controller
interceptortest post
interceptortest after

## 二.Filter

Filter是Spring过滤器，要定义一个Filter类有以下步骤：

首先定义一个Filter类，继承javax.servlet.Filter类，重写其init、doFilter、destroy方法。init()方法会在Filter初始化后进行调用，在init()方法里面我们可以通过FilterConfig访问到初始化参数( getInitParameter()或getInitParameters() )、ServletContext (getServletContext)和当前Filter部署的名称( getFilterName() )等信息。destroy()方法将在Filter被销毁之前调用。而doFilter()方法则是真正进行过滤处理的方法，在doFilter()方法内部，我们可以过滤请求的request和返回的response，同时我们还可以利用FilterChain把当前的request和response传递给下一个过滤器或Servlet进行处理。

```java
public class FilterTest implements Filter {
    @Autowired
    private PointService pointService;
 
    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        System.out.println("init yes");
    }
 
    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse servletResponse, FilterChain filterChain) throws IOException, ServletException {
        System.out.println("filter test");
        filterChain.doFilter(servletRequest, servletResponse);  // 传递给下一个Filter进行处理
        return;
    }
 
    @Override
    public void destroy() {
        System.out.println("destroy yes");
    }
}
```

然后在配置中使该Filter生效：

```xml
<filter>
    <filter-name>filtertest</filter-name>
    <filter-class>FilterTest</filter-class>
</filter>
<filter-mapping>
    <filter-name>filtertest</filter-name>
    <url-pattern>/point/*</url-pattern>
</filter-mapping>
```

这样，当我们访问/point/*类型的url，控制台输出如下：

```xml
init yes

filter test

controller
```



## 三.比较

同时配置过滤器和拦截器然后请求，结果如下：

```xml
init yes

filter test

interceptortest pre

controller

interceptortest post

interceptortest after
```

可以看到filter优先于interceptor被调用。

过滤器和拦截器主要区别如下：

1.二者适用范围不同。Filter是Servlet规范规定的，只能用于Web程序中，而拦截器既可以用于Web程序，也可以用于Application、Swing程序中。

2.规范不同。Filter是在Servlet规范定义的，是Servlet容器支持的，而拦截器是在Spring容器内的，是Spring框架支持的。

3.使用的资源不同。同其他代码块一样，拦截器也是一个Spring的组件，归Spring管理，配置在Spring文件中，因此能使用Spring里的任何资源、对象(各种bean)，而Filter不行。

4.深度不同。Filter只在Servlet前后起作用，而拦截器能够深入到方法前后、异常跑出前后等，拦截器的使用有更大的弹性。