from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'status', 'publish', 'created']
    list_filter = ('created', 'title', 'status')
    search_fields = ('title', 'body')
    prepopulated_fields = {
        'slug': ('title',)
    }
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']


admin.site.register(Post, PostAdmin)
