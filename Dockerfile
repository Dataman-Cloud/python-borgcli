FROM demoregistry.dataman-inc.com/library/centos7-base:latest

# install python3
RUN yum install -y epel-release && yum install -y python34 && \
	yum clean all

#install python3 pip
RUN curl "https://bootstrap.pypa.io/get-pip.py"  |python3

MAINTAINER Zheng Liu zliu@dataman-inc.com

RUN mkdir /code
ADD . /code/

RUN pip3 install -r /code/requirements.txt

WORKDIR /code
