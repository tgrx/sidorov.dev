from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from applications.meta.applications.blog.forms import CommentForm
from applications.meta.applications.blog.models import Post


class AllBlogPostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post


class BlogPostView(DetailView):
    template_name = "blog/post.html"
    model = Post

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            ctx['form'] = CommentForm(initial={"post": self.object, "author": self.request.user})

        return ctx


class CommentView(FormView):
    form_class = CommentForm
    http_method_names = ["post"]

    def get_success_url(self):
        url = reverse_lazy("meta:blog:post", kwargs={"pk": self.kwargs["pk"]})

        return url

    def form_valid(self, form):
        form.save()
        self.__post = form.instance.post

        return super().form_valid(form)
