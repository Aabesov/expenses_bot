from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot, Update
from telegram.ext import CallbackContext, MessageHandler, Updater, CommandHandler, filters, ApplicationBuilder, \
    ContextTypes, CallbackQueryHandler
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram._replykeyboardmarkup import KeyboardButton, ReplyKeyboardMarkup
from telegram.ext.filters import MessageFilter
from telegram.request import HTTPXRequest
from telegram._keyboardbuttonpolltype import KeyboardButtonPollType
import asyncio
import re
from django.core.exceptions import ValidationError
from ugc.forms import MessageForm
from django.db.models.aggregates import Count, Sum
from ugc.models import Message, Profile, CategoryEx, DayEx, MonthsEx
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

application = ApplicationBuilder().token(settings.TOKEN).build()

DAY, MONTH, BACK, SETTINGS = range(4)


async def do_echo(update: Update, context: CallbackContext):
    keyboard = [
        [
            InlineKeyboardButton("День", callback_data=str(DAY)),
            InlineKeyboardButton("Месяц", callback_data=str(MONTH)),
        ],
        [InlineKeyboardButton("Настройки", callback_data=str(SETTINGS))],
    ]

    profile, _ = Profile.objects.get_or_create(
        external_id=update.message.chat_id,
        name=update.message.from_user.full_name,
    )
    profile.save()

    m = Message(
        profile=profile,
        text=update.message.text
    )
    if m.clean_fields() is True:
        pass
    else:
        m.save()
        x = update.message.text.split(" ", 1)

        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=f"Cохранено \n"
                 f"{x[0]}--Категория--{x[1]}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        category, _ = CategoryEx.objects.get_or_create(
            name=x[1]
        )
        category.save()

        DayEx.objects.create(
            sum=x[0],
            id_category=category,
            profile=profile,
        )
        MonthsEx.objects.create(
            sum=x[0],
            id_category=category,
            profile=profile,
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I'm a bot, please talk to me!"
    )


async def day_expenses(update: Update, context: CallbackContext):
    query = update.callback_query
    pro = query.from_user.id
    prof = Profile.objects.get(external_id=pro)
    prof_id = prof.id

    queries = DayEx.objects.filter(profile=prof_id, date=datetime.date.today())

    a = 0

    for i in queries:
        a += i.sum

    keyboard = [
        [

        ],
        [
            InlineKeyboardButton("<<", callback_data=str("Left")),
            InlineKeyboardButton(">>", callback_data=str("Right")),
        ],
        [InlineKeyboardButton("Назад", callback_data=str(BACK))]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"{datetime.date.today()}\n"
             f"Расходы: {a} ", reply_markup=reply_markup
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
    month1 = MonthsEx.objects.filter(profile=prof_id).values('id_category').annotate(Sum('sum')).order_by()
    list_of = []
    print(month1)
    for i in month1:
        category_name = str(CategoryEx.objects.get(id=i.get("id_category")))
        sum_sum = i.get('sum__sum')
        res_name = re.sub(f'[0-9]', '', category_name)
        list_of.append(
            [InlineKeyboardButton(f"{res_name} -- {sum_sum}", callback_data=str("&&"))])

    b = 0
    for j in month_expens:
        b += j.sum

    list_of.append([InlineKeyboardButton(text='<<', callback_data=str("&&")),
                    InlineKeyboardButton(text='>>', callback_data=str("&&")),
                    ])
    list_of.append([InlineKeyboardButton('Назад', callback_data=str(BACK))])

    reply_markup = InlineKeyboardMarkup(list_of)

    await query.edit_message_text(
        # chat_id=query.from_user.id,
        text=f"{calendar.month_name[datetime.date.today().month]} {datetime.date.today().year} \n"
             f"Расходы: {b}",
        reply_markup=reply_markup
    )


async def back_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("День", callback_data=str(DAY)),
            InlineKeyboardButton("Месяц", callback_data=str(MONTH)),
        ],
        [InlineKeyboardButton("Настройки", callback_data=str(SETTINGS))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    pro = query.from_user.id
    prof = Profile.objects.get(external_id=pro)
    prof_id = prof.id

    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day

    day_expens = DayEx.objects.filter(profile=prof_id, date=datetime.date.today())
    month_expens = MonthsEx.objects.filter(profile=prof_id, date__year=year, date__month=month)
    a = 0
    b = 0
    for i in day_expens:
        a += i.sum
    for j in month_expens:
        b += j.sum

    await query.edit_message_text(
        text=f"———\n"
             f"в этом месяце: {b} \n"
             f"Сегодня: {a}",
        reply_markup=reply_markup,
    )


if __name__ == '__main__':
    application = ApplicationBuilder().token('TOKEN').build()

echo_handler = MessageHandler(filters.TEXT, do_echo)
s = CommandHandler('start', start)

application.add_handler(s)
application.add_handler(CallbackQueryHandler(day_expenses, pattern="^" + str(DAY) + "$"))
application.add_handler(CallbackQueryHandler(month_expenses, pattern="^" + str(MONTH) + "$"))
application.add_handler(CallbackQueryHandler(back_menu, pattern="^" + str(BACK) + "$"))
application.add_handler(echo_handler)

application.run_polling()
