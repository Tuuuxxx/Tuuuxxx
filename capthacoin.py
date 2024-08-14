import sqlite3
import telebot
from telebot import types
import random
from captcha.image import ImageCaptcha
from db import Database

db = Database('database.db')


bot = telebot.TeleBot('7362609291:AAHjVotsLwoTWfmubHqpqH916hqBULBUTEw')

def captcha(message):
        bot.delete_message(message.chat.id, message.message_id-1)
        sym = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        image = ImageCaptcha(width=800, height=400, fonts =['arial_bolditalicmt.ttf'], font_sizes=[200])
        global ans
        ans = random.choices(sym, k=4)
        image.write(ans, 'captcha.png')
        file = open('./captcha.png', 'rb')
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("Профиль")
        btn2 = types.KeyboardButton("В меню")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_photo(message.chat.id, file, 'Решите капчу', reply_markup=markup)
        bot.delete_message(message.chat.id, message.message_id)
        bot.register_next_step_handler(message, check)

cards = {
    '🂱': 11, '🂲': 2, '🂳': 3, '🂴': 4, '🂵': 5, '🂶': 6, '🂷': 7, '🂸': 8, '🂹': 9, '🂺': 10,
    '🂻': 10, '🂼': 10, '🂽': 10, '🂾': 10, '🂡': 11, '🂢': 2, '🂣': 3, '🂤': 4, '🂥': 5, '🂦': 6,
    '🂧': 7, '🂨': 8, '🂩': 9, '🂪': 10, '🂫': 10, '🂬': 10, '🂭': 10, '🂮': 10, '🃁': 11, '🃂': 2,
    '🃃': 3, '🃄': 4, '🃅': 5, '🃆': 6, '🃇': 7, '🃈': 8, '🃉': 9, '🃊': 10, '🃋': 10, '🃌': 10,
    '🃍': 10, '🃎': 10, '🃑': 11, '🃒': 2, '🃓': 3, '🃔': 4, '🃕': 5, '🃖': 6, '🃗': 7, '🃘': 8,
    '🃙': 9, '🃚': 10, '🃛': 10, '🃜': 10, '🃝': 10
}
playerHand = []
dealerHand = []

PlayerTotal = 0
DealerTotal = 0

def DealerdealCard():
    global DealerTotal
    card = random.choice(list(cards.items()))
    dealerHand.append(card[0])
    DealerTotal+=card[1]
    cards.pop(card[0])

def PlayerdealCard():
    global PlayerTotal
    card = random.choice(list(cards.items()))
    playerHand.append(card[0])
    PlayerTotal+=card[1]
    cards.pop(card[0])

def revealDealerHand():
    if len(dealerHand) == 2:
        return dealerHand[0]
    elif len(dealerHand) > 2:
        return dealerHand[0], dealerHand[1]

@bot.message_handler(commands=['start'])
def start(message):
    if not db.user_exists(message.from_user.id):
        referrer_id = str(message.text[7:])
        if referrer_id != "":
            if str(referrer_id) != str(message.from_user.id):
                db.add_user(message.from_user.id, referrer_id)
                try:
                    bot.send_message(referrer_id, 'Новый пользователь перешёл по вашей реферальной ссылке!')
                except:
                    pass
            else:
                db.add_user(message.from_user.id)
                bot.send_message(message.chat.id, 'Нельзя регестрироваться по своей реферальной ссылке!')
        else:
            db.add_user(message.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton("Профиль")
    btn2 = types.KeyboardButton("Решать капчи")
    markup.row(btn1, btn2)
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}, Теперь ты работник офиса CaptchaCoin, Ты должен решать капчи и получать за это валюту, Вскоре будет листинг, так что успей заполучить CaptchaCoin до него', reply_markup=markup)
    bot.register_next_step_handler(message, menu)
def check(message):
    global ans
    if message.text == ''.join(ans):
        try:
            captcha(message)
            db.add_coin(message.from_user.id, 5)
        except: pass
    else:
        menu(message)

        
