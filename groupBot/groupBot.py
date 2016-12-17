#-*. coding: utf-8 -*-
import time
import telepot
import threading
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from Queue import Queue


# Esta lista guarda los chat_id de los que entran como alumnos al bot
users = []
# Aquí guardo el chat_id del administrador cuando este acceda por primera vez al bot
global admin
admin = 0
# La clave que pide el bot si entras como administrador o como usuario
claveAdmin = 1720
claveUser = 3411

buzon = []

# Los diferentes teclados que va a usar el bot

keyboardLogin = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Alumno', callback_data='alumno'),
                   InlineKeyboardButton(text='Profesor', callback_data='profesor')],
               ])
keyboardUser = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Enviar mensaje al profesor.', callback_data='msg_user')],
               ])

keyboardAdminMsg = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Enviar mensaje al grupo.', callback_data='difusion')],
                   [InlineKeyboardButton(text='Hacer una encuesta.', callback_data='encuesta')],
                   [InlineKeyboardButton(text='Ver siguiente mensaje del buzón.', callback_data='msg_buzon')],
               ])
keyboardAdminSinMsg = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Enviar mensaje al grupo.', callback_data='difusion')],
                   [InlineKeyboardButton(text='Hacer una encuesta.', callback_data='encuesta')],
               ])

# Bot que organiza interacciones entre un administrador y los usuarios que se añadan.
# Estas interacciones serán: hacer llegar a los usuarios los mensajes que ponga el administrador
# a través del bot, hacer llegar encuestas que pueda crear el administrador con el bot y 
# hacer llegar sugerencias de manera anónima de los alumnos a un buzón que podrá ver el administrador
 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)   
    
    if content_type == 'text':
     if msg['text'] == '/start':
      bot.sendMessage(chat_id, 'Bienvenido al bot de ELP. ¿Eres un alumno o el profesor?', reply_markup=keyboardLogin)
     elif msg['text'] == claveAdmin or chat_id == admin and msg['text'] == 'mostrar':
      if msg['text'] == claveAdmin:
       admin = chat_id
      if len(buzon) == 0: # Si no tiene mensajes
       bot.sendMessage(chat_id, 'Bienvenido, no tiene mensajes en el buzón. ¿Qué desea hacer?', reply_markup=keyboardAdminSinMsg)
      else:
       n = len(buzon)
       bot.sendMessage(chat_id, txtMensajes(n) + '¿Qué desea hacer?', reply_markup=keyboardAdminMsg)
     elif msg['text'] == claveUser and not chat_id in users:
      bot.sendMessage(chat_id, 'Clave correcta. Bienvenido al bot de ELP. Cuando el profesor envíe algo yo te lo haré llegar. Si tienes algún mensaje para el profesor o alguna sugerencia, puedo hacérselo llegar si pulsas el botón de abajo.', reply_markup=keyboardUser)

# Los mensajes que mando a cada hilo tienen formato de lista, con el primer elemento siendo
# el nombre de cada tipo de mensaje, y el resto de campos los datos que le hagan falta
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    
    if query_data == 'alumno':
      bot.answerCallbackQuery(query_id, text='Introduzca el código de los alumnos.')
    elif query_data == 'profesor':
      bot.answerCallbackQuery(query_id, text='Introduzca el código del profesor.')

# Para diferenciar el texto que muestro
def txtMensajes(n):
	if n == 1:
		txt = 'Tiene un mensaje. '
	else:
		txt = 'Tiene ' + str(n) + ' mensajes. '
	return txt

# Token del bot devuelto por botFather
TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.Bot(TOKEN)
# Definir así el message_loop hace que redirija los mensajes de texto a on_chat_message y
# los callback_query generados por el teclado del bot a on_callback_query
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
print ('Listening ...')

# Tiempo de espera para comprobar nuevos mensajes
while 1:
    time.sleep(10)
