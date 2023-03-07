from telegram import Update
from telegram.ext import ContextTypes
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import re
from django.db.models.aggregates import Sum
from ugc.models import Profile, CategoryEx, DayEx, MonthsEx
from datetime import timedelta
import logging
import os
import django
import datetime
import calendar

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def scrolling_days(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    pro = query.from_user.id
    prof = Profile.objects.get(external_id=pro)
    prof_id = prof.id
    if query.data == '7':
        today = query.message.text.split('\n')[0]
        yesterday = datetime.datetime.strptime(today, '%Y-%m-%d') - timedelta(1)

        days_expenses = DayEx.objects.filter(profile=prof_id, date=yesterday)
        day1 = DayEx.objects.filter(profile=prof_id, date=yesterday).values('id_category').annotate(
            Sum('sum')).order_by()
        list_of = []
        for i in day1:
            category_name = str(CategoryEx.objects.get(id=i.get("id_category")))
            sum_sum = i.get('sum__sum')
            res_name = re.sub(f'[0-9]', '', category_name).strip()
            list_of.append(
                [InlineKeyboardButton(f"{res_name}: {sum_sum}.0", callback_data=f"0{res_name}")])

        b = 0
        for j in days_expenses:
            b += j.sum

        list_of.append([InlineKeyboardButton(text='<<', callback_data=str(7)),
                        InlineKeyboardButton(text='>>', callback_data=str(8)),
                        ])
        list_of.append([InlineKeyboardButton('Назад', callback_data=str(2))])

        reply_markup = InlineKeyboardMarkup(list_of)

        await query.edit_message_text(
            text=f"{yesterday.strftime('%Y-%m-%d')}\n"
                 f"Расходы: {b}.0 ", reply_markup=reply_markup
        )
    elif query.data == '8':
        today = query.message.text.split('\n')[0]
        tomorrow = datetime.datetime.strptime(today, '%Y-%m-%d') + timedelta(1)

        days_expenses = DayEx.objects.filter(profile=prof_id, date=tomorrow)
        day1 = DayEx.objects.filter(profile=prof_id, date=tomorrow).values('id_category').annotate(
            Sum('sum')).order_by()
        list_of = []
        for i in day1:
            category_name = str(CategoryEx.objects.get(id=i.get("id_category")))
            sum_sum = i.get('sum__sum')
            res_name = re.sub(f'[0-9]', '', category_name).strip()
            list_of.append(
                [InlineKeyboardButton(f"{res_name}: {sum_sum}.0", callback_data=f"0{res_name}")])

        b = 0
        for j in days_expenses:
            b += j.sum

        list_of.append([InlineKeyboardButton(text='<<', callback_data=str(7)),
                        InlineKeyboardButton(text='>>', callback_data=str(8)),
                        ])
        list_of.append([InlineKeyboardButton('Назад', callback_data=str(2))])

        reply_markup = InlineKeyboardMarkup(list_of)

        await query.edit_message_text(
            text=f"{tomorrow.strftime('%Y-%m-%d')}\n"
                 f"Расходы: {b}.0 ", reply_markup=reply_markup
        )


async def scrolling_months(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    pro = query.from_user.id
    prof = Profile.objects.get(external_id=pro)
    prof_id = prof.id
    if query.data == '9':
        month_name = query.message.text.split(' ')
        mnum = datetime.datetime.strptime(month_name[0], '%B').month
        today = datetime.date.today()
        first = today.replace(day=1)
        start_date = datetime.date(int(month_name[1]), mnum, first.day)
        last_month = start_date - datetime.timedelta(days=15)

        month_expens = MonthsEx.objects.filter(profile=prof_id, date__year=last_month.year,
                                               date__month=last_month.month)
        month1 = MonthsEx.objects.filter(profile=prof_id, date__year=last_month.year,
                                         date__month=last_month.month).values(
            'id_category').annotate(Sum('sum')).order_by()
        list_of = []
        for i in month1:
            category_name = str(CategoryEx.objects.get(id=i.get("id_category")))
            sum_sum = i.get('sum__sum')
            res_name = re.sub(f'[0-9]', '', category_name).strip()
            list_of.append(
                [InlineKeyboardButton(f"{res_name}: {sum_sum}.0", callback_data=res_name)])

        b = 0
        for j in month_expens:
            b += j.sum

        list_of.append([InlineKeyboardButton(text='<<', callback_data=str(9)),
                        InlineKeyboardButton(text='>>', callback_data=str(10)),
                        ])
        list_of.append([InlineKeyboardButton('Назад', callback_data=str(2))])

        reply_markup = InlineKeyboardMarkup(list_of)

        await query.edit_message_text(
            text=f"{calendar.month_name[last_month.month]} {last_month.year} \n"
                 f"Расходы: {b}.0",
            reply_markup=reply_markup
        )
    elif query.data == '10':
        month_name = query.message.text.split(' ')
        mnum = datetime.datetime.strptime(month_name[0], '%B').month
        today = datetime.date.today()
        first = today.replace(day=1)
        start_date = datetime.date(int(month_name[1]), mnum, first.day)
        last_month = start_date + datetime.timedelta(days=32)

        month_expens = MonthsEx.objects.filter(profile=prof_id, date__year=last_month.year,
                                               date__month=last_month.month)
        month1 = MonthsEx.objects.filter(profile=prof_id, date__year=last_month.year,
                                         date__month=last_month.month).values(
            'id_category').annotate(Sum('sum')).order_by()
        list_of = []
        for i in month1:
            category_name = str(CategoryEx.objects.get(id=i.get("id_category")))
            sum_sum = i.get('sum__sum')
            res_name = re.sub(f'[0-9]', '', category_name).strip()
            list_of.append(
                [InlineKeyboardButton(f"{res_name}: {sum_sum}.0", callback_data=res_name)])

        b = 0
        for j in month_expens:
            b += j.sum

        list_of.append([InlineKeyboardButton(text='<<', callback_data=str(9)),
                        InlineKeyboardButton(text='>>', callback_data=str(10)),
                        ])
        list_of.append([InlineKeyboardButton('Назад', callback_data=str(2))])

        reply_markup = InlineKeyboardMarkup(list_of)

        await query.edit_message_text(
            text=f"{calendar.month_name[last_month.month]} {last_month.year} \n"
                 f"Расходы: {b}.",
            reply_markup=reply_markup
        )
