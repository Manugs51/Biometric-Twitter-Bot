import tweepy
import time
from secrets import *

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
api = tweepy.API(auth)


respuesta_temporal = (" De momento no sé responder a esa pregunta, pero puedes entrar a "
					  "https://elp42019.wixsite.com/biometricdata/ y quizá encuentres "
					  "ahí esa información")
#tweet = "hola"
#busqueda = "#biometrico"
#Para evitar que pida demasiada información
#id_ultimo_biometrico = 1203071930242351104

#Tweetea
#api.update_status(tweet)

#Devuelve la lista de tweets con un hastag
#api.search(q = busqueda, result_type = "recent")

#Devuelve los 10 tweets mas nuevos con un hashtag
#  y más nuevos que el indicado y los imprime
"""
answer = api.search(q = busqueda,
					result_type = "recent",
					count = 10,
					since_id = id_ultimo_biometrico)

for tweets in answer:
	print(tweets, "\n")
"""
#Menciones

#  Texto del tweet de la mencion
#api.mentions_timeline()[0].text

#  ID del tweet de la mencion
#api.mentions_timeline()[0].id


#  username sin @ del usuario del tweet de la mencion
#api.mentions_timeline()[0].user.screen_name

#while True:


#usuario = "@" + menciones[0].user.screen_name
#id_respuesta = menciones[0].id


#api.update_status(status = usuario + respuesta_temporal,
#				  in_reply_to_status_id = id_respuesta)

#Sería más correcto realizar todo lo de dentro del bucle
#  una sola vez y que fuera el sistema operativo el que 
#  llamara periódicamente al proceso, pero también es más
#  costoso de implementar.
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
		usuario = "@" + m.user.screen_name

		#Se responde
		api.update_status(status = usuario + respuesta_temporal,
						  in_reply_to_status_id = m.id)

	#Máximo de 75 peticiones cada 15 minutos en Twitter
	#  podría ser 900/75 = 12 segundos de espera
	time.sleep(15)