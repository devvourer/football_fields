from rest_framework import serializers

from .models import Field

class FieldSerializer(serializers.Serializer):
    model = Field

    class Meta:
        fields = ('title', 'size', 'type', 'service', 'price', 'location', 'owner')
