FROM tomcat:8.5.31-jre8

MAINTAINER yuzicheng yu.zicheng@neoway.com

ENV DIR_WEBAPP /usr/local/tomcat/webapps/

RUN  rm -rf $DIR_WEBAPP/*

ADD ./target/restful.war $DIR_WEBAPP/ROOT.war

VOLUME /usr/local/tomcat/webapps

WORKDIR /usr/local/tomcat/webapps

RUN  unzip $DIR_WEBAPP/ROOT.war  -d  $DIR_WEBAPP/ROOT/

EXPOSE 6375

CMD ["catalina.sh", "run"]