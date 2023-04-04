import json
from datetime import datetime, timedelta
from time import sleep

import action
import gspread
import pandas as pd
import requests
import telebot
import validators
from gspread import worksheet

bot = telebot.TeleBot("5670074293:AAEoqvcWwC55R79vrYBk-wodk1DUQFXhhN8")
ROW, COL = None, None


def convert_date(date_str: str = "01/01/0000") -> datetime:
    """Конвертируем дату из строки в datetime"""
    # PUT YOUR CODE HERE
    try:
        return datetime.strptime(date_str, "%d/%m/%Y")
    except ValueError:
        print(f"Некорректный формат даты: {date_str}")
        return None


def is_valid_date(date: str = "01/01/00", divider: str = "/") -> bool:
    try:
        parsed_date = datetime.strptime(date, f"%d{divider}%m{divider}%y")
        if datetime.now().date() > parsed_date.date():
            return False
        if parsed_date > datetime.now() + timedelta(days=365):
            return False
        return True
    except ValueError:
        return False


def is_valid_url(url: str = "") -> bool:
    try:
        response = requests.get(url)
        return response.status_code == 200
    except Exception:
        return False


def connect_table(message):
    """Подключаемся к Google-таблице"""
    url = message.text
    sheet_id = url.split("/")[5]
    try:
        with open("tables.json") as json_file:
            tables = json.load(json_file)
        title = len(tables) + 1
        tables[title] = {"url": url, "id": sheet_id}
    except FileNotFoundError:
        tables = {0: {"url": url, "id": sheet_id}}
    with open("tables.json", "w") as json_file:
        json.dump(tables, json_file)
    bot.send_message(message.chat.id, "Таблица подключена!")
    sleep(2)
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
        # PUT YOUR CODE HERE
        mes = bot.send_message(message.chat.id, "Отправьте полную ссылку на таблицу")
        bot.register_next_step_handler(mes, connect_table)
    elif message.text == "Редактировать предметы":
        # PUT YOUR CODE HERE
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Добавить новый предмет")
        markup.row("Редактировать выбранный предмет")
        markup.row("Удалить имеющийся предмет")
        markup.row("Удалить все предметы")
        info = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        bot.register_next_step_handler(info, choose_subject_action)
    elif message.text == "Редактировать дедлайн":
        # PUT YOUR CODE HERE
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Добавить новую дату дедлайна")
        markup.row("Изменить дату дедлайна")
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        bot.register_next_step_handler(message, choose_subject)
    elif message.text == "Посмотреть дедлайны на этой неделе":
        # PUT YOUR CODE HERE
        today = datetime.now()
        worksheet, url, df = access_current_sheet()
        deadline_count = 0
        for i, row in df.iterrows():
            for j, cell_data in enumerate(row.items()):
                cell_data = cell_data[1]
                if cell_data and j > 1:
                    date = convert_date(cell_data)
                    delta = date - today
                    if 0 <= delta.days <= 7:
                        deadline_count += 1
                        bot.send_message(message.chat.id, f"{row['Предмет']}. Работа № {j - 1}\nДедлайн <b>{cell_data}</b>", parse_mode="HTML")
        if deadline_count == 0:
            bot.send_message(message.chat.id, "Дедлайнов на этой неделе нет!")
        sleep(deadline_count)
        start(message)


def choose_subject_action(message):
    """Выбираем действие в разделе Редактировать предметы"""
    # PUT YOUR CODE HERE
    if message.text == "Добавить новый предмет":
        info = bot.send_message(message.chat.id, "Введите название предмета, который желаете добавить")
        bot.register_next_step_handler(info, add_new_subject)

    elif message.text == "Редактировать выбранный предмент":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Изменить название предмета")
        markup.row("Изменить ссылку на таблицу")
        info = bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
        bot.register_next_step_handler(info, choose_subject)

    elif message.text == "Удалить имеющийся предмет":
        choose_subject(message)

    elif message.text == "Удалить все предметы":
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.row("Да, я хочу удалить все предметы")
        markup.row("Нет, я передумал/а")
        info = bot.send_message(message.chat.id, "Желаете ли вы удалить все предметы?", reply_markup=markup)
        bot.register_next_step_handler(info, choose_removal_option)


