from django.contrib import admin

from applications.meta.applications.blog.models import Comment
from applications.meta.applications.blog.models import Photo
from applications.meta.applications.blog.models import Post


@admin.register(Post)
class BlogPostModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoModelAdmin(admin.ModelAdmin):
    pass
