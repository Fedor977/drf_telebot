from rest_framework import serializers
from .models import Courses, TelegramAdmin, Chat


class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = '__all__'


class TelegramAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramAdmin
        fields = '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'
