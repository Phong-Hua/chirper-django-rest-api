from django.urls import path
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()

urlpatterns = [

    # Register create user view
    path('user/create/', views.CreateUserAPIView.as_view(),
         name='user-create'),
    # Register list all users
    path('user/list/', views.ListUserAPIView.as_view(),
         name='user-list'),
    # Register retrieve a single user
    path('user/details/<pk>/', views.RetrieveUserAPIView.as_view(),
         name='user-details/'),
    # Register login view
    path('login/', views.UserLoginView.as_view(), name='login'),
    # Register router to urls
    # path('', include(router.urls))
]
