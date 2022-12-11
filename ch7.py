"""
Exemple des notions du chapitre 7.
"""


from chatbot import *
from twitch_bot import *
from configparser import ConfigParser

def build_say_hi_callback(bot, message):
	# TODO: Créer et retourner une fonction qui prend un paramètre (ignoré).
	#       Cette fonction envoie `message` dans le chat à l'aide de la méthode `send_privmsg` du paramètre `bot`.
	def callback(*arg):
		bot.send_privmsg(message)
	return callback

def run_ch7_example():
	bot = TwitchBot("logs")
	conf = ConfigParser()
	conf.read("data/config.ini")
	# TODO: Construire le callback avec le bot et un message de votre choix.
	callback = build_say_hi_callback(bot, "hello")
	callback2 = build_say_hi_callback(bot, "bonjour tout le monde")
	callback3 = build_say_hi_callback(bot, "C'est quoi le STEP?")
	# TODO: Enregister le callback sous la commande "say_hi".
	bot.register_command("STEP", callback3)
	# TODO: Mettre votre jeton (incluant le "oauth:") et le nom du compte Twitch associé.
	bot.connect_and_join(
		conf.get("login", "account_oauth_token"),
		conf.get("login", "account_name"),
		conf.get("chat", "channel")
	)
	bot.run()


if __name__ == "__main__":
	run_ch7_example()
