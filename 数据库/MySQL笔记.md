- 备份与恢复

```
mysqldump -h192.168.2.167 -P3017 -uyzc -p --all-databases --triggers --routines --events > MySqlBackup167.sql

mysql -u root -p < C:\MySqlBackup167.sql
```

