from rest_framework.viewsets import ModelViewSet

from applications.api.impl.v1.serializers import PhotoSerializer
from applications.meta.applications.blog.models import Photo


class PhotoViewSet(ModelViewSet):
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
