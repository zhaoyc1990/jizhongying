from django.contrib import admin

from .models import Environment
from .models import Server
from .models import ConfigureFile
from .models import HttpChannel
# Register your models here.

admin.site.register(Environment)
admin.site.register(Server)
admin.site.register(ConfigureFile)
admin.site.register(HttpChannel)
