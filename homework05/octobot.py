import json
import re
from datetime import datetime, timedelta
from os.path import exists

import dateutil  # type: ignore
import gspread  # type: ignore
import pandas as pd  # type: ignore
import requests  # type: ignore
import telebot  # type: ignore
from dateutil.parser import parse  # type: ignore

bot = telebot.TeleBot("5670074293:AAEoqvcWwC55R79vrYBk-wodk1DUQFXhhN8")


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    """Проверяем, что дата дедлайна валидна:
    - дата не может быть до текущей
    - не может быть позже, чем через год
    - не может быть такой, которой нет в календаре
    - может быть сегодняшним числом
    - пользователь не должен быть обязан вводить конкретный формат даты
    (например, только через точку или только через слеш)"""
    try:
        date_formats = [f"%d{divider}%m{divider}%y", f"%d{divider}%m{divider}%Y"]
        date_obj = None
        for date_format in date_formats:
            try:
                date_obj = datetime.strptime(date, date_format).date()
                break
            except ValueError:
                continue
        if date_obj is None:
            return False
        current_date = datetime.now().date()
        if date_obj < current_date:
            return False
        year_later = current_date + timedelta(days=365)
        if date_obj > year_later:
            return False
        return True
    except ValueError:
        return False


def is_valid_url(url: str = "") -> bool:
    """Проверяем, что ссылка рабочая"""
    regex = r"^(https?://|www\.)\S*\.ru$"
    if re.match(regex, url):
        return True
    regex = r"^\S*\.ru$"
    if re.match(regex, url):
        return True
    regex = r"^en\S*\.[a-z]+\.[a-z]{2,3}$"
    if re.match(regex, url):
        return False
    return False


def convert_date(date: str = "01/01/00"):
    """Конвертируем дату из строки в datetime"""
    return datetime.strptime(date, "%d/%m/%y")


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = "1jYp_NzxEwPDi0GRfYjfevhPAqLPSMRWZDiw8aQJPvzE"
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена")
    start(message)


def access_current_sheet():
    """Обращаемся к Google-таблице"""
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        sheet_id = tables[max(tables)]["id"]
        gc = gspread.service_account(filename="credentials.json")
        sh = gc.open_by_key(sheet_id)
        worksheet = sh.sheet1
        ws_values = worksheet.get_all_values()
        df = pd.DataFrame.from_records(ws_values[1:], columns=ws_values[0])
        return worksheet, tables[max(tables)]["url"], df
    except FileNotFoundError:
        return None


