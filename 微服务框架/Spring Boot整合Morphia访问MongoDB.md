 **1、 application.yml**
```
spring:
  data:
    mongodb:
      host: 192.168.2.167
      username: caruser
      password: normalneoway
      database: carcloud
      port: 27017
```

 **2、MorphiaFactory**
```
@Configuration
@ConditionalOnClass(Mongo.class)
public class MorphiaFactory {

    @Autowired
    private Mongo mongo;

    @Autowired
    MongoProperties mongoProperties;

    @Bean
    public Datastore get() {
        Morphia morphia = new Morphia();
        return morphia.createDatastore((MongoClient) mongo,mongoProperties.getDatabase());
    }
}
```
**3、实体类**
```
@Entity(value = "test", noClassnameStored = true)
@EnableMongoAuditing
public class UserEntity extends NeoModuleBaseEntity implements Serializable {
    private static final long serialVersionUID = -3258839839160856613L;
    private String data;

    public String getData() {
        return data;
    }

    public void setData(String data) {
        this.data = data;
    }

}
```
**4、DAO**

```
@Component
public class UserDao extends BasicDAO<UserEntity, ObjectId>{

    @Autowired
    public UserDao(Datastore datastore) {

        super(datastore);
    }

}
```
**5、操作类**
 
```
@Autowired
private UserDao userDao;

    @Test
    public void testSaveUser() throws Exception {
        UserEntity user=new UserEntity();
        user.setData("aaaaaaaa");
        user.setCdate(new Date());
        user.setMsgId("1");
        userDao.save(user);
    }
```
