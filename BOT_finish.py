import telebot
from telebot import types
import time
import sqlite3
import random

bot = telebot.TeleBot("2066162532:AAF4ee60LQolUFScthSg1ld9-Lo2TM_24yE")

plus = True

connect = sqlite3.connect('players.db')
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS players(
            i INTEGER,
            id_user INTEGER,
            name TEXT,
            mafia1 INTEGER,
            mafia2 INTEGER,
            donmaf INTEGER,
            slut INTEGER,
            doctor INTEGER,
            citizen INTEGER,
            sherif INTEGER,
            maniac INTEGER,
            chat_id INTEGER
        )
        """)

@bot.message_handler(commands=['start'])
def Start(message):
    if plus:
        connect = sqlite3.connect('players.db')
        cursor = connect.cursor()
        chatid = message.chat.id
        cursor.execute(f"DELETE FROM players WHERE chat_id = {chatid}")
        connect.commit()
        keyboard = types.InlineKeyboardMarkup()
        key_ru = types.InlineKeyboardButton(text='Да', callback_data='Yes')
        key_eng = types.InlineKeyboardButton(text='Не', callback_data='No')
        keyboard.add(key_ru, key_eng)
        bot.send_message(message.chat.id, text="Вы хотите поиграть?☠", reply_markup=keyboard)

@bot.callback_query_handler(func= lambda call: True)
def callback_warker(call):
    global zn, roll_numer, mafia
    global x, btn, ru, eng, players, roll, i, num, MinTeam, MiddleTeam, BigTeam, LargeTeam
    if call.data == "Yes":
        i = 0
        x = 0
        num = 0
        btn = True
        ru = False
        eng = True
        players = str(':\n')
        keyboard_plus = types.InlineKeyboardMarkup()
        key_plus = types.InlineKeyboardButton(str("+"), callback_data="plus")
        key_play = types.InlineKeyboardButton(str("END"), callback_data="play")
        keyboard_plus.add(key_plus)
        keyboard_plus.add(key_play)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Who wanna play?", reply_markup= keyboard_plus)
    if call.data == "No":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id= call.message.message_id , text = "🗿")
    if call.data == "plus" and plus is True:
        connect = sqlite3.connect('players.db')
        cursor = connect.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS players(
            i INTEGER,
            id_user INTEGER,
            name TEXT,
            mafia1 INTEGER,
            mafia2 INTEGER,
            donmaf INTEGER,
            slut INTEGER,
            doctor INTEGER,
            citizen INTEGER,
            sherif INTEGER,
            maniac INTEGER,
            chat_id INTEGER
        )
        """)
        connect.commit()
        people_id = call.from_user.id
        cursor.execute(f"SELECT id_user FROM players WHERE id_user = {people_id}")
        data = cursor.fetchone()
        if data is None:

            i += 1

            users_list = [i, call.from_user.id, call.from_user.first_name, 2, 2, 2, 2, 2, 2, 2, 2, call.message.chat.id]
            players_name = call.from_user.first_name
            cursor.executemany("INSERT INTO players(i, id_user, name, mafia1, mafia2, donmaf, slut, doctor, citizen, sherif, maniac, chat_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (users_list,))
            connect.commit()

            x += 1

            keyboard_plus = types.InlineKeyboardMarkup()
            key_plus = types.InlineKeyboardButton(str("+"), callback_data="plus")
            key_play = types.InlineKeyboardButton(str("END"), callback_data="play")
            keyboard_plus.add(key_plus)
            keyboard_plus.add(key_play)
            players = players + str(players_name) + '\n'
            if ru is True:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Кто хочет играть?. " + str(int(x)), reply_markup=keyboard_plus)
            elif eng is True:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Who wanna play?. " + str(int(x)), reply_markup=keyboard_plus)
        else:
            if btn:
                btn = False
                keyboard_plus = types.InlineKeyboardMarkup()
                key_plus = types.InlineKeyboardButton(str("+"), callback_data="plus")
                key_play = types.InlineKeyboardButton(str("END"), callback_data="play")
                keyboard_plus.add(key_plus)
                keyboard_plus.add(key_play)
                if ru == True:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="Не нажимайте кноку больше одного раза")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="Кто хочет играть?.. " + str(int(x)), reply_markup=keyboard_plus)
                elif eng == True:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="Dont touch the button more then once time")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Who wanna play?.. " + str(int(x)), reply_markup=keyboard_plus)
            elif btn is False:
                btn = True
                keyboard_plus = types.InlineKeyboardMarkup()
                key_plus = types.InlineKeyboardButton(str("+"), callback_data="plus")
                key_play = types.InlineKeyboardButton(str("END"), callback_data="play")
                keyboard_plus.add(key_plus)
                keyboard_plus.add(key_play)
                if ru is True:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="Не нажимайте кноку больше одного раза")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Кто хочет играть?... " + str(int(x)), reply_markup=keyboard_plus)
                elif eng is True:
                    bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                              text="Dont touch the button more then once time")
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                          text="Who wanna play?... " + str(int(x)), reply_markup=keyboard_plus)

    if call.data == "play":
        connect = sqlite3.connect('players.db')
        cursor = connect.cursor()

        i_list = []
        ch = 0
        MinTeam = False
        MiddleTeam = False
        BigTeam = False
        LargeTeam = False
        cursor.execute(f"SELECT i FROM players WHERE chat_id = {call.message.chat.id}")
        data = cursor.fetchall()

        for row in data:
            ch += 1
            i_list.append(row[0])

        if ch >= 3 and ch <= 7:
            MinTeam = True
            rand_mafia1 = random.choice(i_list)
            i_list.remove(rand_mafia1)
            rand_sherif = random.choice(i_list)
            i_list.remove(rand_sherif)

            roll_number = [1, rand_mafia1]
            cursor.executemany("UPDATE players SET mafia1 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_sherif]
            cursor.executemany("UPDATE players SET sherif = ? WHERE i = ?", (roll_number,))
            connect.commit()

            cursor.execute(f"SELECT i FROM players WHERE chat_id = {call.message.chat.id}")
            data = cursor.fetchall()

            for row in data:
                if row[0] in i_list:
                    roll_number = [1, row[0]]
                    cursor.executemany("UPDATE players SET citizen = ? WHERE i = ?", (roll_number,))
                    connect.commit()

            keyboard = types.InlineKeyboardMarkup()
            key_who = types.InlineKeyboardButton(text="check", callback_data="who")
            keyboard.add(key_who)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Набор игроков окончен!\n' 'Игроков (' + str(int(x)) + ')' + str(players), reply_markup=keyboard)

        if ch >7 and ch <= 10:
            MiddleTeam = True
            rand_mafia1 = random.choice(i_list)
            i_list.remove(rand_mafia1)
            rand_mafia2 = random.choice(i_list)
            i_list.remove(rand_mafia2)
            rand_sherif = random.choice(i_list)
            i_list.remove(rand_sherif)
            rand_doctor = random.choice(i_list)
            i_list.remove(rand_doctor)

            roll_number = [1, rand_mafia1]
            cursor.executemany("UPDATE players SET mafia1 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_mafia2]
            cursor.executemany("UPDATE players SET mafia2 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_sherif]
            cursor.executemany("UPDATE players SET sherif = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_doctor]
            cursor.executemany("UPDATE players SET doctor = ? WHERE i = ?", (roll_number,))
            connect.commit()

            cursor.execute(f"SELECT i FROM players WHERE chat_id = {call.message.chat.id}")
            data = cursor.fetchall()

            for row in data:
                if row[0] in i_list:
                    roll_number = [1, row[0]]
                    cursor.executemany("UPDATE players SET citizen = ? WHERE i = ?", (roll_number,))
                    connect.commit()

            keyboard = types.InlineKeyboardMarkup()
            key_who = types.InlineKeyboardButton(text="check", callback_data="who")
            keyboard.add(key_who)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Набор игроков окончен!\n' 'Игроков (' + str(int(x)) + ')' + str(players), reply_markup=keyboard)

        if ch > 10 and ch <= 15:
            BigTeam = True
            rand_mafia1 = random.choice(i_list)
            i_list.remove(rand_mafia1)
            rand_mafia2 = random.choice(i_list)
            i_list.remove(rand_mafia2)
            rand_sherif = random.choice(i_list)
            i_list.remove(rand_sherif)
            rand_doctor = random.choice(i_list)
            i_list.remove(rand_doctor)
            rand_slut = random.choice(i_list)
            i_list.remove(rand_slut)

            roll_number = [1, rand_mafia1]
            cursor.executemany("UPDATE players SET mafia1 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_mafia2]
            cursor.executemany("UPDATE players SET mafia2 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_sherif]
            cursor.executemany("UPDATE players SET sherif = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_doctor]
            cursor.executemany("UPDATE players SET doctor = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_slut]
            cursor.executemany("UPDATE players SET slut = ? WHERE i = ?", (roll_number,))
            connect.commit()

            cursor.execute(f"SELECT i FROM players WHERE chat_id = {call.message.chat.id}")
            data = cursor.fetchall()

            for row in data:
                if row[0] in i_list:
                    roll_number = [1, row[0]]
                    cursor.executemany("UPDATE players SET citizen = ? WHERE i = ?", (roll_number,))
                    connect.commit()

            keyboard = types.InlineKeyboardMarkup()
            key_who = types.InlineKeyboardButton(text="check", callback_data="who")
            keyboard.add(key_who)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Набор игроков окончен!\n' 'Игроков (' + str(int(x)) + ')' + str(players), reply_markup=keyboard)

        if ch > 15 and ch <= 25:
            LargeTeam = True
            rand_donmaf = random.choice(i_list)
            i_list.remove(rand_donmaf)
            rand_mafia1 = random.choice(i_list)
            i_list.remove(rand_mafia1)
            rand_mafia2 = random.choice(i_list)
            i_list.remove(rand_mafia2)
            rand_sherif = random.choice(i_list)
            i_list.remove(rand_sherif)
            rand_doctor = random.choice(i_list)
            i_list.remove(rand_doctor)
            rand_slut = random.choice(i_list)
            i_list.remove(rand_slut)
            rand_maniac = random.choice(i_list)
            i_list.remove(rand_maniac)

            roll_number = [1, rand_mafia1]
            cursor.executemany("UPDATE players SET mafia1 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_mafia2]
            cursor.executemany("UPDATE players SET mafia2 = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_sherif]
            cursor.executemany("UPDATE players SET sherif = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_doctor]
            cursor.executemany("UPDATE players SET doctor = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_slut]
            cursor.executemany("UPDATE players SET slut = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_donmaf]
            cursor.executemany("UPDATE players SET donmaf = ? WHERE i = ?", (roll_number,))
            connect.commit()

            roll_number = [1, rand_maniac]
            cursor.executemany("UPDATE players SET maniac = ? WHERE i = ?", (roll_number,))
            connect.commit()

            cursor.execute(f"SELECT i FROM players WHERE chat_id = {call.message.chat.id}")
            data = cursor.fetchall()

            for row in data:
                if row[0] in i_list:
                    roll_number = [1, row[0]]
                    cursor.executemany("UPDATE players SET citizen = ? WHERE i = ?", (roll_number,))
                    connect.commit()

            keyboard = types.InlineKeyboardMarkup()
            key_who = types.InlineKeyboardButton(text="check", callback_data="who")
            keyboard.add(key_who)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Набор игроков окончен!\n' 'Игроков (' + str(int(x)) + ')' + str(players), reply_markup=keyboard)

        if ch < 3 or ch > 25:
            bot.send_message(call.message.chat.id, text = 'U soooo bad...')

    if call.data == "who":
        connect = sqlite3.connect('players.db')
        cursor = connect.cursor()
        people = call.from_user.id

        if MinTeam:
            cursor.execute(f"SELECT mafia1 FROM players WHERE id_user = {people}")
            data_mafia1 = cursor.fetchone()
            if data_mafia1[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МАФИЯ")

            cursor.execute(f"SELECT sherif FROM players WHERE id_user = {people}")
            data_sherif = cursor.fetchone()
            if data_sherif[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ШЕРИФ")

            cursor.execute(f"SELECT citizen FROM players WHERE id_user = {people}")
            data_citizen = cursor.fetchone()
            if data_citizen[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МИРНЫЙ")

        if MiddleTeam:
            cursor.execute(f"SELECT mafia1 FROM players WHERE id_user = {people}")
            data_mafia1 = cursor.fetchone()
            if data_mafia1[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МАФИЯ")

            cursor.execute(f"SELECT mafia2 FROM players WHERE id_user = {people}")
            data_mafia2 = cursor.fetchone()
            if data_mafia2[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МАФИЯ")

            cursor.execute(f"SELECT slut FROM players WHERE id_user = {people}")
            data_slut = cursor.fetchone()
            if data_slut[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ШЛ#ХА")

            cursor.execute(f"SELECT doctor FROM players WHERE id_user = {people}")
            data_doctor = cursor.fetchone()
            if data_doctor[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ДОКТОР")

            cursor.execute(f"SELECT citizen FROM players WHERE id_user = {people}")
            data_citizen = cursor.fetchone()
            if data_citizen[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МИРНЫЙ")

        if LargeTeam:
            cursor.execute(f"SELECT mafia1 FROM players WHERE id_user = {people}")
            data_mafia1 = cursor.fetchone()
            if data_mafia1[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МАФИЯ")

            cursor.execute(f"SELECT mafia2 FROM players WHERE id_user = {people}")
            data_mafia2 = cursor.fetchone()
            if data_mafia2[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МАФИЯ")

            cursor.execute(f"SELECT slut FROM players WHERE id_user = {people}")
            data_slut = cursor.fetchone()
            if data_slut[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ШЛ#ХА")

            cursor.execute(f"SELECT doctor FROM players WHERE id_user = {people}")
            data_doctor = cursor.fetchone()
            if data_doctor[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ДОКТОР")

            cursor.execute(f"SELECT donmaf FROM players WHERE id_user = {people}")
            data_donmaf = cursor.fetchone()
            if data_donmaf[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="ДОН")

            cursor.execute(f"SELECT maniac FROM players WHERE id_user = {people}")
            data_maniac = cursor.fetchone()
            if data_maniac[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МАНЬЯК")

            cursor.execute(f"SELECT citizen FROM players WHERE id_user = {people}")
            data_citizen = cursor.fetchone()
            if data_citizen[0] == 1:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="МИРНЫЙ")


bot.polling()
