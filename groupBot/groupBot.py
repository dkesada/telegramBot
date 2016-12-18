#-*. coding: utf-8 -*-
import time
import telepot
import threading
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from Queue import Queue

###

# To do:
# Leer mensajes del buzon
# Enviar y contestar encuestas (creacion de encuestas ya hecha)
# Guardar en fichero users y admin[0] como copia de seguridad por si cae el bot
# Reset de los usuarios y el admin

###

# Esta lista guarda los chat_id de los que entran como alumnos al bot
users = []
# Aquí guardo el chat_id del administrador cuando este acceda por primera vez al bot
# En la segunda posicion hay un 0 si no está creando una encuesta o a 1 en caso contrario
admin = [0,0]
# La clave que pide el bot si entras como administrador o como usuario
claveAdmin = '1720'
claveUser = '3411'
# Lista con los usuarios que están enviando un mensaje
senders = []
buzon = []
enc = []

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
keyboardMensaje = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Cancelar', callback_data='cancelar')],
               ])
keyboardCrearEncuesta = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Aceptar', callback_data='cancelar')],
                   [InlineKeyboardButton(text='Cancelar', callback_data='cancelar')],
               ])

# Función que crea un teclado personalizado para realizar una encuesta a los integrantes del 
# grupo. El primer parámetro es el texto del mensaje que se enviará con la encuesta, el segundo
# argumento son las opciones a elegir en la encuesta separados por comas
def encuesta(opciones):
 listado = opciones.split(';') # Opciones separadas por comas
 texto = listado.pop(0)
 botones = []
 n = 0
 
 for i in listado:
  if i[0] == ' ':
   i = i[1:]
  botones.append([InlineKeyboardButton(text=i, callback_data='opcion' + str(n))])
  n = n+1;
  
 botones.append([InlineKeyboardButton(text='(Aspecto correcto, crear encuesta.)', callback_data='enviarEnc')])
 botones.append([InlineKeyboardButton(text='(Aspecto incorrecto, rehacer encuesta.)', callback_data='encuesta')])
 botones.append([InlineKeyboardButton(text='(Cancelar)', callback_data='cancelar')])
  
 return [texto, InlineKeyboardMarkup(inline_keyboard = botones)]

# Bot que organiza interacciones entre un administrador y los usuarios que se añadan.
# Estas interacciones serán: hacer llegar a los usuarios los mensajes que ponga el administrador
# a través del bot, hacer llegar encuestas que pueda crear el administrador con el bot y 
# hacer llegar sugerencias de manera anónima de los alumnos a un buzón que podrá ver el administrador
 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)   
    
    if content_type == 'text':
     if msg['text'] == '/start':
      bot.sendMessage(chat_id, 'Bienvenido al bot de ELP. ¿Eres un alumno o el profesor?', reply_markup=keyboardLogin)
     if msg['text'] == '/mostrar' and chat_id in users:
      bot.sendMessage(chat_id, 'Puede enviar un mensaje al profesor pulsando el boton de abajo.', reply_markup=keyboardUser)
     elif msg['text'] == claveAdmin and admin[0] == 0:
      admin[0] = chat_id
      menuAdmin()
     elif msg['text'] == claveUser and not chat_id in users:
      bot.sendMessage(chat_id, 'Clave correcta. Bienvenido al bot de ELP. Cuando el profesor envíe algo yo te lo haré llegar. Si tienes algún mensaje para el profesor o alguna sugerencia, puedo hacérselo llegar si pulsas el botón de abajo.', reply_markup=keyboardUser)
     elif chat_id in senders:
      senders.remove(a)
      buzon.append(msg['text'])
      bot.sendMessage(chat_id, 'Mensaje enviado.', reply_markup=keyboardUser)
     elif chat_id == admin[0] and admin[1] == 1:
      res = encuesta(msg['text'])
      bot.sendMessage(chat_id, res[0], reply_markup=res[1])
      

# Las pulsaciones en los botones del bot se gestionan en esta función
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    
    if query_data == 'alumno':
      bot.answerCallbackQuery(query_id, text='Introduzca el código de los alumnos.')
    elif query_data == 'profesor':
      bot.answerCallbackQuery(query_id, text='Introduzca el código del profesor.')
    elif query_data == 'msg_user':
      senders.append(from_id)
      bot.sendMessage(from_id, "Escriba el mensaje que quiere enviar.", reply_markup=keyboardMensaje)
    elif query_data == 'encuesta':
      admin[1] = 1
      bot.sendMessage(from_id, "Escriba el texto del mensaje primero y las opciones a elegir de la encuesta separadas por punto y coma. Ej: Texto del mensaje; Opcion 1; Opcion 2; ...", reply_markup=keyboardMensaje)
    elif query_data == 'cancelar':
      if from_id == admin[0] and admin[1] == 1: # El admin cancela la encuesta
       admin[1] = 0
       menuAdmin()
      elif from_id in senders: # Un usuario cancela el envio de un mensaje
       senders.remove(from_id)
       bot.sendMessage(from_id, 'Mensaje no enviado.', reply_markup=keyboardUser)

# Envia el menu principal del bot al admin
def menuAdmin():
 if len(buzon) == 0: # Si no tiene mensajes
  bot.sendMessage(admin[0], 'Bienvenido, no tiene mensajes en el buzón. ¿Qué desea hacer?', reply_markup=keyboardAdminSinMsg)
 else:
  n = len(buzon)
  bot.sendMessage(admin[0], txtMensajes(n) + '¿Qué desea hacer?', reply_markup=keyboardAdminMsg)

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