from django.urls import path

from applications.meta.applications.blog import views
from applications.meta.applications.blog.apps import BlogConfig

app_name = BlogConfig.label

urlpatterns = [
    path("", views.AllBlogPostsView.as_view(), name="all_posts"),
    path("post/<int:pk>/", views.BlogPostView.as_view(), name="post"),
]