def choose_deadline_action(message):
    """Выбираем действие в разделе Редактировать дедлайн"""
    # PUT YOUR CODE HERE
    table_data = access_current_sheet()
    ws = table_data[0]
    global ROW, COL
    cell = ws.find(message.text)
    ROW = cell.row
    COL = cell.col
    info = bot.send_message(message.chat.id, "Введите номер работы")
    bot.register_next_step_handler(info, update_subject_deadline, action)


def choose_removal_option(message):
    """Уточняем, точно ли надо удалить все"""
    # PUT YOUR CODE HERE
    """Уточняем, точно ли надо удалить все"""
    if message.text == "Да, я хочу удалить все предметы":
        clear_subject_list(message)

    elif message.text == "Нет, я передумал/а":
        bot.send_message(message.chat.id, "Хорошо")
        sleep(2)
        start(message)


def choose_subject(message):
    """Выбираем предмет, у которого надо отредактировать дедлайн"""
    # PUT YOUR CODE HERE
    worksheet, url, df = access_current_sheet()
    subjects = df["Предмет"].tolist()
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for subject in subjects:
        markup.row(subject)
    info = bot.send_message(message.chat.id, "Выберите предмет", reply_markup=markup)
    bot.register_next_step_handler(info, choose_deadline_action)


def update_subject_deadline(message, action):
    """Обновляем дедлайн"""
    global COL
    if not message.text.isdigit():
        info = bot.send_message(
            message.chat.id,
            "Ошибочка. Введи номер работы как целое число без дополнительных знаков",
        )
        bot.register_next_step_handler(info, update_subject_deadline)
        return
    if int(message.text) > 100:
        info = bot.send_message(
            message.chat.id,
            "Вряд ли у тебя так много работ. Введи номер работы как целое число, не большее, чем 100",
        )
        bot.register_next_step_handler(info, update_subject_deadline)
        return
    table_data = access_current_sheet()
    ws = table_data[0]
    df = table_data[2]
    if action == "Редактировать дедлайн" and int(message.text) > df.shape[1] - 2:
        info = bot.send_message(
            message.chat.id,
            "Такой работы не существует, попробуйте еще раз",
        )
        bot.register_next_step_handler(info, update_subject_deadline, action)
        return
    current_date = ws.cell(ROW, COL + int(message.text) + 1).value
    if current_date:
        info = bot.send_message(
            message.chat.id,
            f"Cейчас по этой работе стоит дедлайн <b>{current_date}</b>.\nВведите новую дату в формате\nDD/MM/YYYY",
            parse_mode="HTML",
        )
    elif action == "Редактировать дедлайн":
        info = bot.send_message(
            message.chat.id,
            "Такой работы не существует, попробуйте еще раз",
        )
        bot.register_next_step_handler(info, update_subject_deadline, action)
        return
    else:
        info = bot.send_message(message.chat.id, "Введи дату дедлайна в формате\nDD/MM/YYYY")
    COL += int(message.text) + 1
    bot.register_next_step_handler(info, update_cell_datetime)


def update_cell_datetime(message):
    try:
        today = datetime.now()
        date = convert_date(message.text)
        delta = date - today
        if delta.days // 365 > 10:
            info = bot.send_message(
                message.chat.id,
                "Ошибка, попробуйте ещё раз",
            )
            bot.register_next_step_handler(info, update_cell_datetime)
            return
    except Exception:
        info = bot.send_message(
            message.chat.id,
            "Ошибка, попробуйте ещё раз",
        )
        bot.register_next_step_handler(info, update_cell_datetime)
        return

    global ROW, COL
    table_data = access_current_sheet()
    ws = table_data[0]
    ws.update_cell(ROW, COL, message.text)
    bot.send_message(message.chat.id, "Готово!")
    sleep(2)
    start(message)


def update_deadline(message, work_number, subject_chosen, df):
    """Обновляем дедлайн"""
    row = df[df["Предмет"] == subject_chosen]
    cell = row.iloc[0, work_number + 1]
    cell.value = message.text
    worksheet.update_cell(cell.row, cell.col, message.text)
    bot.send_message(message.chat.id, f"Дедлайн для работы №{work_number} по предмету {subject_chosen} успешно обновлен")
    start(message)


def add_new_subject(message):
    """Вносим новое название предмета в Google-таблицу"""
    # PUT YOUR CODE HERE
    table_data = access_current_sheet()
    ws = table_data[0]
    ws.append_row([message.text])
    info = bot.send_message(message.chat.id, "Введите полную ссылку на таблицу")
    bot.register_next_step_handler(info, add_new_subject_url)


