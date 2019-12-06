- 根据端口查找运行程序位置
```
1、lsof -i :9988 查看9988端口运行的程序，找到pid
2、通过上面获得的PID来查看ssh的执行的命令和路径
# ps -ef|grep 2445
3、kill -9 pid 杀死对应程序
```

- 用户设置

```
groupadd neoway 
useradd -g neoway neoway 
passwd neoway
```

- 防火墙和端口

```
1.启动防火墙 systemctl start firewalld   
2.设置开机启动 systemctl enable firewalld
3.重启防火墙 firewall-cmd --reload
4.在指定区域打开端口（记得重启防火墙）
firewall-cmd --zone=public --add-port=80/tcp(永久生效再加上 --permanent)

说明：
–zone 作用域
–add-port=8080/tcp 添加端口，格式为：端口/通讯协议
–permanent #永久生效，没有此参数重启后失效
```

- Linux关机和重启

```
关机命令有halt，init 0，poweroff，shutdown -h 时间，其中shutdown是最安全的
重启命令有reboot, init 6, shutdow -r 时间 
```

- 命令行操作

```
复制当前行：yy
删除当前行：dd
删除多行：ndd
```

- 文件权限

```
drwxr-xr-x
d ：第一位表示文件类型，d是目录文件、l是链接文件、-是普通文件、p是管道
rwx ：第2-4位表示这个文件的属主拥有的权限。r是读、w是写、x是执行
r-x ：第5-7位表示和这个文件属主所在同一个组的用户所具有的权限
r-x ：第8-10位表示其他用户所具有的权限
```

- 设置静态IP
```
1、vi /etc/sysconfig/network-scripts/ifcfg-*
设置：
NM_CONTROLLED=no
ONBOOT=yes #开机启用本配置  
BOOTPROTO=static #dhcp改为static
IPADDR=192.168.2.167 #静态IP（增加）
NETMASK=255.255.255.0 #子网掩码（增加）
GATEWAY=192.168.2.254 #默认网关（增加）
DNS1="192.168.2.69/108"

2、vi /etc/sysconfig/network
NETWORKING=yes
HOSTNAME=centos167

3、systemctl restart network.service 

4、出现问题的话
输入ip addr，找到类似 link/ether 00:50:56:aa:4b:25 brd ff:ff:ff:ff:ff:ff
编辑ifcfg-*：HWADDR=00:50:56:aa:4b:25

netstat -rn 显示网络信息

route  显示路由信息

ip addr 查看ip

cat /etc/resolv.conf 查看dns

```







