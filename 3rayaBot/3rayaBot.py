#-*. coding: utf-8 -*-
import sys
import time
import threading
from Queue import Queue
import telepot
import telepot.helper
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)

"""
$ python3.5 quiz.py <token>
Send a chat message to the bot. It will give you a math quiz. Stay silent for
10 seconds to end the quiz.
It handles callback query by their origins. All callback query originated from
the same chat message will be handled by the same `CallbackQueryOriginHandler`.
"""

partidas = {}
q = Queue()

# El gestionador lleva todo lo relacionado con crear partidas y terminarlas
class Gestionador(threading.Thread):
    def __init__(self, cola):
        threading.Thread.__init__(self)
        self.cola = cola
        self.num = 0
        self.ids = [1,2]
    
    def run(self):
        while(True):
            mensaje = self.cola.get()
            if mensaje[0] is 'pair':
                self.peticion(mensaje[1])
            elif mensaje[0] is 'delPair':
                del partidas[mensaje[1]]
            time.sleep(3)
            
    def peticion(self, x):
        if self.num == 1 and self.ids[0] != x:
            self.ids[1] = x
            q1 = Queue()
            q2 = Queue()
            partidas[self.ids[0]] = [self.ids[1],'x',q1]
            partidas[self.ids[1]] = [self.ids[0],'o',q2]
            self.num = 0
        else:
            self.ids[0] = x
            self.num = 1

class GameStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GameStarter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.sender.sendMessage(
            'Pulsa START para buscar una partida.',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text='START', callback_data='start'),
                ]]
            )
        )

        self.close()  # Dejas que Game se haga cargo de las partidas

class Game(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.tipo = ' '
        self.turno = 'x'

    def _next_move(self, from_id):
        if self.turno != self.tipo:
            msg = self.representateKeyboard() 
            self.editor.editMessageText(msg, reply_markup=None)
            mov = partidas[from_id][2].get() # Si no te toca esperas el siguiente movimiento
            self.board[mov[0]] = mov[1]
        self.turno = self.invers() 
        msg = 'Tu turno.'
        keyboard = self.createKeyboard()
        
        self.editor.editMessageText(msg,reply_markup=keyboard)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

        if query_data == 'start':
            q.put(['pair', from_id])
            while from_id not in partidas:
                time.sleep(2)
            self.tipo = partidas[from_id][1]
        else:
            self.movimiento(from_id, int(query_data), self.tipo)

        self._next_move(from_id)

    def on__idle(self, event): # Si no se hace nada durante un tiempo se acaba la partida
        text = 'Partida terminada por inactividad.'
        self.editor.editMessageText(text, reply_markup=None)
        self.close()
        
    def movimiento(self,from_id,pos,val): # Manda un movimiento a tu oponente
        self.board[pos] = val
        partidas[partidas[from_id][0]][2].put([pos,val])
    
    def invers(self):
        if self.turno == 'x':
            return 'o'
        else:
            return 'x'
    
    def createKeyboard(self): # Crea un teclado con el tablero que se le da
        botones = []
        for i in [0,3,6]:
            botones.append([InlineKeyboardButton(text=self.board[i], callback_data=str(i)),
                            InlineKeyboardButton(text=self.board[i+1], callback_data=str(i+1)),
                            InlineKeyboardButton(text=self.board[i+2], callback_data=str(i+2))])
        return InlineKeyboardMarkup(inline_keyboard = botones)
    
    def representateKeyboard(self): # Crea una representacion en texto del tablero
        rep = ''
        for i in [0,3,6]:
            rep = rep + '|'+ self.board[i] +'|' + self.board[i+1] + '|' + self.board[i+2] + '| \n'
            
        return rep

gest = Gestionador(q)
gest.setDaemon = True
gest.start()

TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, GameStarter, timeout=30),
    pave_event_space()(
        per_callback_query_origin(), create_open, Game, timeout=30),
])

bot.message_loop(run_forever='Listening ...')
