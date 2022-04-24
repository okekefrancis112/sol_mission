# from re import M
from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea, TextInput

# Register your models here.
# admin.site.register(NewUser)
admin.site.register(Board)
admin.site.register(Mission)
admin.site.register(Payment)
admin.site.register(Image)
admin.site.register(Category)
# admin.site.register(Comment)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {
        'slug': ('title',)
    }
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'date_added')
    list_filter = ('active', 'date_added', 'updated')
    search_fields = ('name', 'body')
    
class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('email', 'user_name', 'first_name', 'last_name')
    list_filter = ('email', 'user_name', 'first_name', 'last_name', 
                    'is_active', 'is_staff')
    ordering = ('-start_date',)
    list_display = ('email', 'user_name', 'first_name', 'last_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name', 'last_name', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active', )}),
        ('Personal', {'fields': ('about', )}),
    )
    formfield_overrides = {
        NewUser.about:{'widget': Textarea(attrs={'rows':10, 'cols':40})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'last_name', 'password1',
                       'password2', 'is_active', 'is_staff')
        }),
    )
    
    
admin.site.register(NewUser, UserAdminConfig)
    

