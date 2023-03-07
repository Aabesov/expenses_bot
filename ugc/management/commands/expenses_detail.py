from telegram import Update
from telegram.ext import ContextTypes
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
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


async def day_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    call_back_data = query.data
    date = query.message.text.split('\n')[0]

    keyboard = [
        [
            InlineKeyboardButton("Удалить категорию", callback_data=str(12))
        ],
        [InlineKeyboardButton("Назад", callback_data=str(6))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    profile = Profile.objects.get(external_id=query.from_user.id)
    name_category = CategoryEx.objects.get(name=call_back_data[1:])
    expens = DayEx.objects.filter(profile=profile.id, id_category=name_category.id, date=date)

    months_expenses = 0
    date_l_expenses = f"----- {date} -----\n"

    for item in expens:
        months_expenses += item.sum
        date_l_expenses += f"◦ {item.sum}.0\n"

    await query.edit_message_text(
        text=f"{query.data[1:]}\n"
             f"\n"
             f"{calendar.month_name[datetime.date.today().month]} {datetime.date.today().year}\n"
             f"Расходы: {months_expenses}.0\n"
             f"\n"
             f"{date_l_expenses}\n",
        reply_markup=reply_markup
    )


async def months_detail(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    month_name = query.message.text.split(' ')
    mnum = datetime.datetime.strptime(month_name[0], '%B').month
    start_date = datetime.date(int(month_name[1]), mnum, 11)

    keyboard = [
        [
            InlineKeyboardButton("Удалить категорию", callback_data=str(122))
        ],
        [InlineKeyboardButton("Назад", callback_data=str(6))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    profile = Profile.objects.get(external_id=query.from_user.id)
    name_category = CategoryEx.objects.get(name=query.data)
    expens = MonthsEx.objects.filter(profile=profile.id, id_category=name_category.id,
                                     date__month=start_date.month, date__year=start_date.year)
    months_expenses = 0

    date_l_expenses = ""

    for item in expens:
        months_expenses += item.sum
        date_l_expenses += f"----- {item.date} -----\n" \
                           f"◦ {item.sum}.0\n"

    await query.edit_message_text(
        text=f"{query.data}\n"
             f"\n"
             f"{calendar.month_name[start_date.month]} {start_date.year}\n"
             f"Расходы: {months_expenses}.0\n"
             f"\n"
             f"{date_l_expenses}\n",
        reply_markup=reply_markup
    )
