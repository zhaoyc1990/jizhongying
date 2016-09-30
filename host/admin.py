from django.contrib import admin

from .models import hostinfo
from .models import Group
from .models import Group_script
from .models import Script
from LogSplit.models import LogSplit
from LogSplit.models import servicename
# Register your models here.
admin.site.register(servicename)
admin.site.register(LogSplit)
admin.site.register(hostinfo)
admin.site.register(Group)
admin.site.register(Group_script)
admin.site.register(Script)