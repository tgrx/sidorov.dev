from django.contrib import admin

from applications.meta.applications.blog.models import Post


@admin.register(Post)
class BlogPostModelAdmin(admin.ModelAdmin):
    pass
