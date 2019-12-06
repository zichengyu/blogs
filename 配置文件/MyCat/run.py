#/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: 20160301301
@date:    2017年2月7日
'''
import subprocess,os,time
def start_or_stop(statu):
    print(statu,statu == 'start')
    try:
        if statu == 'start':
            os.chdir(r'/usr/local/zookeeper')
            subprocess.call(r'/usr/local/zookeeper/bin/zkServer.sh start',shell=True)
            subprocess.call(r'/usr/local/mycat/bin/init_zk_data.sh',shell=True)
            
            os.chdir(r'/usr/local/mycat')
            subprocess.call(r'/usr/local/mycat/bin/mycat start',shell=True)
            
            os.chdir(r'/usr/local/mycat-web')
            subprocess.call(r'/usr/local/mycat-web/start.sh &',shell=True)
        if statu == 'stop':
            os.chdir(r'/usr/local/zookeeper')
            subprocess.call(r'/usr/local/zookeeper/bin/zkServer.sh stop',shell=True)
            
            os.chdir(r'/usr/local/mycat')
            subprocess.call(r'/usr/local/mycat/bin/mycat stop',shell=True)
            
            ip=os.popen("ifconfig eth0|grep 'inet addr'|awk -F ':' '{print $2}'|awk '{print $1}'")
            ip=ip.read().strip()
            pid=os.popen("netstat -anp|grep 8082 |awk '{print $7}'").read().split('/')[0]
            if pid != '':
                os.popen('kill -9 {0}'.format(int(pid)))
    except Exception as e:
        print('Exception:',e)
    finally:
        time.sleep(3)
        subprocess.call(r'netstat -lntup',shell=True)       
#Sample usage
statu = str(raw_input('start or stop?:'))
start_or_stop(statu.strip())
