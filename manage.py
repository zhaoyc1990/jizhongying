# coding: utf-8
#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    #在这启动一个socket服务端，做到最后业务操作，会打断django 运行，故再启动一个服务端做业务逻辑
    #尽量放轻django
    ##########3
    #每次重启都将删除通道组数据 表

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jizhongying.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django

        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise

    execute_from_command_line(sys.argv)
