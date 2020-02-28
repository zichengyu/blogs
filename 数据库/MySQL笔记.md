- 备份与恢复

```
mysqldump -h192.168.2.167 -P3017 -uyzc -p --all-databases --triggers --routines --events > MySqlBackup167.sql

mysql -u root -p < C:\MySqlBackup167.sql
```

- innodb刷盘机制   
innodb_flush_log_at_trx_commit 0/1/2   
1：事务每次提交都会将log buffer中的日志写入os buffer并调用fsync()刷到log file on disk中。即使系统崩溃也不会丢失任何数据，但每次提交都写入磁盘，IO性能较差。   
0：事务提交时不会将log buffer中日志写入到os buffer，而是每秒写入os buffer并调用fsync()写入到log file on disk中。也就是说设置为0时是(大约)每秒刷新写入到磁盘中的，当系统崩溃，会丢失1秒钟的数据。   
2：每次提交都仅写入到os buffer，然后是每秒调用fsync()将os buffer中的日志写入到log file on disk。   
[innodb刷盘机制](https://github.com/yu757371316/blogs/blob/master/images/Innodb%E5%88%B7%E7%9B%98%E6%9C%BA%E5%88%B6.png)

- Redo log    
默认就是N个文件ib_logfileN中，默认每个48M，且不会变大，满了 就从头开始覆盖以前的数据，类似[圆环](https://github.com/yu757371316/blogs/blob/master/images/redo_log.png)

- [innodb存储引擎更新语句执行流程](https://github.com/yu757371316/blogs/blob/master/images/innodb%E6%9B%B4%E6%96%B0%E8%AF%AD%E5%8F%A5%E6%B5%81%E7%A8%8B.png)

```
1、更新语句到达server层，语法词法分析后转入存储引擎层，
2、存储引擎将更新写入到innodb_buffer_poll中(依赖缓存刷新机制刷到磁盘)
3、缓存写入完成后，记录redo log(磁盘顺序写)，并将redo log状态置为prepare
4、存储引擎返回server，可以提交事务了
5、server层写入binlog
6、server层向存储引擎发送请求commit事务
7、存储引擎将redo log状态置为commiit状态
```

