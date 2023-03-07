from django.conf import settings
from telegram import Update
from telegram.ext import CallbackContext, MessageHandler, CommandHandler, filters, ApplicationBuilder, \
    ContextTypes, CallbackQueryHandler
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram._inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from ugc.models import Message, Profile, CategoryEx, DayEx, MonthsEx
import logging
import os
import django
import datetime
import csv
from .expenses import month_expenses, day_expenses
from .expenses_detail import months_detail, day_detail
from .scrooling import scrolling_days, scrolling_months
from .delete import delete_check, delete

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

application = ApplicationBuilder().token(settings.TOKEN).build()

DAY, MONTH, BACK, SETTINGS, RES_NAME, \
    BACK_MON, QWER, YESTERDAY, TOMORROW, \
    LAST_MONTH, NEXT_MONTH, DATA, DELETE_DAY, \
    DELETE_MONTH, NO_DEL_DAY, DELETE_DAY_2, \
    DELETE_ANSWER = range(17)


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
                 f"{x[0]}.0 -- Категория -- {x[1]}",
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


async def back_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == '16':
        query = update.callback_query
        await query.answer()
        cat_name = query.message.text.split('\n')[1]
        date = query.message.text.split('\n')[0]
        profile = Profile.objects.get(external_id=query.from_user.id)

        category_id = CategoryEx.objects.get(name=cat_name)
        day_data_delete = DayEx.objects.filter(profile=profile, id_category=category_id.id, date=date).delete()
        month_data_delete = MonthsEx.objects.filter(profile=profile, id_category=category_id.id, date=date).delete()

        await query.delete_message()

        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=f'Вы успешно удалили категорию -- {cat_name}'
        )
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

        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=f"———\n"
                 f"в этом месяце: {b}.0 \n"
                 f"Сегодня: {a}.0",
            reply_markup=reply_markup,
        )
    elif query.data == '166':
        query = update.callback_query
        await query.answer()
        cat_name = query.message.text.split('\n')[1]
        date = query.message.text.split('\n')[0]
        profile = Profile.objects.get(external_id=query.from_user.id)

        category_id = CategoryEx.objects.get(name=cat_name)
        month_data_delete = MonthsEx.objects.filter(profile=profile, id_category=category_id.id,
                                                    date__year=date.split('-')[0],
                                                    date__month=date.split('-')[1]).delete()
        day_data_delete = DayEx.objects.filter(profile=profile, id_category=category_id.id,
                                               date__year=date.split('-')[0],
                                               date__month=date.split('-')[1]).delete()

        await query.delete_message()

        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=f'Вы успешно удалили категорию -- {cat_name}'
        )
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

        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=f"———\n"
                 f"в этом месяце: {b}.0 \n"
                 f"Сегодня: {a}.0",
            reply_markup=reply_markup,
        )
    else:
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
                 f"в этом месяце: {b}.0 \n"
                 f"Сегодня: {a}.0",
            reply_markup=reply_markup,
        )


async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Получить выписку", callback_data=str(DATA)),
        ],
        [InlineKeyboardButton("Назад", callback_data=str(BACK))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Настройки",
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
application.add_handler(CallbackQueryHandler(month_expenses, pattern="^" + str(BACK_MON) + "$"))
application.add_handler(CallbackQueryHandler(day_expenses, pattern="^" + str(QWER) + "$"))
application.add_handler(CallbackQueryHandler(scrolling_days, pattern="^" + str(YESTERDAY) + "$"))
application.add_handler(CallbackQueryHandler(scrolling_days, pattern="^" + str(TOMORROW) + "$"))
application.add_handler(CallbackQueryHandler(scrolling_months, pattern="^" + str(LAST_MONTH) + "$"))
application.add_handler(CallbackQueryHandler(scrolling_months, pattern="^" + str(NEXT_MONTH) + "$"))
application.add_handler(CallbackQueryHandler(settings, pattern="^" + str(SETTINGS) + "$"))
application.add_handler(CallbackQueryHandler(delete_check, pattern="^" + str(DELETE_DAY) + "$"))
application.add_handler(CallbackQueryHandler(delete_check, pattern="^" + str(122) + "$"))
application.add_handler(CallbackQueryHandler(day_expenses, pattern="^" + str(NO_DEL_DAY) + "$"))
application.add_handler(CallbackQueryHandler(delete, pattern="^" + str(DELETE_DAY_2) + "$"))
application.add_handler(CallbackQueryHandler(delete, pattern="^" + str(155) + "$"))
application.add_handler(CallbackQueryHandler(back_menu, pattern="^" + str(DELETE_ANSWER) + "$"))
application.add_handler(CallbackQueryHandler(back_menu, pattern="^" + str(166) + "$"))

for i in CategoryEx.objects.all():
    application.add_handler(CallbackQueryHandler(months_detail, str(i.name)))
    application.add_handler(CallbackQueryHandler(day_detail, str(f"0{i.name}")))
application.add_handler(echo_handler)

application.run_polling()
