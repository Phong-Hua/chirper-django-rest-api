from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import UserProfileViewSet

app_name = 'user'

router = DefaultRouter()
# Register viewset to router
router.register('user', UserProfileViewSet)
urlpatterns = [

    # Register router to urls
    path('', include(router.urls))
]