def choose_action(message):
    """Обрабатываем действия верхнего уровня"""
    if message.text == "Подключить Google-таблицу":
        info = bot.send_message(message.chat.id, "Отправьте ссылку таблицу")
        bot.register_next_step_handler(info, check_rights)
    elif message.text == "Редактировать предметы":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Добавить предмет")
        start_markup.row("Изменить предмет")
        start_markup.row("Удалить предмет")
        start_markup.row("Удалить всё")
        start_markup.row("Вернуться назад...")
        info = bot.send_message(message.chat.id, "Выберите следующее действие", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайны":
        worksheet, u, df = access_current_sheet()
        if not worksheet.col_values(1)[1:]:
            bot.send_message(message.chat.id, "Таблица пуста, добавьте в нее предмет")
            start(message)
        else:
            start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            start_markup.row("Добавить дедлайн")
            start_markup.row("Изменить дедлайн")
            start_markup.row("Вернуться назад...")
            info = bot.send_message(message.chat.id, "Что изменить в дедлайнах?", reply_markup=start_markup)
            bot.register_next_step_handler(info, choose_deadline_action)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        worksheet, u, df = access_current_sheet()
        today = datetime.now().date()
        one_week = timedelta(days=7)
        week_end = today + one_week
        deadlines = []
        for row in worksheet.get_all_values()[1:]:
            name = row[0]
            dates = []
            for date_str in row[2:]:
                if is_valid_date(date_str):
                    deadline = datetime.strptime(date_str, "%d/%m/%y").date()
                    if today <= deadline < week_end:
                        dates.append(deadline.strftime("%d.%m.%y"))
            if dates:
                deadlines.append(f"{name}: " + ", ".join(dates))

        if not deadlines:
            response = "На этой неделе дедлайнов, к счастью, нет!"
        else:
            response = "Дедлайны на этой неделе:\n" + "\n".join(deadlines)
        bot.send_message(message.chat.id, response)
        start(message)


def check_rights(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row("Да")
    start_markup.row("Нет")
    start_markup.row("Вернуться назад")
    info = bot.send_message(message.chat.id, "Вы предоставили доступ к таблице?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_rights_option)


def choose_rights_option(message):
    if message.text == "Да":
        connect_table(message)
    elif message.text == "Нет":
        info = bot.send_message(message.chat.id, "Предоставьте права доступа и попробуйте еще раз")
        start(message)
    elif message.text == "Вернуться назад":
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    worksheet, u, df = access_current_sheet()
    if message.text == "Добавить предмет":
        info = bot.send_message(message.chat.id, "Введите название предмета")
        new_row = df.shape[0] + 2
        bot.register_next_step_handler(info, add_new_subject, new_row)
    elif message.text == "Изменить предмет":
        reply = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for element in worksheet.col_values(1)[1:]:
            reply.row(f"{element}")
        info = bot.send_message(message.chat.id, "Выберите предмет", reply_markup=reply)
        bot.register_next_step_handler(info, update_subject)
    if message.text == "Удалить предмет":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        subjects = len(worksheet.col_values(1)) + 1
        for i in range(2, subjects):
            start_markup.row(worksheet.cell(i, 1).value)
        info = bot.send_message(message.chat.id, "Какой предмет удалить?", reply_markup=start_markup)
        bot.register_next_step_handler(info, delete_subject)
    elif message.text == "Удалить всё":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        start_markup.row("Да")
        start_markup.row("Нет")
        info = bot.send_message(message.chat.id, "Вы точно хотите удалить всё?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_removal_option)
    elif message.text == "Вернуться назад":
        start(message)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    worksheet, u, df = access_current_sheet()
    if message.text == "Добавить дедлайн":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadlines = len(worksheet.col_values(1)) + 1
        for i in range(2, deadlines):
            start_markup.row(worksheet.cell(i, 1).value)
        info = bot.send_message(message.chat.id, "Для какого предмета изменить дедлайн?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject)  # type: ignore
    elif message.text == "Изменить дедлайн":
        start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        deadlines = len(worksheet.col_values(1)) + 1
        for i in range(2, deadlines):
            start_markup.row(worksheet.cell(i, 1).value)
        info = bot.send_message(message.chat.id, "Для какого предмета изменить дедлайн?", reply_markup=start_markup)
        bot.register_next_step_handler(info, choose_subject)
    elif message.text == "Вернуться назад":
        start(message)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да":
        clear_subject_list(message)
    elif message.text == "Нет":
        start(message)
    elif message.text == "Вернуться назад":
        start(message)


def add_new_deadline(message):
    subject = message.text
    worksheet, u, df = access_current_sheet()
    cell = worksheet.find(subject)
    row = cell.row
    num_cols = len(worksheet.row_values(1))
    deadline_col = None
    for col in range(num_cols, 0, -1):
        if worksheet.cell(row, col).value:
            deadline_col = col
            break
    if deadline_col is None:
        deadline_col = num_cols + 1
    info = bot.send_message(message.chat.id, "Введите дату дедлайна")
    bot.register_next_step_handler(info, update_subject_deadline, subject, deadline_col)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    info = bot.send_message(message.chat.id, "Введите номер работы")
    bot.register_next_step_handler(info, choose_task, message.text)


def choose_task(message, subject):
    info = bot.send_message(message.chat.id, "Введите новую дату дедлайна")
    bot.register_next_step_handler(info, update_subject_deadline, subject, message.text)


def update_subject_deadline(message, subject, task):
    """Обновляем дедлайн"""
    worksheet, u, df = access_current_sheet()
    cell = worksheet.find(subject)
    column = int(task) + 2
    worksheet.update_cell(1, column, task)
    try:
        date = parse(message.text, dayfirst=True)
        today = datetime.now()
        if date > today + timedelta(days=365):
            info = bot.send_message(message.chat.id, "Дата дедлайна слишком далеко, выберете дату поближе")
            bot.register_next_step_handler(info, update_subject_deadline, subject, task)
            return
        elif date > today:
            worksheet.update_cell(cell.row, column, date.strftime("%d/%m/%y"))
            bot.send_message(message.chat.id, "Готово")
            start(message)
        elif today - timedelta(days=1) < date < today + timedelta(days=1):
            worksheet.update_cell(cell.row, column, date.strftime("%d/%m/%y"))
            info = bot.send_message(message.chat.id, "Дедлайн добавлен")
            start(message)
        else:
            info = bot.send_message(message.chat.id, "Дата дедлайта слишком близко" "Введите новую дату")
            bot.register_next_step_handler(info, update_subject_deadline, subject, task)
            return
    except dateutil.parser.ParserError:
        info = bot.send_message(message.chat.id, "Такой даты не существует, введите другую")
        bot.register_next_step_handler(info, update_subject_deadline, subject, task)
        return


def add_new_subject(message, row):
    """Вносим новое название предмета в Google-таблицу"""
    worksheet, u, df = access_current_sheet()
    title = message.text
    worksheet.append_row(["предмет", "ссылка"])
    if worksheet.find(title) is not None:
        info = bot.send_message(message.chat.id, "Название этого предмета уже есть в таблице, введите другое название")
        bot.register_next_step_handler(info, add_new_subject, row)
        return
    else:
        worksheet.update_cell(row, 1, message.text)
        info = bot.send_message(message.chat.id, "Введите ссылку на этот предмет. Если ее нет, то напишите 'нет'")
        bot.register_next_step_handler(info, add_new_subject_url, row)


def add_new_subject_url(message, row):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    try:
        url = message.text
        r = requests.get(url)
        if r.ok:
            worksheet, u, df = access_current_sheet()
            worksheet.update_cell(row, 2, url)
            bot.send_message(message.chat.id, "Готово")
            start(message)
        else:
            info = bot.send_message(message.chat.id, "Ссылка некорректна, вставьте другую")
            bot.register_next_step_handler(info, add_new_subject_url, row)
            return
    except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError) as e:
        info = bot.send_message(message.chat.id, "Ссылка некорректна, вставьте другую")
        bot.register_next_step_handler(info, add_new_subject_url, row)
        return


def update_subject(message):
    """Обновляем информацию о предмете в Google-таблице"""
    worksheet, u, df = access_current_sheet()
    cell = worksheet.find(message.text)
    if cell:
        info = bot.send_message(message.chat.id, "Ведите название предмета")
        bot.register_next_step_handler(info, add_new_subject, cell.row)
    else:
        info = bot.send_message(message.chat.id, "Такого названия нет, попробуйте еще раз")
        bot.register_next_step_handler(info, update_subject)
        return


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    worksheet, u, df = access_current_sheet()
    cell = worksheet.find(message.text)
    if cell:
        worksheet.delete_rows(cell.row)
        bot.send_message(message.chat.id, "Предмет удален")
        start(message)
    else:
        info = bot.send_message(message.chat.id, "Такого названия нет, попробуйте еще раз")
        bot.register_next_step_handler(info, delete_subject)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    worksheet, u, df = access_current_sheet()
    worksheet.clear()
    bot.send_message(message.chat.id, "Всё удалено")
    start(message)


@bot.message_handler(commands=["start"])
def start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if not exists("chat_id.txt"):
        with open("chat_id.txt", "w") as f:
            f.write(str(message.chat.id))
    if exists("tables.json"):
        start_markup.row("Посмотреть дедлайны на этой неделе")
        start_markup.row("Редактировать дедлайны")
        start_markup.row("Редактировать предметы")
        start_markup.row("Подключить Google-таблицу")
    info = bot.send_message(message.chat.id, "Выберите действие", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


if __name__ == "__main__":
    bot.infinity_polling()
