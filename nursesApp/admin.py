from django.contrib import admin
from .models import Contributor
from .models import Member
from .models import Msg

# Register your models here.
admin.site.register(Contributor)
admin.site.register(Member)
admin.site.register(Msg)
