from rest_framework import serializers
from rest_framework.fields import CharField

from applications.meta.applications.blog.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    thumbnail = CharField()

    class Meta:
        model = Photo
        fields = "__all__"
