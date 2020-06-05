from rest_framework import serializers

from applications.meta.applications.blog.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = "__all__"
