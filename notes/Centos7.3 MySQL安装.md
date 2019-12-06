- [Centos7 安装](https://www.cnblogs.com/Jxiaobai/p/6836081.html)

```
1、下载和用户
mysql-5.7.17-1.el5.i686.rpm-bundle.tar 

groupadd mysql
useradd -r -g mysql mysql

2、解压
tar xvf mysql-5.7.17-1.el5.i686.rpm-bundle.tar -C /usr/src/mysql/

3、安装方式可以采用rpm或者yum install，rpm方式缺少的关联包需要手动安装，几个包都存在相互依赖的关系，所用使用--nodeps参数忽略依赖关系
rpm -ivh mysql-community-common-5.7.17-1.el5.i686.rpm  --nodeps 
rpm -ivh mysql-community-libs-compat-5.7.17-1.el5.i686.rpm  --nodeps
rpm -ivh mysql-community-libs-5.7.17-1.el5.i686.rpm  --nodeps
rpm -ivh mysql-community-client-5.7.17-1.el5.i686.rpm  --nodeps
rpm -ivh mysql-community-server-5.7.17-1.el5.i686.rpm --nodeps

4、遇到mariadb冲突
rpm -qa | grep mariadb
sudo yum -y remove mariadb-libs-1:5.5.52-1.el7.x86_64

5、启动数据库 
service mysqld start

6、对于Mysql 5.7.6以后的5.7系列版本，Mysql使用mysqld --initialize或mysqld --initialize-insecure命令来初始化数据库，后者可以不生成随机密码。  
但是安装Mysql时默认使用的是前一个命令，这个命令也会生成一个随机密码。改密码保存在了Mysql的日志文件中。  
a、打开配置文件，找到日志路径：cat /etc/my.cnf  
b、查到密码：cat /var/log/mysqld.log | grep password

改密码：
   第一次：set password = password('大写字母+数字+特殊字符');
   查看密码限制：SHOW VARIABLES LIKE 'validate_password%'; 
   修改mysql密码限制：set global validate_password_policy=0; 
   修改密码为自己的简单密码：set password = password('123456');
   
   
7、安装完mysql后执行自带的安全设置
/usr/bin/mysql_secure_installation

8、修改默认的数据目录：
找到默认的数据目录：cat /etc/my.cnf
拷贝到指定的位置：cp -r /var/lib/mysql/  /usr/local/mysql/

修改/etc/my.cnf: datadir=/usr/local/mysql

重启数据库：service mysqld start

注意：修改mysql默认目录需要修改一下项
a、关闭selinux：
   临时关闭：setenforce 0
   永久关闭：/etc/selinux/config设置SELINUX=enforcing改为SELINUX=disabled
b、apparmor：
   在 /etc/apparmor.d/usr.sbin.mysqld 这个文件中（没有这个文件，则不需要修改），有这两行，规定了mysql使用的数据文件路径权限/var/lib/mysql/ r, /var/lib/mysql/**rwk,你一定看到了，/var/lib/mysql/就是之前mysql安装的数据文件默认路径，apparmor控制这里mysqld可以使用的目录的权限 我想把数据文件移动到/data/mysql下，那么为了使mysqld可以使用/data/mysql这个目录，照上面那两条，增加下面这两条就可以了/data/mysql/ r, /data/mysql/** rwk,
   
   重启apparmor，/etc/inid.d/apparmor restart

自行初始化：mysqld --defaults-file=/etc/my.cnf --initialize  --user=mysql --basedir=/usr/local/mysql-5.7.20 --datadir=/usr/local/mysql-5.7.20/data
```