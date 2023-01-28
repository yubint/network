from django.contrib import admin

from .models import User , Post
# Register your models here.

@admin.register(User)
class Useradmin(admin.ModelAdmin):
    pass

@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    pass