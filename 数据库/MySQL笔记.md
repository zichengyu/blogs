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

- 事务隔离的解决方案
```
1、在读取数据前，对其加锁，阻止其他事务对数
据进行修改(LBCC) Lock Based Concurrency Control。
2、生成一个数据请求时间点的一致性数据快照 (Snapshot)，并用这个快照来提供一定级别(语句级或事 务级)的一致性读取(MVCC)Multi Version Concurrency Control。

mvcc实现机制是在行后面新增两个字段：
1、DB_TRX_ID，6字节:插入或更新行的最后一个事务的事务 ID，事务编号是自动递增的(创建版本)。
2、DB_ROLL_PTR，7字节:回滚指针(删除版本)。
```

- MySQL锁类型
```
共享锁(行锁):又称为读锁，简称S锁，顾名思义，共享锁就是多个事务对于同一数 据可以共享一把锁，都能访问到数据，但是只能读不能修改
排它锁(行锁):又称为写锁，简称X锁，排他锁不能与其他锁并存
意向共享锁(表锁):表示事务准备给数据行加入共享锁，也就是说一个数据行加共享锁前必须先取得该表的IS锁。
意向排它锁(表锁):表示事务准备给数据行加入排他锁，说明事务在一个数据行加排他锁前必须先取得该表的IX锁
```

- MySQL行锁算法   
[示意图](https://github.com/yu757371316/blogs/blob/master/images/Innodb%E8%A1%8C%E9%94%81%E7%A4%BA%E6%84%8F%E5%9B%BE.png)
```
1、Gap Locks(间隙锁)：唯一性索引等值查询，精确匹配；Gap锁之间不冲突
2、Record Locks(记录锁)：记录不存在时
3、Next-key Locks(临键锁)：范围查询，且同时包含记录和区间，加该锁；
    innodb默认的行锁算法，相当于前两中锁的和
    锁定范围时最后一个记录的下一个左开右闭区间
    当查询不到记录时，会退化为间隙锁；
    当等值查询刚好命中唯一索引时，会退化为记录锁
```


