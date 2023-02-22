from django.db import models
from django.forms import ModelForm
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
import re


def validate_hash(value):
    reg = re.compile('^\d+ [А-я]+$')
    if not reg.match(value):
        raise ValidationError(u'%s hashtag doesnot comply' % value)


class Profile(models.Model):
    external_id = models.PositiveBigIntegerField(verbose_name='ID пользователя в соц сети', unique=True)
    name = models.TextField(verbose_name='Имя пользователя')

    def __str__(self):
        return f"#{self.external_id} {self.name}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to=Profile,
        verbose_name="Профиль",
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name="Текст",
        validators=[validate_hash],
    )
    created_at = models.DateTimeField(
        verbose_name="Время получения",
        auto_now_add=True,
    )

    def __str__(self):
        return f"Сообщение {self.pk} от {self.profile}"

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class CategoryEx(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=255)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f"{self.pk} {self.name}"


class DayEx(models.Model):
    sum = models.PositiveIntegerField(verbose_name="Сумма")
    id_category = models.ForeignKey(CategoryEx, on_delete=models.PROTECT, verbose_name="Категория")
    date = models.DateField(verbose_name="Время получения", auto_now_add=True)
    profile = models.ForeignKey(
        to=Profile,
        verbose_name="Профиль",
        on_delete=models.PROTECT,
        null=True
    )

    class Meta:
        verbose_name = 'День'
        verbose_name_plural = 'День'

    def __str__(self):
        return f"Сообщение {self.pk} от {self.profile}"


class MonthsEx(models.Model):
    sum = models.PositiveIntegerField(verbose_name="Сумма")
    id_category = models.ForeignKey(CategoryEx, on_delete=models.PROTECT, verbose_name="Категория")
    date = models.DateField(verbose_name="Время получения", auto_now_add=True)
    profile = models.ForeignKey(
        to=Profile,
        verbose_name="Профиль",
        on_delete=models.PROTECT,
        null=True)

    class Meta:
        verbose_name = 'Месяц'
        verbose_name_plural = 'Месяц'
