from django.views.generic import DetailView
from django.views.generic import ListView

from applications.meta.applications.blog.models import BlogPost


class AllBlogPostsView(ListView):
    template_name = "blog/all_posts.html"
    model = BlogPost


class BlogPostView(DetailView):
    template_name = "blog/post.html"
    model = BlogPost
