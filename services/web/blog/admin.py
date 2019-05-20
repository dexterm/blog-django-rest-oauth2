from django.contrib import admin

# Register your models here.
from django.contrib import admin
from blog.models import Post, Comment, Category, Tag
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    #fields = ('title', 'created_at', 'updated_at')

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