def add_new_subject_url(message):
    """Вносим новую ссылку на таблицу предмета в Google-таблицу"""
    # PUT YOUR CODE HERE
    text = message.text.strip()
    if text.startswith("www."):
        text = "https://" + text
    is_valid = validators.url(text)
    if not is_valid:
        new = bot.send_message(message.chat.id, "Введенная ссылка некорректна, попробуйте еще раз")
        bot.register_next_step_handler(new, add_new_subject_url)
        return
    table_data = access_current_sheet()
    ws = table_data[0]
    df = table_data[2]
    ws.update_cell(df.shape[0] + 1, 2, text)
    bot.send_message(message.chat.id, "Предмет добавлен")
    sleep(2)
    start(message)


def update_subject(message):
    """ Обновляем информацию о предмете в Google-таблице """
    worksheet, url, df = access_current_sheet()
    subject_row = df[df["Предмет"] == message.text]
    if len(subject_row) == 0:
        bot.send_message(message.chat.id, "Предмет не найден, попробуйте еще раз.")
        sleep(2)
        start(message)
        return
    new_subject = bot.send_message(message.chat.id, "Введите новое название предмета:")
    bot.register_next_step_handler(new_subject, lambda m: update_subject_name(m))


def update_subject_name(message):
    """ Обновляем название предмета в Google-таблице """
    table_data = access_current_sheet()
    ws = table_data[0]
    global ROW, COL
    cell = ws.find(message.text)
    ROW = cell.row
    COL = cell.col
    new = bot.send_message(message.chat.id, "Введите новое название")
    bot.register_next_step_handler(new, update_cell_data, new.text)


def update_subject_url(message):
    table_data = access_current_sheet()
    ws = table_data[0]
    global ROW, COL
    cell = ws.find(message.text)
    ROW = cell.row
    COL = cell.col + 1
    new = bot.send_message(message.chat.id, "Введите новую ссылку")
    bot.register_next_step_handler(new, update_cell_data, new.text)


def update_cell_data(message, action):
    if action == "Введите новую ссылку" or action == "Введенная ссылка некорректна, попробуйте еще раз":
        text = ("https://" + message.text if (len(message.text) > 3 and message.text[:4] == "www.") else message.text)
        is_valid = validators.url(text)
        if not is_valid:
            new = bot.send_message(message.chat.id, "Введенная ссылка некорректна, попробуйте еще раз")
            bot.register_next_step_handler(new, update_cell_data, new.text)
            return
        message.text = text
    global ROW, COL
    table_data = access_current_sheet()
    ws = table_data[0]
    ws.update_cell(ROW, COL, message.text)
    bot.send_message(message.chat.id, "Готово!")
    sleep(2)
    start(message)


def delete_subject(message):
    """Удаляем предмет в Google-таблице"""
    # PUT YOUR CODE HERE
    table_data = access_current_sheet()
    ws = table_data[0]
    cell = ws.find(message.text)
    ws.delete_rows(cell.row)
    bot.send_message(message.chat.id, "Удалено!")
    sleep(2)
    start(message)


def clear_subject_list(message):
    """Удаляем все из Google-таблицы"""
    # PUT YOUR CODE HERE
    table_data = access_current_sheet()
    ws = table_data[0]
    ws.clear()
    bot.send_message(message.chat.id, "Информация из таблицы удалена!")
    sleep(2)
    start(message)


@bot.message_handler(commands=["start"])
def octobot(message):
    bot.send_message(message.chat.id, "Привет, я 0ct0bot! Теперь я буду помнить все твои дедлайны")
    table_data = access_current_sheet()
    if table_data:
        df = table_data[2]
        bot.send_message(message.chat.id, "Доступные предметы")
        for i in range(df.shape[0]):
            bot.send_message(message.chat.id, f"<a href='{df.at[i, 'Link']}'> {df.at[i, 'Subject']} </a>", parse_mode="HTML", disable_web_page_preview=True, )
    start(message)


def start(message):
    table_data = access_current_sheet()
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if not table_data:
        start_markup.row("Подключить Google-таблицу")
    else:
        start_markup.row("Посмотреть дедлайны на этой неделе")
        start_markup.row("Редактировать дедлайн")
        start_markup.row("Редактировать предметы")
    info = bot.send_message(message.chat.id, "Что хотите сделать?", reply_markup=start_markup)
    bot.register_next_step_handler(info, choose_action)


bot.infinity_polling()
