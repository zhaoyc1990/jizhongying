# coding: utf-8
import os
import subprocess
import sys
#未做任务：项目重名,提示不到位

class Gitopera:
    def __init__(self,gitsite=None,tag=None):
        self.gitsite = gitsite
        self.tag = tag
    #以标签号切换版本
    def checkout_tag(self, path=''):
        project = self.getproject(self.gitsite)
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        if path == '':
            gitpath = os.path.normpath(os.path.split(curr_dir)[0] + '/git/' + project)
        else:
            gitpath = os.path.normpath(path + "/" + project)
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
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        # git仓库下载到本地哪个目录
        gitpath = os.path.normpath(os.getcwd() + '/git')
        os.chdir(gitpath)
        #切换目录后，检查是否有重名项目
        listdir = os.listdir(".")
        project = self.getproject(self.gitsite)
        for listdir in listdir:
            if listdir == project:
                print "Warning:有重名项目名:"+project
                return u"有重名项目名:"+project
        # 以前不需要去项目名重名做处理.....
        try:
            returnCode = subprocess.check_call('git clone ' + self.gitsite, shell=True)
        except subprocess.CalledProcessError, e:
            print e
            return e
        finally:
            os.chdir(curr_dir)
        return 0
    #返回一个tags列表
    def tags(self):
        project = self.getproject(self.gitsite)
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        gitpath = os.path.normpath(os.getcwd() + '/git/' + project)
        # print '切换目录', gitpath
        os.chdir(gitpath)
        try:
            git_cmd = "git tag"
            tags = subprocess.check_output(git_cmd, shell=True)
            # for tag in tags.split("\n"):
            #     print "tag:" ,tag
            # print "type(tags.split()):", type(tags.split("\n"))
        except subprocess.CalledProcessError, e:
            print e  + u"列出标签列表，命令出错!!!"
            return 1
        finally:
            os.chdir(curr_dir)
        return tags

    #做一些git全局配置信息
    def pull(self):
        project = self.getproject(self.gitsite)
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        gitpath = os.path.normpath(os.getcwd() + '/git/' + project)
        print "gitpath: ", gitpath, "切换工作目录<br>"
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
    def getproject(self, gitsite):
        start = 0
        try:
            while True:
                start = gitsite.index("/", start) + 1
        except ValueError, e:
            pass
        if start == 0:
            print "gitsite:" + gitsite + u'不是一个合法的git远程仓库'
            return 1
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

if __name__ == '__main__':
    try:
        gitt = Gitopera(sys.argv[2],sys.argv[3])
    except IndexError:
        try:
            gitt = Gitopera(sys.argv[2])
        except IndexError:
            print u'参数传递不完整004'

    if sys.argv[1] == 'tags':
        return_code = gitt.tags()
        print return_code
    elif sys.argv[1] == 'clone':
        return_code = gitt.clone()
    elif sys.argv[1] == 'pull':
        return_code  = gitt.pull()
    elif sys.argv[1] == 'checkout_tag':
        return_code = gitt.checkout_tag()
        print return_code