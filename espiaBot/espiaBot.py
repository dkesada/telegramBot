#-*. coding: utf-8 -*-
import time
import telepot
import threading
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from Queue import Queue
from random import randint

# El objetivo de este bot era comprobar cómo funcionan los bots en grupos y ver cómo 
# podía gestionar partidas con muchos miembros y usando threads para cada partida

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

# Este diccionario relaciona un chat_id con una cola a la que meto órdenes que le llegan de
# cada partida al bot. Las órdenes las gestiona cada hilo, cada uno las de su cola
partidas = {}

# Pongo una ubicacion y sus oficios a pincho para probar el bot

ubicaciones = ['Cocina de restaurante']
oficios = []
rel = {}
numUb = 0
rel['Cocina de restaurante'] = numUb
numUb = numUb + 1
cocina = ['Cocinero', 'Friega platos', 'Camarero', 'Pinche de cocina', 'Dueño del restaurante', 'Gerente']
oficios.append(cocina)


# Aquí pongo los 2 inline keyboards que voy a usar. Como estos van sujetos a un mensaje,
# cada mensaje puede tener un inline keyboard distinto.

keyboard1 = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Unirse', callback_data='unirse'),
                   InlineKeyboardButton(text='Comenzar partida', callback_data='comenzar')],
               ])
keyboard2 = InlineKeyboardMarkup(inline_keyboard=[
                   [InlineKeyboardButton(text='Ver oficio', callback_data='oficio')],
               ])


# Thread que espera un numero de segundos antes de poner fin a true
def cronometro(q, fin):
 cont = 0
 while not fin and cont < 60: #Numero de segundos que dura la partida
  time.sleep(1)
  cont = cont +1
 if not fin:
  q.put(['finalizar'])

# Anade el chat al diccionario y crea el thread con la queue para 
# pasarle mensajes
def comienzo(chat_id):
 q = Queue()
 t = threading.Thread(target=partida, args=(chat_id, q,))
 t.setDaemon = True
 partidas[chat_id] = q
 t.start()

#Este es el cuerpo de los threads que gestionan cada partida. La mayor parte del tiempo lo
#pasa esperando que le lleguen mensajes por la cola que se le asigna.
def partida(chat_id, q):
 num_jugadores = 0;
 fin = False
 jugadores = [] # Los jugadores que se vayan uniendo se añadirán aquí
 asignados = [] # Aquí se recogen los oficios asignados a cada jugador cuando comience la partida
 t = threading.Thread(target=cronometro, args=(q, fin)) # Cronómetro que dicta la duración máxima de la partida
 t.setDaemon = True
 empezada = False
 while(not fin): # fin sólo se pone a true si llega el comando /fin al bot o se acaba el tiempo de cronómetro lanzado antes
  mensaje = q.get()
  if mensaje[0] is 'comenzar' and not empezada:
   asignar(jugadores, asignados)
   t.start()
   empezada = True
   bot.sendMessage(chat_id, 'Comienza la partida.', reply_markup=keyboard2)
  elif mensaje[0] is 'unirse' and not(mensaje[1] in jugadores) and not empezada:
   jugadores.append(mensaje[1])
  elif mensaje[0] is 'finalizar' and empezada:
   bot.sendMessage(chat_id, 'Fin de la partida.')
   del partidas[chat_id]
   fin = True
  elif mensaje[0] is 'oficio' and empezada:
   pos = jugadores.index(mensaje[1])
   msg = asignados[pos]
   bot.answerCallbackQuery(mensaje[2], text=msg)
    

# Asigna una ubicacion a la partida y un oficio a cada jugador
def asignar(jugadores, asignados):
 u = ubicaciones[randint(0,numUb-1)] # Genero una ubicacion aleatoria
 numJ = len(jugadores)-1
 espia = randint(0,numJ) # Decido el espia
 numJ = numJ + 1
 of = oficios[rel[u]]
 numOf = len(of)-1

 for i in range(numJ):
  if i != espia:
   asignados.append('Ubicación: ' + u + ', oficio: ' + of[randint(0,numOf)])
  else:
   asignados.append('Eres el espía.')
  
  

# Una peticion coloca en la cola del chat en el diccionario un mensaje para el thread que
# corresponda
def peticion(chat_id, mensaje):
 if chat_id in partidas:
  partidas[chat_id].put(mensaje)
  
 
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)   
    
    if msg['text'] == '/espia' and  msg['chat']['type'] == 'group' and not(chat_id in partidas):
      bot.sendMessage(chat_id, 'Bienvenidos.', reply_markup=keyboard1)
      comienzo(chat_id)
    elif msg['text'] == '/espia' and  msg['chat']['type'] != 'group':
      bot.sendMessage(chat_id, 'Solo puedo montar una partida de espia en un grupo.')
    elif msg['text'] == '/Muestrate' and  msg['chat']['type'] == 'group':
      bot.sendMessage(chat_id, 'Aquí estoy.', reply_markup=keyboard1)
    if msg['text'] == '/fin' and  msg['chat']['type'] == 'group' and chat_id in partidas:
      peticion(chat_id, ['finalizar'])
    
# Los mensajes que mando a cada hilo tienen formato de lista, con el primer elemento siendo
# el nombre de cada tipo de mensaje, y el resto de campos los datos que le hagan falta
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    chat_id = msg['message']['chat']['id']
    if query_data == 'comenzar' and chat_id in partidas:
      bot.answerCallbackQuery(query_id, text='Partida comenzada.')
      peticion(chat_id, ['comenzar'])
    elif query_data == 'oficio' and chat_id in partidas:
      peticion(chat_id, ['oficio', from_id, query_id]) 
    elif query_data == 'unirse' and chat_id in partidas:
      peticion(chat_id, ['unirse', from_id])
      bot.answerCallbackQuery(query_id, text='Te has unido a la partida.')


TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.Bot(TOKEN)
# Definir así el message_loop hace que redirija los mensajes de texto a on_chat_message y
# los callback_query generados por el teclado del bot a on_callback_query
bot.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query})
print ('Listening ...')

while 1:
    time.sleep(10)
