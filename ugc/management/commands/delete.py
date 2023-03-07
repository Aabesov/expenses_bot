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


async def delete_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    cat_name = query.message.text.split('\n')[0]
    date = query.message.text.split('-----')[1].strip()

    if query.data == '122':
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=str(155))
            ],
            [InlineKeyboardButton("Нет", callback_data=str(1))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [
            [
                InlineKeyboardButton("Да", callback_data=str(15))
            ],
            [InlineKeyboardButton("Нет", callback_data=str(14))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f'{date}\n'
             f'{cat_name}\n'
             f'\n'
             f'Вы уверены, что хотите удалить категорию?',
        reply_markup=reply_markup
    )


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    date = query.message.text.split('\n')[0]
    cat_name = query.message.text.split('\n')[1]
    if query.data == '155':
        keyboard = [
            [
                InlineKeyboardButton("Да, я уверен", callback_data=str(166))
            ],
            [InlineKeyboardButton("Нет", callback_data=str(1))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
    else:
        keyboard = [
            [
                InlineKeyboardButton("Да, я уверен", callback_data=str(16))
            ],
            [InlineKeyboardButton("Нет", callback_data=str(14))],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=f'{date}\n'
             f'{cat_name}\n'
             f'\n'
             f'Вы ДЕЙСТВИТЕЛЬНО уверены, что хотите удалить эту категорию?\n'
             f'Это действие нельзя отменить. Все данные будут удалены.',
        reply_markup=reply_markup
    )
