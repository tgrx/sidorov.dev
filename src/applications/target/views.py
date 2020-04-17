from django.views.generic import DetailView

from applications.target.models import UserInfo


class IndexView(DetailView):
    template_name = "target/index.html"
    model = UserInfo

    def get_object(self, queryset=None):
        if not queryset:
            obj = UserInfo.objects.first()
        else:
            obj = queryset.first()
        return obj
