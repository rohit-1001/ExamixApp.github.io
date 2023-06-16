from rest_framework import serializers
from backendapp.models import user_data

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=user_data
        fields=('email', 'password', 'checkbox')