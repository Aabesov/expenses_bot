from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
import re
from django.db.models.aggregates import Sum
from ugc.models import Profile, CategoryEx, DayEx, MonthsEx
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


async def day_expenses(update: Update, context: CallbackContext):
    query = update.callback_query
    pro = query.from_user.id
    prof = Profile.objects.get(external_id=pro)
    prof_id = prof.id

    days_expenses = DayEx.objects.filter(profile=prof_id, date=datetime.date.today())
    day1 = DayEx.objects.filter(profile=prof_id, date=datetime.date.today()).values('id_category').annotate(
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
        text=f"{datetime.date.today()}\n"
             f"Расходы: {b}.0 ", reply_markup=reply_markup
    )


async def month_expenses(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    pro = query.from_user.id
    prof = Profile.objects.get(external_id=pro)
    prof_id = prof.id

    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day

    month_expens = MonthsEx.objects.filter(profile=prof_id, date__year=year, date__month=month)
    month1 = MonthsEx.objects.filter(profile=prof_id, date__year=year, date__month=month).values(
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
        # chat_id=query.from_user.id,
        text=f"{calendar.month_name[datetime.date.today().month]} {datetime.date.today().year} \n"
             f"Расходы: {b}.0",
        reply_markup=reply_markup
    )
