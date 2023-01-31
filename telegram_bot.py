import telebot
from telebot import types
import parsing_functions as PA
token='6118639062:AAEo1Y_t4ThlBI9n_ZzxQrC_mjVLNV0kWf0'
bot=telebot.TeleBot(token)

all_articles=''
all_parsed_artics=''
kb1=types.ReplyKeyboardMarkup(resize_keyboard=True)
but1=types.KeyboardButton('Да')
but2=types.KeyboardButton('Quit')
but0=types.KeyboardButton('Описание')
but6=types.KeyboardButton('Фото')
kb0=types.ReplyKeyboardMarkup(resize_keyboard=True)
kb0.add(but1,but2,but6)
kb1.add(but1,but2,but0)

kb9=types.ReplyKeyboardMarkup(resize_keyboard=True)
kb9.add(but0,but6,but2)

kbQ=types.ReplyKeyboardMarkup(resize_keyboard=True)
kbQ.add(types.KeyboardButton('Quit'))

kb2=types.ReplyKeyboardMarkup(resize_keyboard=True)
but3=types.KeyboardButton('Описание')
but4=types.KeyboardButton('Фото')
kb2.add(but3,but4)

# @bot.message_handler(commands=['get_info','info'])
def get_user_info():
    marks_inline=types.InlineKeyboardMarkup()
    item_description=types.InlineKeyboardButton(text='Подробнее',callback_data='description')
    marks_inline.add(item_description)
    return marks_inline

# kb=get_user_info()

# @bot.callback_query_handler(func=lambda call:True)
# def answer(call):
#     if call.data == 'description':
#         get


@bot.message_handler(commands=['start'])
def starting(message):
    bot.send_message(message.chat.id,'Привет\nЭто парсер сайта "kaktus.media"(раздел популярные сегодня)',reply_markup=types.ReplyKeyboardRemove())

    global all_articles
    global all_parsed_artics
    all_articles=PA.findArticles(PA.getHtml(PA.BASE_URL))
    all_parsed_artics=PA.parseArticles(all_articles)
    var2=all_parsed_artics   ###     <TUPLE>    ( [0]-LIST-NAMES    [1]-LIST-LINKS    [2]-LIST-VIEWS     [3]-LIST-IMAGES )
    for x in range(0,len(all_articles)-1):
        msg1=bot.send_photo(message.chat.id,var2[3][x],caption=f'№{x+1}\n{var2[0][x]}\nПросмотров: {var2[2][x]}\n\n{var2[1][x]}')
    
        

    var1=bot.send_message(message.chat.id,'Напишите номер статьи, которой хотите посмотреть...',reply_markup=kbQ)
    bot.register_next_step_handler(var1,clarifyInfo)

def clarifyInfo(message):
        # var1=PA.findArticles(PA.getHtml(PA.BASE_URL))
        global all_articles
        global all_parsed_artics
        try:
            var2=int(message.text)-1
            if not var2+1>len(all_articles) and var2+1>0:
                bot.send_photo(message.chat.id,all_parsed_artics[3][var2],caption=f'№{var2+1}\n{all_parsed_artics[0][var2]}\nПросмотров: {all_parsed_artics[2][var2]}\n\n{all_parsed_artics[1][var2]}',reply_markup=types.ReplyKeyboardRemove())
                var5=bot.send_message(message.chat.id,'Что хотите посмотреть?',reply_markup=kb9)
                bot.register_next_step_handler(var5,more,var2)

                # var3=PA.getDetails(all_parsed_artics[1][var2-1])
            else:
                msg2=bot.send_message(message.chat.id,f'Число должно быть от 1 до {len(all_articles)-1}',reply_markup=kbQ)
                bot.register_next_step_handler(msg2,clarifyInfo)
        except ValueError:
            if not message.text=='Quit':
                msg1=bot.send_message(message.chat.id,'Неправильное число!',reply_markup=kbQ)
                bot.register_next_step_handler(msg1,clarifyInfo)
            else:
                bot.send_message(message.chat.id,'До свидания',reply_markup=types.ReplyKeyboardRemove())
        

def details(message,number_of_article):
    global all_parsed_artics
    getphoto=PA.getPhoto(all_parsed_artics[1][number_of_article])
    if message.text == 'Фото':
        try:
            if type(all_parsed_artics[3][number_of_article])==type(list):
                for x in getphoto:
                    bot.send_photo(message.chat.id,x,reply_markup=types.ReplyKeyboardRemove())
            else:
                if getphoto:
                    bot.send_photo(message.chat.id,getphoto,reply_markup=types.ReplyKeyboardRemove())
                else:
                    bot.send_message(message.chat.id,'Фото нет!',reply_markup=types.ReplyKeyboardRemove())
            var4=bot.send_message(message.chat.id,'Сначала?',reply_markup=kb1)
            bot.register_next_step_handler(var4,more,number_of_article)
        except:
            bot.send_message(message.chat.id,'Вложенных фото нет!')
            var4=bot.send_message(message.chat.id,'Сначала?',reply_markup=kb1)
            bot.register_next_step_handler(var4,more,number_of_article)

    elif message.text == 'Описание':
        var3=PA.getDetails(all_parsed_artics[1][number_of_article])
        if len(var3)>4095:
            bot.send_message(message.chat.id,var3,reply_markup=types.ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id,'Описание слишком длинное! Не покажу)))')
        var4=bot.send_message(message.chat.id,'Сначала?',reply_markup=kb0)
        bot.register_next_step_handler(var4,more,number_of_article)
    else:
        var6=bot.send_message(message.chat.id,'Не понял')
        bot.register_next_step_handler(var6,details)


def more(message,number_art):
    if message.text == 'Да':
        var1=bot.send_message(message.chat.id,'Введите номер статьи...')
        bot.register_next_step_handler(var1,clarifyInfo)
    elif message.text == 'Quit':
        bot.send_message(message.chat.id,'До свидания',reply_markup=types.ReplyKeyboardRemove())
    elif message.text == 'Описание':
        details(message,number_art)
    elif message.text == 'Фото':
        details(message,number_art)
    else:
        bot.send_message(message.chat.id,'Не понял')
        bot.register_next_step_handler(message,more,number_art)


# def neTo(message,number_art):
#     if message.text !=







if __name__=='__main__':
    bot.polling(none_stop=True, interval=0)