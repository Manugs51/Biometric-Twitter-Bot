import tweepy
import time
import asyncio
import unidecode
from secrets import *
from rasa.core.agent import Agent
from rasa.core.interpreter import RasaNLUInterpreter

def main():
	#Claves de autorización para Twitter indicadas en secrets
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)

	#Para poder usar las acciones de Rasa
	agent = Agent.load("../Respuestas/models/20191214-013836.tar.gz")
	loop = asyncio.get_event_loop()

	while True:
		#Se coge el id de la última mención a la que se haya respondido
		file = open("id_ultima_mencion.txt", "r")
		id_ultima_mencion = file.readline()
		file.close()
		
		#Recopila las menciones más nuevas que la última mencion a la 
		#  que se haya respondido
		menciones = api.mentions_timeline(since_id = id_ultima_mencion)

		#Se invierte para que responda primero los más antiugos
		for m in reversed(menciones):

			#Para controlar por consola
			print(m.id)
			print(m.user.screen_name)
			print(m.text)

			#Se actualiza la ultima mencion
			file = open("id_ultima_mencion.txt", "w")
			file.write(str(m.id))
			file.close()

			#Formatear el texto para evitar errores y mejorar la comprensión
			texto_formateado = m.text.lower()
			texto_formateado = texto_formateado.replace("@abiometrica", "")
			texto_formateado = unidecode.unidecode(texto_formateado)

			#Se le pasa a Rasa para que decida la respuesta (se devuelve como una lista de diccionarios)
			dict_con_respuesta = loop.run_until_complete(agent.handle_text(texto_formateado, 
																		   sender_id = m.id))

			#Se le da formato a la respuesta
			respuesta = ""
			for valores in dict_con_respuesta:
				respuesta = respuesta + valores.get('text') + "\n\n"
			respuesta = respuesta[:-2]

			#Para controlar por consola
			print("Respuesta: ", respuesta)
			print("-------------------------------------\n\n\n")

			#A la hora de responder es necesario mencionar al usuario
			usuario = "@" + m.user.screen_name + " "

			#Se responde
			api.update_status(status = usuario + respuesta,
							  in_reply_to_status_id = m.id)

		#Máximo de 75 peticiones cada 15 minutos en Twitter
		#  podría ser 900/75 = 12 segundos de espera
		time.sleep(15)


if __name__ == "__main__":
	main()