from requests import Response
from rest_framework import viewsets
from rest_framework.decorators import action
#--------------------------------------------
from .models import Courses, TelegramAdmin, Chat
from .seriallizers import CoursesSerializer, TelegramAdminSerializer, ChatSerializer


class CourseView(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer


class ChatView(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer


class AdminTelegramView(viewsets.ModelViewSet):
    queryset = TelegramAdmin.objects.all()
    serializer_class = TelegramAdminSerializer

    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):
        admin = self.get_object()
        if admin:
            admin.is_confirmed = True
            admin.save()
            return Response({'status': 'Администратор подтвержден'})
        return Response({'status': 'Ошибка'}, status=400)

