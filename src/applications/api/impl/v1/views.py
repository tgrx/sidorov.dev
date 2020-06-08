from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from applications.api.impl.v1.serializers import PhotoSerializer
from applications.meta.applications.blog.models import Photo


class PhotoViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PhotoSerializer
    queryset = Photo.objects.all()
