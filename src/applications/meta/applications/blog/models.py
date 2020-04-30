from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse_lazy

User = get_user_model()


class Post(models.Model):
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    nr_likes = models.IntegerField(null=True, blank=True)
    nr_dislikes = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse_lazy("meta:blog:post", kwargs={"pk": str(self.pk)})

    def upvote(self):
        if self.nr_likes is None:
            self.nr_likes = 0

        self.nr_likes += 1
        self.save()

    def downvote(self):
        if self.nr_dislikes is None:
            self.nr_dislikes = 0

        self.nr_dislikes += 1
        self.save()


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    message = models.TextField()
