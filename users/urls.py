from django.conf.urls import url
from .views import (CreateUserAPIView, LoginUserAPIView)

urlpatterns = [
    url('create', CreateUserAPIView.as_view(), name='create-user'),
    url('login', LoginUserAPIView.as_view(), name='login'),
]
