我们在做项目的时候是不是都会区分很多环境呢？比如开发环境、测试环境、生产环境等，那么第一步我将先带大家配置好各个环境；

maven的过滤资源需要结合maven的2个定义才能实现，分别是：

- profile：定义一系列的配置信息，然后指定其激活条件
- resources：指定maven编译资源文件指定到何处的，例如maven的标准资源目录结构是src/main/resources(这个在超级pom中定义到了)，maven进行编译时候就会将resources中的资源文件放到web的WEB-INF/classes下

1. 首先打开我们项目的pom.xml文件加入以下内容：

   ```xml
   <build>
      <finalName>${project.artifactId}-${project.version}</finalName>
      <plugins>
   
         <plugin>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-maven-plugin</artifactId>
            <executions>
               <execution>
                  <goals>
                     <goal>repackage</goal>
                  </goals>
               </execution>
            </executions>
         </plugin>
   
         <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-compiler-plugin</artifactId>
            <version>3.3</version>
            <configuration>
               <source>1.8</source>
               <target>1.8</target>
               <encoding>utf8</encoding>
            </configuration>
         </plugin>
   
      </plugins>
   
      <filters>
          <!-- 指定使用的 filter -->
         <filter>src/main/resources/application-${filter-resource-name}.properties</filter>
      </filters>
      <resources>
         <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>
            <excludes>
               <exclude>filters/*</exclude>
               <exclude>filters/*</exclude>
               <exclude>application-dev.properties</exclude>
               <exclude>application-test.properties</exclude>
               <exclude>application-prod.properties</exclude>
            </excludes>
         </resource>
         <resource>
            <directory>src/main/resources</directory>
            <filtering>true</filtering>
            <includes>
               <include>application-${filter-resource-name}.properties</include>
            </includes>
         </resource>
      </resources>
   </build>
   
   <profiles>
      <profile>
         <id>dev</id>
         <activation>
            <activeByDefault>true</activeByDefault>
         </activation>
         <properties>
            <filter-resource-name>dev</filter-resource-name>
         </properties>
      </profile>
      <profile>
         <id>test</id>
         <properties>
            <filter-resource-name>test</filter-resource-name>
         </properties>
      </profile>
      <profile>
         <id>prod</id>
         <properties>
            <filter-resource-name>prod</filter-resource-name>
         </properties>
      </profile>
   </profiles>
   ```

   这一段相信大家都很熟悉了吧，我就不多做解释了

2. 然后打开application.properties文件，并在其中加入以下内容：

   ```xml
   #表示激活的配置文件（dev|prod|test）
   spring.profiles.active=@filter-resource-name@
   ```

3. 选择指定的profile，使用maven打包

   ```
   开发: mvn package -Pdev 
   测试: mvn package -Ptest
   预演:mvn package -Pprev
   生产:mvn package -Pprod
   ```

   至此，我们项目的基本环境配置已经搭建好，通过maven clean install以下选择dev|test|prod打入你指定的配置，然后run application运行，如果通过localhost:8888可以访问说明你的配置worked了