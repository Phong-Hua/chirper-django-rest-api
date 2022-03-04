from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views

app_name = 'api'

router = DefaultRouter()
# Register viewset to router
router.register('user', views.UserProfileViewSet)
urlpatterns = [

    # Register login view
    path('login/', views.UserLoginView.as_view(), name='login'),
    # Register router to urls
    path('', include(router.urls))
]
