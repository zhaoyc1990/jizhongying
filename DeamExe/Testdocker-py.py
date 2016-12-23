# coding: utf-8
#!/usr/bin/env python
import os, json
from docker import Client

if __name__ == '__main__':
    cli = Client(base_url='tcp://192.168.239.128:6732', timeout=2)
    for line in cli.pull('192.168.2.246:5000/busybox', tag='latest' , stream=True):
        ss = eval(line)
        status = ss['status']
        if status == 'Extracting' or status == 'Downloading':
            current = ss['progressDetail']['current']
            total = ss['progressDetail']['total']
            percent = current *20 /total
            print percent
            # jindu = ss['progressDetail']['current'] + ss['progressDetail']['total']
            # # print ss['status'] + ':' + ss['progress']
            # print jindu
        else:
            try:
                print ss['status'] + ":" + ss['id']
            except KeyError:
                print ss['status']
       # print(json.dumps(json.loads(line), indent=4))
        # print type(line)

    #############################################
import sys, time


# class ProgressBar:
#     def __init__(self, count=0, total=0, width=50):
#         self.count = count
#         self.total = total
#         self.width = width
#
#     def move(self):
#         self.count += 1
#
#     def log(self, s):
#         sys.stdout.write(' ' * (self.width + 9) + '\r')
#         sys.stdout.flush()
#         print s
#         progress = self.width * self.count / self.total
#         sys.stdout.write('{0:3}/{1:3}: '.format(self.count, self.total))
#         sys.stdout.write('#' * progress + '-' * (self.width - progress) + '\r')
#         if progress == self.width:
#             sys.stdout.write('\n')
#         sys.stdout.flush()
#
#
# bar = ProgressBar(total=10)
# for i in range(10):
#     bar.move()
#     bar.log('We have arrived at: ' + str(i + 1))
#     time.sleep(1)