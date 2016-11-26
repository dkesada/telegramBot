#-*. coding: utf-8 -*-
# David Quesada López
import time
import telepot
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

# La idea inicial de este bot era hacer algo relacionado con cartas, para lo que
# he hecho un pack de stickers de telegram en el que pensaba poner toda una baraja.
# Hice pruebas para ver cómo funciona un bot con los stickers, pero me di cuenta
# que no se pueden mandar más de 1 sticker al mismo tiempo, lo que reduce gravemente
# su utilidad a la hora de jugar a algo que no sea que el bot te de una carta aleatoria.

# Al parecer, los bots de juegos de cartas en telegram usan los 4 iconos que representan
# los palos de la baraja francesa y un número, estilo 4♠, lo que da mucho más juego al
# ser un caracter que se puede meter en botones con facilidad.

# Al final el bot ha quedado en que te rebota los sticker que le mandes y si le pides
# el comando /oro te manda la única carta triste que he puesto en mi pack de stickers.
# Al menos lo de hacer tus propios stickers es interesante, y parece que su uso por el bot
# es bastante sencillo.

oro = 'BQADBAADBAADyRUkD9PLEbHKwOTFAg' # Este es el id de la única carta que he puesto en el pack de stickers
 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)   
    print(content_type)
    if content_type == 'text': # Si me mandan texto
     if msg['text'] == '/oro':
      bot.sendSticker(chat_id, oro)
     else: 
      bot.sendMessage(chat_id, 'Mándame un sticker y te lo mando de vuelta, o pídeme el /oro')
    elif content_type == 'sticker': # Si me mandan un sticker
     sticker_id = msg['sticker']['file_id']
     print(sticker_id)
     bot.sendSticker(chat_id, sticker_id)

TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)
print ('Listening ...')

while 1:
    time.sleep(10)
