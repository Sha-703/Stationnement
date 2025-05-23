from rest_framework import serializers
from .models import Dashboard  # Replace with your actual model name

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard  # Replace with your actual model name
        fields = '__all__'  # Specify the fields you want to include in the serialization