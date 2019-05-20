from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import FarmLevel, Users, UsersPay, UsersFb
# Register your models here.
class FarmLevelAdmin(admin.ModelAdmin):
    change_list_template = "admin/import.html"
    list_display = ['comment', 'hidden', 'raid']
    fields = ['comment', 'hidden', 'raid']
    ordering = ["id"]

class UsersPayAdmin(admin.StackedInline):
    model = UsersPay
    extra = 1

class UsersFbAdmin(admin.StackedInline):
    model = UsersFb
    fields = ['fb_id', 'fb_key', 'created', 'used']
    extra = 1

class UsersAdmin(admin.ModelAdmin):
    list_display = ['name','email','created']
    fields = ['name','email']
    inlines = [UsersPayAdmin, UsersFbAdmin]
    ordering = ['id']
admin.site.site_header = "Portal admin panel"

admin.autodiscover()
# remove Authentication and Authorization section on admin panel
admin.site.unregister(User)
admin.site.unregister(Group)
# add Farm level and user panle on admin
admin.site.register(FarmLevel,FarmLevelAdmin)
admin.site.register(Users, UsersAdmin)

