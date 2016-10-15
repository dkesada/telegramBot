# Suma dos operandos

import sys
import telepot
from telepot.delegate import per_chat_id, create_open, pave_event_space

class Sumador(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(Sumador, self).__init__(*args, **kwargs)
		self._operando = 0
		self._sumando = False

	def on_chat_message(self, msg):
		if self._sumando == False:
			self._sumando = True
			self._operando = int(msg['text'])
			self.sender.sendMessage("Introduzca el siguiente operando: ")
		else:
			self._sumando = False
			self.sender.sendMessage("Resultado: " + str(self._operando + int(msg['text'])))


TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, Sumador, timeout=10
    ),
])
bot.message_loop(run_forever='Listening ...')
