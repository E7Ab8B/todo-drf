from django.conf import settings

from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.tasks.api.views import TaskViewSet
from apps.users.api.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register('users', UserViewSet)
router.register('tasks', TaskViewSet)


app_name = 'api'
urlpatterns = router.urls
