from rest_framework import serializers
from .models import Student, Token

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll', 'city']


class TokenSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)

    class Meta:
        model = Token
        fields = ['student', 'otp', 'created_at', 'is_verified']
