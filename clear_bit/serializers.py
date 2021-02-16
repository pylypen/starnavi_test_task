from rest_framework import serializers
from users.models import User


class PersonSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = (
            "location",
            "bio",
            "site",
            "avatar",
        )
