from django.contrib import admin
from .models import Course, Post, Contact, User, Comment
# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'datetime')

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', )
admin.site.register(Course)
admin.site.register(Post, PostAdmin)
admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Contact, ContactAdmin)
