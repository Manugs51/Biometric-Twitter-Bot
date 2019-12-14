import tweepy
import time
from secrets import *

def main():
	auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
	auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
	api = tweepy.API(auth)


	respuesta_temporal = ("De momento no sé responder a esa pregunta, pero puedes entrar a "
						  "https://elp42019.wixsite.com/biometricdata/ y quizá encuentres "
						  "ahí esa información")

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
			print(m.text, "\n")

			#Se actualiza la ultima mencion
			file = open("id_ultima_mencion.txt", "w")
			file.write(str(m.id))
			file.close()

			#A la hora de responder es necesario mencionar al usuario
			usuario = "@" + m.user.screen_name + " "

			#Se responde
			api.update_status(status = usuario + respuesta_temporal,
							  in_reply_to_status_id = m.id)

		#Máximo de 75 peticiones cada 15 minutos en Twitter
		#  podría ser 900/75 = 12 segundos de espera
		time.sleep(15)


if __name__ == "__main__":
	main():