def menu(message):
    if message.text == 'Профиль':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("В меню")
        markup.add(btn1)
        bot.send_message(message.chat.id, f'Имя: {message.from_user.first_name}\nСсылка для приглашения: https://t.me/CaptchaCoinBot?start={message.from_user.id}\nCaptchaCoin: {db.view_balance(message.from_user.id)}', reply_markup=markup)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.register_next_step_handler(message, menu)
    elif message.text == 'В меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Профиль")
        btn2 = types.KeyboardButton("Решать капчи")
        btn3 = types.KeyboardButton("Казино")
        markup.add(btn3)
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, 'Меню\nПоговаривают что если подписаться на канал то начислится 500 койнов\nТы должен решать капчи и получать за это валюту, Вскоре будет листинг, так что успей заполучить CaptchaCoin до него', reply_markup=markup)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.register_next_step_handler(message, menu)
    elif message.text == 'Решать капчи':
        sym = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
        image = ImageCaptcha(width=800, height=400, fonts =['arial_bolditalicmt.ttf'], font_sizes=[200])
        global ans
        ans = random.choices(sym, k=4)
        image.write(ans, 'captcha.png')
        file = open('./captcha.png', 'rb')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Профиль")
        btn2 = types.KeyboardButton("В меню")
        markup.add(btn1)
        markup.add(btn2)
        bot.send_photo(message.chat.id, file, 'Решите капчу', reply_markup=markup)
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.register_next_step_handler(message, check)


 
    elif message.text == 'Казино':
        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id-1)
        global PlayerTotal
        global DealerTotal
        for _ in range(2):
            DealerdealCard()
            PlayerdealCard()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("Hit")
        btn2 =types.KeyboardButton("Stay")
        markup.row(btn1, btn2)
        bot.send_message(message.chat.id, f'Добро пожаловать в Блэк Джэк! Правила стандартные. Ставка всегда 10 CaptchaCoin\nУдачной игры\nКарты дилера: {revealDealerHand()} и  🂠\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
        bot.register_next_step_handler(message, blackjack)
def blackjack(message):
    global PlayerTotal
    global DealerTotal
    playerHand.clear()
    dealerHand.clear()
    DealerTotal = 0
    PlayerTotal = 0
    if message.text == 'Stay':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton("В меню")
        markup.add(btn1)

        while DealerTotal < 16:
            DealerdealCard()
        if DealerTotal > 21 and PlayerTotal > 21:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, f'Ничья! Как так?\nКарты дилера: {revealDealerHand()}Счёт дилера: {DealerTotal}\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
            playerHand.clear()
            dealerHand.clear()
            DealerTotal = 0
            PlayerTotal = 0
        elif DealerTotal > PlayerTotal and DealerTotal <= 21:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, f'Ты проиграл.\nКарты дилера: {revealDealerHand()}Счёт дилера: {DealerTotal}\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
            playerHand.clear()
            dealerHand.clear()
            DealerTotal = 0
            PlayerTotal = 0
        elif PlayerTotal > DealerTotal and PlayerTotal <= 21:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, f'Ты победил!\nКарты дилера: {revealDealerHand()}Счёт дилера: {DealerTotal}\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
            playerHand.clear()
            dealerHand.clear()
            DealerTotal = 0
            PlayerTotal = 0
        elif PlayerTotal == DealerTotal:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            bot.send_message(message.chat.id, f'Ничья! Как так?\nКарты дилера: {revealDealerHand()}Счёт дилера: {DealerTotal}\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
            playerHand.clear()
            dealerHand.clear()
            DealerTotal = 0
            PlayerTotal = 0

        bot.register_next_step_handler(message, menu)

    elif message.text == 'Hit':
        markup = types.ReplyKeyboardMarkup()
        btn1 = types.KeyboardButton("Hit")
        btn2 =types.KeyboardButton("Stay")
        markup.row(btn1, btn2)
        if PlayerTotal > 21:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            markup = types.ReplyKeyboardMarkup()
            btn1 =types.KeyboardButton("В меню")
            markup.add(btn1)
            bot.send_message(message.chat.id, f'Ты проиграл.\nКарты дилера: {revealDealerHand()}Счёт дилера: {DealerTotal}\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
            playerHand.clear()
            dealerHand.clear()
            DealerTotal = 0
            PlayerTotal = 0
            bot.register_next_step_handler(message, menu)
        else:
            bot.delete_message(message.chat.id, message.message_id)
            bot.delete_message(message.chat.id, message.message_id-1)
            PlayerdealCard()
            bot.send_message(message.chat.id, f'Карты дилера: {revealDealerHand()}Счёт дилера: {DealerTotal}\nТвои карты: {playerHand} и твой счёт составляет {PlayerTotal}', reply_markup=markup)
        bot.register_next_step_handler(message, blackjack)









bot.polling(none_stop=True)