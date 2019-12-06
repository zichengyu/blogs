- [数据库备份与恢复](https://www.cnblogs.com/xiaotengyi/p/6393972.html)   
 
```
mongodump -h 127.0.0.1:27017 -d pttcloud --dumpDbUsersAndRoles -o /home/neoway/backup/

mongorestore -h 127.0.0.1:27017 -d pttcloud --dir /home/neoway/backup/pttcloud
```

- 更新用户密码

```
db.changeUserPassword('tank2','test');

db.updateUser(
   "user123",
   {
      pwd: "KNlZmiaNUp0B",
      customData: { title: "Senior Manager" }
   }
)

```

- 添加用户

```
db.createUser(
   {
     user:"admin",
     pwd:"neowayyzc",
     roles:[ "readWrite", { role:"root", db:"admin" } ]
   }
)
```

