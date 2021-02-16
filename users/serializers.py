from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer
    """
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined')
        extra_kwargs = {'password': {'write_only': True}}


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Create User Serializer (use only for create action)
    """
    date_joined = serializers.ReadOnlyField()

    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password', 'location',
                  'bio', 'site', 'avatar')

    # Make hashed password for new user
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(CreateUserSerializer, self).create(validated_data)
