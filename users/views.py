from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions, status
from clear_bit.model import ClearBit
from email_hunter.model import EmailHunter
from users.serializers import UserSerializer, CreateUserSerializer
from .utils import get_tokens_for_user
from .models import User


class CreateUserAPIView(APIView):
    """
    Create User View
    """
    permission_classes = (AllowAny,)

    @staticmethod
    def get_clearbit_data(serializer):
        clearbit = ClearBit()

        if clearbit.is_available():
            # TODO move code to Celery queues
            data = {}
            clearbit_data = clearbit.get_person_enrichment(serializer.data.get('email'))

            # Checking clearbit data
            if clearbit_data is False or clearbit_data is None:
                return False

            # Merging data
            for i in serializer.data:
                data[i] = serializer.data[i]
            for i in clearbit_data:
                data[i] = clearbit_data[i]

            # Validate data
            serializer = CreateUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            return serializer.data

        return False

    def post(self, request):
        user = request.data
        serializer = CreateUserSerializer(data=user)
        serializer.is_valid(raise_exception=True)

        # Verifying email by EmailHunter
        email_hunter = EmailHunter(serializer.data.get('email'))
        if email_hunter.is_available():
            if email_hunter.email_verifier() is False:
                return Response({"error": 'User email is invalid'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Getting additional information with ClearBit
        clearbit_data = self.get_clearbit_data(serializer)

        # Creating user
        serializer.create(clearbit_data) if clearbit_data else serializer.create(serializer.data)

        return Response('User Created!', status=status.HTTP_201_CREATED)


class LoginUserAPIView(APIView):
    """
    Login User View
    """

    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # Simple validate for email and password
        if (email is None) or (password is None):
            return Response({"error": 'Email and password required'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Getting user instance
        user = User.objects.filter(email=email).first()

        # Validate User
        if user is None:
            return Response({"error": 'User not found'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not user.check_password(password):
            return Response({"error": 'Wrong password'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Generating JWT Token
        serialized_user = UserSerializer(user).data
        response = Response(status=status.HTTP_200_OK)
        response.data = {
            'access_token': get_tokens_for_user(user),
            'user': serialized_user,
        }

        return response
