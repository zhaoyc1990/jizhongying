# coding: utf-8
import os
import subprocess
#未做任务：项目重名

class Gitopera:
    def __init__(self,gitsite,tag=None):
        self.gitsite = gitsite
        self.project = self.getproject(gitsite)
        self.tag = tag
    #以标签号切换版本
    def checkout_tag(self):
        curr_dir = os.getcwd()
        gitpath = os.path.normpath(os.getcwd() + '/git/' + self.project)
        print "gitpath: ", gitpath, "切换工作目录"
        os.chdir(gitpath)
        try:
            git_cmd = ['git checkout master',
                       'git checkout ' + self.tag]
            for cmd in git_cmd:
                returnCode = subprocess.check_call(cmd, shell=True)
                if returnCode != 0:
                    return 1
        except subprocess.CalledProcessError, e:
            print e
            return 1
        finally:
            os.chdir(curr_dir)
        return 0
    #从远程仓库拉回最新的代码
    def clone(self):
        curr_dir = os.getcwd()
        # git仓库下载到本地哪个目录
        gitpath = os.path.normpath(os.getcwd() + '/git')
        print "gitpath: ", gitpath, "切换工作目录"
        os.chdir(gitpath)
        # 以前不需要去项目名重名做处理.....
        try:
            i = 3
            while i:
                i = i-1
                returnCode = subprocess.check_call('git clone ' + self.gitsite, shell=True)
                if returnCode == 0:
                    return 0
        except subprocess.CalledProcessError, e:
            print e
            return 1
        finally:
            os.chdir(curr_dir)
        return 0
    #返回一个tags列表
    def tags(self):
        curr_dir = os.getcwd()
        gitpath = os.path.normpath(os.getcwd() + '/git/' + self.project)
        print "gitpath: ", gitpath, "切换工作目录"
        os.chdir(gitpath)
        try:
            git_cmd = ["git tag"]
            tags = subprocess.check_output(git_cmd, shell=True)
            print tags
            for tag in tags.split("\n"):
                print "tag:" ,tag
            print "type(tags.split()):", type(tags.split("\n"))
        except subprocess.CalledProcessError, e:
            print e  + "列出标签列表，命令出错!!!"
            return 1
        finally:
            os.chdir(curr_dir)
        return tags.split("\n")

    #做一些git全局配置信息
    def pull(self):
        curr_dir = os.getcwd()
        gitpath = os.path.normpath(os.getcwd() + '/git/' + self.project)
        print "gitpath: ", gitpath, "切换工作目录"
        os.chdir(gitpath)
        git_cmd = ["git pull origin", "git pull origin --tags"]
        try:
            for cmd in git_cmd:
                returnCode = subprocess.check_call(cmd, shell=True)
                if returnCode != 0:
                    return 1
        except subprocess.CalledProcessError, e:
            print e
            return 1
        finally:
            os.chdir(curr_dir)
        return 0
    def getproject(gitsite):
        start = 0
        try:
            while True:
                start = gitsite.index("/", start) + 1
        except ValueError, e:
            print e
        if start == 0:
            print "gitsite:" + gitsite + "不是一个合法的git远程仓库"
            return 0
        else:
            end = 0
            try:
                end = gitsite.index(".", start)
            except ValueError:
                pass
            if end == 0:
                return gitsite[start:]
            else:
                return gitsite[start:end]