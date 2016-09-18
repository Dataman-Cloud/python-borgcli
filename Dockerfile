#FROM index.shurenyun.com/zqdou/python:3.4
FROM python:3-onbuild

MAINTAINER Zheng Liu zliu@dataman-inc.com

RUN mkdir /code
ADD . /code/

RUN pip3 install -r /code/requirements.txt

WORKDIR /code

ENTRYPOINT ["python3", "borgapi_cli.py", "-v"]
