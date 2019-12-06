# 消息事务

------

​    消息事务是在生产者producer到broker或broker到consumer过程中同一个session中发生的，保证几条消息在发送过程中的原子性。

​    在支持事务的session中，producer发送message时在message中带有transactionID。broker收到message后判断是否有transactionID，如果有就把message保存在transaction store中，等待commit或者rollback消息。

# 消息生产者-异步发送

------

   消息生产者使用持久（persistent）传递模式发送消息的时候，Producer.send() 方法会被阻塞，直到 broker 发送一个确认消息给生产者(ProducerAck)，这个确认消息暗示broker已经成功接收到消息并把消息保存到二级存储中。这个过程通常称为同步发送。

 如果应用程序能够容忍一些消息的丢失，那么可以使用异步发送。异步发送不会在受到 broker 的确认之前一直阻塞 Producer.send 方法。

   但有一个例外，当发送方法在一个事务上下文中时，被阻塞的是 commit 方法而不是 send 方法。commit 方法成功返回意味着所有的持久消息都以被写到二级存储中。

   想要使用异步，在brokerURL中增加 jms.alwaysSyncSend=false&jms.useAsyncSend=true

  如果设置了alwaysSyncSend=true系统将会忽略useAsyncSend设置的值都采用同步

​     1) 当alwaysSyncSend=false时，“NON_PERSISTENT”(非持久化)、事务中的消息将使用“异步发送”

​     2) 当alwaysSyncSend=false时，如果指定了useAsyncSend=true，“PERSISTENT”类型的消息使用异步发送。如果useAsyncSend=false，“PERSISTENT”类型的消息使用同步发送。

总结：默认情况(alwaysSyncSend=false,useAsyncSend=false)，非持久化消息、事务内的消息均采用异步发送；对于持久化消息采用同步发送。

   jms.sendTimeout:发送超时时间，默认等于0，如果jms.sendTimeout>0将会忽略（alwaysSyncSend、useAsyncSend、消息是否持久化）所有的消息都是用同步发送！

   `即使使用异步发送，也可以通过producerWindowSize来控制发送端无节制的向broker发送消息`

producerWindowSize:窗口尺寸，用来约束在异步发送时producer端允许积压的(尚未ACK)的消息的尺寸，且只对异步发送有意义。每次发送消息之后，都将会导致memoryUsage尺寸增加(+message.size)，当broker返回producerAck时，如果达到了producerWindowSize上限，即使是异步调用也会被阻塞，防止不停向broker发送消息。

​     通过jms.producerWindowSize=。。。来设置

 

# 消息消费者-消息确认

------

1、确认机制(ack_mod)

​      AUTO_ACKNOWLEDGE = 1    自动确认

​      CLIENT_ACKNOWLEDGE = 2    客户端手动确认   

​      DUPS_OK_ACKNOWLEDGE = 3    自动批量确认

​      SESSION_TRANSACTED = 0    事务提交并确认

​      ACK_MODE描述了Consumer与broker确认消息的方式(时机),比如当消息被Consumer接收之后,Consumer将在何时确认消息。所以ack_mode描述的不是producer于broker之间的关系，而是customer于broker之间的关系。

​      对于broker而言，只有接收到ACK指令,才会认为消息被正确的接收或者处理成功了,通过ACK，可以在consumer与Broker之间建立一种简单的“担保”机制.

​      session = connection.createSession(false, Session.AUTO_ACKNOWLEDGE);

​      第一个参数:是否支持事务，如果为true，则会忽略第二个参数，自动被jms服务器设置为SESSION_TRANSACTED