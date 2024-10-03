from django.db import models


class Courses(models.Model):
    language_choice = [
        ('ru', 'Russian'),
        ('uz', 'O\'zbek')
    ]

    name = models.CharField(max_length=300, verbose_name='Имя')
    language = models.CharField(max_length=50, verbose_name='Язык', choices=language_choice, default='ru')
    days_and_week = models.CharField(max_length=30, verbose_name='День - Неделя')
    time = models.TimeField(verbose_name='Время обучения')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'


class TelegramAdmin(models.Model):
    telegram_id = models.CharField(max_length=100, unique=True, verbose_name='телеграм_id')
    name = models.CharField(max_length=120, verbose_name='Никнейм')
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'админ'
        verbose_name_plural = 'админы'


class Chat(models.Model):
    CHAT_TYPE_CHOICES = [
        ('group', 'Группа'),
        ('private', 'Личный чат'),
    ]
    telegram_id = models.CharField(max_length=50, unique=True, verbose_name='Телеграм_id')
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPE_CHOICES, verbose_name='Тип чата')
    course = models.ForeignKey(Courses, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Курс')

    def __str__(self):
        return f"{self.telegram_id} ({self.get_chat_type_display()})"
