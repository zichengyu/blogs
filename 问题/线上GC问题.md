
```
-XX:NewRatio=2 
-XX:SurvivorRatio=8 
-XX:MaxMetaspaceSize=512m 
-XX:+UseCMSInitiatingOccupancyOnly
-XX:CMSInitiatingOccupancyFraction=80
-XX:CMSFullGCsBeforeCompaction=2
-XX:+CMSParallelRemarkEnabled 
-XX:+UseFastAccessorMethods 
-XX:+UseConcMarkSweepGC 
-XX:+CMSClassUnloadingEnabled 
-XX:+CMSScavengeBeforeRemark 
-XX:+PrintTenuringDistribution 
-XX:+PrintGCDetails 
-XX:+PrintGCDateStamps
-Xloggc:/usr/src/app/config/log/common/gc.log
-XX:+HeapDumpOnOutOfMemoryError
-XX:HeapDumpPath=/tmp/heapdump.hprof
crm_server: '-jar -server -Xms2g -Xmx2g {{ crm_gc_config }}  codemaster-report-service.jar'
crm_start_command: 'java  -Duser.timezone=UTC  {{ crm_server }}
```
