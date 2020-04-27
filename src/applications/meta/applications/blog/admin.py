from django.contrib import admin

from applications.meta.applications.blog.models import BlogPost


@admin.register(BlogPost)
class BlogPostModelAdmin(admin.ModelAdmin):
    pass
