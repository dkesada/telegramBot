import time
import telepot
import threading
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from Queue import Queue

partidas = {}

keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Unirse', callback_data='unirse'),
                   InlineKeyboardButton(text='Comenzar partida', callback_data='comenzar')],
               ])
               
# Bot que organiza partidas de espia en grupos. Al ser anadido a un grupo, se va anadiendo
# gente a la partida por medio del inline keyboard y al darle a comenzar se distribuyen
# oficios entre los jugadores. Se creara una cuenta atras para ese chat en concreto y cuando
# esta llegue a 0 se notificara en el grupo que la partida ha acabado y se eliminara
# del diccionario. Hago uso de threads para que cada uno se encargue de una partida y no 
# bloquear la llegada de nuevas peticiones de partidas.

# Las partidas de espia consisten en generar una ubicacion (cocina de restaurante, submarino,
# tren, castillo medieval...) y "oficios" relacionados con dicha ubicacion (si es cocina
# de restaurante los oficios seran algo asi como cocinero, pinche, camarero, friegaplatos...) y
# un espia, que no sabra la ubicacion. Ninguno de los jugadores sabra que oficio tienen los otros
# ni quien es el espia, lo unico que sabran todos excepto el espia es la ubicacion en la que se
# encuentran.
# El juego se desarrolla a base de preguntarse unos a otros sobre la ubicacion o el oficio que
# desempenan con el objetivo de descubrir quien es el espia. Si el espia descubre o adivina la
# ubicacion ganara el, si por el contrario el resto de jugadores descubren quien es el espia,
# ganaran ellos.

# El bot se encargara de montar la partida, eligiendo una ubicacion aleatoria de entre las que
# hay y generando un espia y oficios para el resto de jugadores. Habra una cuenta atras, para
# que si en ese tiempo no se ha descubierto al espia y este no ha adivinado la ubicacion,
# la partida pueda darse por concluida.

# Hago uso del inline keyboard con este bot. Es interesante el poder diferenciar los mensajes
# normales del chat de los callback query que genera el teclado, ademas de poder mandar mesajes
# de manera independiente a miembros de un grupo sin que el resto puedan verlos. En este bot
# hago uso de estos mensajes a cada miembro para distribuir la localizacion y el oficio a cada
# integrante de la partida sin que el resto lo sepan, cosa fundamental para el desarrollo de
# una partida.


# Comienza la cuenta atras en un thread. Al llegar a 0 la cuenta atras o al terminar la partida
# desde el propio chat, se elimina esta del diccionario del bot
def cuentaAtras(x):
 par = convers[x]
 bot.sendMessage(x, 'Conexion finalizada.')
 bot.sendMessage(par, 'Conexion finalizada.')
 del convers[x]
 del convers[par]

# Anade el chat al diccionario y crea el thread con la queue para 
# pasarle usuarios que se vayan uniendo, el inicio de la partida o el final
# de la misma
def comienzo(chat_id):
 q = Queue.Queue()
 t = threading.Thread(target=partida, args=(chat_id, q,))
 t.setDaemon = True
 partidas[chat_id] = t
 t.start()

def partida(chat_id, q):
 num_jugadores = 0;
 fin = False
 jugadores = []
 while(not fin):
  val = self.queue.get()
  if val[0] is 'empezar':
   1+1;
  elif val[0] is 'nuevoJugador' and not(val[1] in jugadores):
   jugadores.append(val[1])
  elif val[0] is 'finalizar':
   fin = True
  
# Una peticion coloca en la cola del chat en el diccionario un mensaje para el thread que
# corresponda
def peticion(chat_id, mensaje):
 
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
    
    if msg['text'] == '/start' and  msg['chat']['type'] == 'group' and not(chat_id in partidas):
      bot.sendMessage(chat_id, 'Bienvenidos.', reply_markup=keyboard1)
      comienzo(chat_id)
    elif msg['text'] == '/start' and  msg['chat']['type'] != 'group':
      bot.sendMessage(chat_id, 'Solo puedo montar una partida de espia en un grupo.')
    elif msg['text'] == '/Muestrate' and  msg['chat']['type'] == 'group':
      bot.sendMessage(chat_id, 'Aqui estoy.', reply_markup=keyboard1)
    if msg['text'] == '/fin' and  msg['chat']['type'] == 'group' and chat_id in partidas:
      peticion(chat_id, ['finalizar'])
    

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    print(user_id)
    chat_id = msg['message']['chat']['id']
    if query_data == 'comenzar' and not(chat_id in partidas):
      bot.answerCallbackQuery(query_id, text='Got it')
      peticion(chat_id, ['comenzar'])
    if query_data == 'unirse':
      peticion(chat_id, ['unirse', from_id])
      bot.answerCallbackQuery(query_id, text='Got it')

    bot.answerCallbackQuery(query_id, text='Got it')

TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.Bot(TOKEN)
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
print ('Listening ...')

while 1:
    time.sleep(10)
