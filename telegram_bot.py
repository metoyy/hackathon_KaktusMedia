import telebot
from telebot import types
import parsing_functions as PA
token='6118639062:AAEo1Y_t4ThlBI9n_ZzxQrC_mjVLNV0kWf0'
bot=telebot.TeleBot(token)
all_articles=''
all_parsed_artics=''
but1=types.KeyboardButton('Другая статья')
but2=types.KeyboardButton('Quit')
but3=types.KeyboardButton('Описание')
but4=types.KeyboardButton('Фото')
but7=types.KeyboardButton('Видео')
but8=types.KeyboardButton('Обновить')
but9=types.KeyboardButton('Новости коротко')

kb9=types.ReplyKeyboardMarkup(resize_keyboard=True)
kb9.add(but3,but4,but7,but1,but8,but2)

kbQ=types.ReplyKeyboardMarkup(resize_keyboard=True)
kbQ.add(but9,but8,but2)

kbStart=types.ReplyKeyboardMarkup(resize_keyboard=True)
butStart=types.KeyboardButton('/start')
kbStart.add(butStart)

question='Дальше?...'




@bot.message_handler(commands=['start'])
def starting(message):
    bot.send_message(message.chat.id,'Привет\nЭто парсер сайта "kaktus.media"(раздел популярные сегодня)',reply_markup=types.ReplyKeyboardRemove())

    global all_articles
    global all_parsed_artics
    all_articles=PA.findArticles(PA.getHtml(PA.BASE_URL))
    all_parsed_artics=PA.parseArticles(all_articles)
    var2=all_parsed_artics   ###     <TUPLE>    ( [0]-LIST-NAMES    [1]-LIST-LINKS    [2]-LIST-VIEWS     [3]-LIST-IMAGES )
    for x in range(0,len(all_articles)):
        msg1=bot.send_photo(message.chat.id,var2[3][x],caption=f'№{x+1}\n{var2[0][x]}\nПросмотров: {var2[2][x]}\n\n{var2[1][x]}')
    var1=bot.send_message(message.chat.id,'Напишите номер статьи, которой хотите посмотреть...',reply_markup=kbQ)
    bot.register_next_step_handler(var1,clarifyInfo)


@bot.message_handler(commands=['stop'])
def stop(message):
    bot.send_message(message.chat.id,'До свидания!\nЧтобы запустить бота снова,\nнапишите /start',reply_markup=kbStart)


def shortCheck(message):
    showtext=''
    i=1
    for u in all_parsed_artics[0]:
        var3=f'№{i}: {u}\n'
        showtext=showtext+''.join(var3)
        i+=1
    bot.send_message(message.chat.id,showtext)
    var4=bot.send_message(message.chat.id,'Введите номер статьи...',reply_markup=kbQ)
    bot.register_next_step_handler(var4,clarifyInfo)


def clarifyInfo(message):
        # var1=PA.findArticles(PA.getHtml(PA.BASE_URL))
        global all_articles
        global all_parsed_artics
        if message.text=='Новости коротко':
            shortCheck(message)
        else:
            try:
                var2=int(message.text)-1
                if not var2+1>len(all_articles) and var2+1>0:
                    bot.send_photo(message.chat.id,all_parsed_artics[3][var2],caption=f'№{var2+1}\n{all_parsed_artics[0][var2]}\nПросмотров: {all_parsed_artics[2][var2]}\n\n{all_parsed_artics[1][var2]}',reply_markup=types.ReplyKeyboardRemove())
                    var5=bot.send_message(message.chat.id,'Что хотите посмотреть?',reply_markup=kb9)
                    bot.register_next_step_handler(var5,more,var2)
                else:
                    msg2=bot.send_message(message.chat.id,f'Число должно быть от 1 до {len(all_articles)-1}',reply_markup=kbQ)
                    bot.register_next_step_handler(msg2,clarifyInfo)
            except ValueError:
                if message.text=='Обновить':
                    starting(message)    
                elif not message.text=='Quit':
                    msg1=bot.send_message(message.chat.id,'Неправильное число!',reply_markup=kbQ)
                    bot.register_next_step_handler(msg1,clarifyInfo)
                else:
                    stop(message)
        

def details(message,number_of_article):
    global all_parsed_artics
    getphoto=PA.getPhoto(all_parsed_artics[1][number_of_article])
    if message.text == 'Фото':
        try:
            if getphoto:
                if type(getphoto)==type(list()):
                    for x in getphoto:
                        bot.send_photo(message.chat.id,x,reply_markup=types.ReplyKeyboardRemove())
                elif type(getphoto)==type(str()):
                    bot.send_photo(message.chat.id,getphoto,reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(message.chat.id,'Фото нет!',reply_markup=types.ReplyKeyboardRemove())
            var4=bot.send_message(message.chat.id,question,reply_markup=kb9)
            bot.register_next_step_handler(var4,more,number_of_article)
        except KeyboardInterrupt:
            bot.send_message(message.chat.id,'Вложенных фото нет!')
            var4=bot.send_message(message.chat.id,question,reply_markup=kb9)
            bot.register_next_step_handler(var4,more,number_of_article)

    elif message.text == 'Описание':
        var3=PA.getDetails(all_parsed_artics[1][number_of_article])
        if len(var3)>4095:
            if len(var3)>4095*2:
                bot.send_message(message.chat.id,'Описание слишком длинное! Не покажу)))')
            var7=var3[0:4095]
            var8=var3[4095:]
            bot.send_message(message.chat.id,var7)            
            bot.send_message(message.chat.id,var8)
        else:
            bot.send_message(message.chat.id,var3,reply_markup=types.ReplyKeyboardRemove())            
        var4=bot.send_message(message.chat.id,question,reply_markup=kb9)
        bot.register_next_step_handler(var4,more,number_of_article)
    elif message.text == 'Видео':
        var9=PA.getVideo(all_parsed_artics[1][number_of_article])
        if var9:
            for x in var9:
                bot.send_message(message.chat.id,x)
            var10=bot.send_message(message.chat.id,question,reply_markup=kb9)
            bot.register_next_step_handler(message,more,number_of_article)

        else:
            var10=bot.send_message(message.chat.id,'Видео нет!',reply_markup=kb9)
            bot.register_next_step_handler(message,more,number_of_article)
    else:
        var6=bot.send_message(message.chat.id,'Не понял')
        bot.register_next_step_handler(var6,details)



def more(message,number_art):
    if message.text == 'Другая статья':
        var1=bot.send_message(message.chat.id,'Введите номер статьи...',reply_markup=kbQ)
        bot.register_next_step_handler(var1,clarifyInfo)
    elif message.text == 'Quit':
        stop(message)
    elif message.text == 'Описание':
        details(message,number_art)
    elif message.text == 'Фото':
        details(message,number_art)
    elif message.text == 'Видео':
        details(message,number_art)
    elif message.text == 'Обновить':
        starting(message)
    else:
        bot.send_message(message.chat.id,'Не понял')
        bot.register_next_step_handler(message,more,number_art)





if __name__=='__main__':
    bot.polling(none_stop=True)