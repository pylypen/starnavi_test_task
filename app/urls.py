from django.contrib import admin
from django.urls import path, include
from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('users.urls')),
    path('api/posts', views.PostList.as_view(), name='post-create'),
    path('api/posts/<int:pk>/like', views.LikeCreate.as_view(), name='post-like'),
]
