import time
import telepot
import threading
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

num = [0]
ids = [1,2]
convers = {}

keyboard1 = ReplyKeyboardMarkup(keyboard=[
                   [KeyboardButton(text='Comenzar'),KeyboardButton(text='Finalizar')],
               ])

# Bot que organiza peticiones de clientes y los empareja para
# que hablen de manera anonima hasta que uno termina la conexion


# Termina una conversacion
def terminarPareja(x):
 par = convers[x]
 bot.sendMessage(pareja[0], 'Conexion finalizada.')
 bot.sendMessage(pareja[1], 'Conexion finalizada.')
 del convers[x]
 del convers[par]

 
#Una peticion coloca un chat_id a la espera de otro o comienza una conexion entre 2
def peticion(x):
 
 if num[0] == 1 and ids[0] != x:
  ids[1] = x
  bot.sendMessage(ids[0], 'Conexion iniciada.')
  bot.sendMessage(ids[1], 'Conexion iniciada.')
  convers[ids[0]] = ids [1]
  convers[ids[1]] = ids [0]
  num[0] = 0
 else:
  ids[0] = x
  num[0] = 1
  
 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)   
    
    if content_type == 'text':
     if msg['text'] == '/start':
      bot.sendMessage(chat_id, 'Bienvenido.', reply_markup=keyboard1)
     elif msg['text'] == 'Comenzar' and  not (chat_id in convers):
	  peticion(chat_id)
     elif msg['text'] == 'Finalizar' and  chat_id in convers:
      terminarPareja(chat_id)
     elif chat_id in convers:
      bot.sendMessage(convers[chat_id], msg['text'])
	  

TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.Bot(TOKEN)
bot.message_loop(on_chat_message)
print ('Listening ...')

while 1:
    time.sleep(10)
