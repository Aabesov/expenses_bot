from django.contrib import admin
from .models import Profile, Message, CategoryEx, DayEx, MonthsEx
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "profile", "text", "created_at")


@admin.register(CategoryEx)
class CategoryExAdmin(admin.ModelAdmin):
    list_display = ("name", )


@admin.register(DayEx)
class DayExAdmin(admin.ModelAdmin):
    list_display = ("id", "sum", "id_category", "date", "profile")


@admin.register(MonthsEx)
class MonthsExAdmin(admin.ModelAdmin):
    list_display = ("id", "sum", "id_category", "date", "profile")