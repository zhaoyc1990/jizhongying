# coding: utf-8
#!/usr/bin/env python
import tarfile
import os
from Gitopera import Gitopera
import subprocess
import sys

#压缩foldername文件夹, 压缩文件名dest_folder, 压缩格式compression
def mak_tar(foldername, dest_folder, compression='bz2'):
    if compression:
        dest_ext = '.' + compression
    else:
        dest_ext = ''
    arcname = os.path.basename(foldername)
    dest_name = '%s.tar%s' % (arcname, dest_ext)
    dest_path = os.path.join(dest_folder, dest_name)
    if compression:
        dest_cmp = ':' + compression
    else:
        dest_com = ''
    out = tarfile.TarFile.open(dest_path, 'w' + dest_cmp)
    out.add(foldername, arcname)
    out.close()
    return 0

if __name__ == '__main__':
    # args[1] 要打包的代码仓库 args[2] 要切换的版本号 tag
    try:
        gitsite = sys.argv[1]
        srccode = Gitopera().getproject(sys.argv[1])
        tag = sys.argv[2]
    except IndexError:
        print "Error:参数传递错误"
        exit(1)
        # 先切换版本
    try:
        curr_dir = os.path.split(os.path.realpath(__file__))[0]
        git_cmd = 'python ' + curr_dir +  '/Gitopera.py checkout_tag ' + gitsite + " " + tag
        # 返回标准输出信息
        returnCode = subprocess.check_output(git_cmd, shell=True)

    except subprocess.CalledProcessError, e:
        print e
        print 'Error:执行代码切换错误'
        exit(2)
    finally:
        os.chdir(curr_dir)
    print returnCode
    # git仓库下载到本地哪个目录
    # gitpath = os.path.normpath(os.getcwd() + '/git')
    wocao = os.path.split(curr_dir)
    gitpath = os.path.normpath(wocao[0])
    os.chdir(gitpath)
    if mak_tar('git/' + srccode, 'upload') == 0:
        print "OK:代码已打包，准备被走带"
    os.chdir(curr_dir)