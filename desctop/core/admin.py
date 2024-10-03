from django.contrib import admin
from .models import *


@admin.register(Courses)
class CursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'days_and_week', 'time')
    list_display_links = ('id', )
    list_editable = ('name',)


@admin.register(TelegramAdmin)
class CursesAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_id', 'name', 'is_confirmed')
    list_display_links = ('id',)
    list_editable = ('name',)
    actions = ['assign_as_admin']

    def assign_as_admin(self, request, queryset):
        for admin in queryset:
            if not admin.is_confirmed:
                admin.send_admin_confirmation()
                self.message_user(request, f"Увведомление пользователю {admin.name}.")
            else:
                self.message_user(request, f"Пользователь {admin.name} подтпвердил статус админа")

    assign_as_admin.short_description = "Назначить админами и отправить сообщение"