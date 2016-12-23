#coding: utf-8

#命令池

class Cmdpool():
    def __init__(self, md5):
        self.md5 = md5  #临时执行脚本文件名和PID文件名

    def tailf_log(self,log):
        TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
tailf """ + log
        return TAILF_LOG


    def docker_tailf_log(self,docker_id,log):
        DOCKER_TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
docker exec -it """ + docker_id + """ tailf """ + log
        return DOCKER_TAILF_LOG
    #只需要跳板机
    def forward_tailf_log(self,log, host, port, user, pw):
        FORWARD_TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
/root/shell/Steppingstoines -h """ + host + " -p " + str(port) + " -u " + user + " -pw " + pw + """ -c "tailf """ + log + "\""
        return FORWARD_TAILF_LOG

    #需要跳板+ 并在容器里
    def forward_docker_tailf_log(self,container_id, log, host, port, user, pw):
        FORWARD_DOCKER_TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
/root/shell/Steppingstones -h """ + host + " -p " + str(port) + " -u " + user + " -pw " + pw + """ -c "docker exec -it """ + container_id + " tailf " + log + "\""
        return FORWARD_DOCKER_TAILF_LOG

    #没有关联服务----
    def noserver_tailf_log(self, log, port):
        TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
isrun=`netstat -tnulp | grep ":""" + str(port) + """  " | grep -v grep | awk '{print $NF}'`
if [ -z "$isrun" ];then
    echo "server is not running"
    exit 1
fi
tailf """ + log
        return TAILF_LOG
    def noserver_docker_tailf_log(self, log, port):
        DOCKER_TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
isrun=`netstat -tnulp | grep ":""" + str(port) + """ " | grep -v grep | awk '{print $NF}'`
if [ -z "$isrun" ];then
    echo "server is not running"
    exit 1
else
    container_id=`docker ps | grep :""" + str(port) + """- | grep -v grep | awk '{print \$1}'`
    docker exec -it $container_id """ + "tailf " + log + """
fi"""
        return DOCKER_TAILF_LOG

    def noserver_forward_docker_tailf_log(self, log, ser_port, host, port, user, pw):
        FORWARD_DOCKER_TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
isrun=`netstat -tnulp | grep ":""" + str(port) + """ " | grep -v grep | awk '{print $NF}'`
if [ -z "$isrun" ];then
    echo "server is not running"
    exit 1
else
    stdout=$(/root/shell/Steppingstones -h """ + host + " -p " + str(port) + " -u " + user + " -pw " + pw + """ -c "docker ps | grep :""" + str(ser_port) + """- | grep -v grep | awk '{print \$1}'")
    container_id=`echo $stdout | awk '{print $NF}'`
    /root/shell/Steppingstones -h """ + host + " -p " + str(port) + " -u " + user + " -pw " + pw + """ -c "docker exec -it $container_id tailf """ + log + """"
fi"""
        return FORWARD_DOCKER_TAILF_LOG

    def noserver_forward_tailf_log(self, log, host, port, user, pw):
        FORWARD_TAILF_LOG = """#!/bin/bash
echo $$ > /tmp/""" + self.md5 + """.pid
/root/shell/Steppingstoines -h """ + host + " -p " + str(port) + " -u " + user + " -pw " + pw + """ -c "tailf """ + log + "\""
        return FORWARD_TAILF_LOG