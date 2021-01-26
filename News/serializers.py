from rest_framework import serializers
from .models import SavedNews


class SavedNewsSerializer(serializers.Serializer):

    class Meta:
        model = SavedNews
        fields = '__all__'

    def create(self, validated_data):
        return SavedNews.objects.create(**validated_data)