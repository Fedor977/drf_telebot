from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseView, TelegramAdmin

router = DefaultRouter()
router.register(r'courses', CourseView)
router.register(r'admins', TelegramAdmin)

urlpatterns = [
    path('api/', include(router.urls)),
]
