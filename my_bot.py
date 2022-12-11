"""
Un chatbot qui s'identifie et donnes des citations aléatoires.
"""

import random
import math
from numbers import Number

import matplotlib.axes
import matplotlib.pyplot as plt
from chatbot import *
from twitch_bot import *


class VotesPlot:
    x_data = None
    y_bars = None
    x_limit = None
    y_limit = None
    axes = None

    def __init__(self, x_data, y_limit: Number, title="Votes in the chat!"):
        # TODO: Reproduire la construction du graphique (code du chapitre 10), mais dans des variables d'instances de
        #  l'objet courant.
        y_data = [0] * len(x_data)
        fig: plt.Figure
        ax: plt.Axes
        fig, ax = plt.subplots()
        fig.suptitle(title)
        ax.set_xlabel("Possible values")
        ax.set_ylabel("Num votes")  # TODO: Donner un nom aux deux axes.
        ax.set_ylim(*(0, y_limit))  # TODO: Établir la portée de l'axe y de 0 à y_limit.
        # TODO: Créer un axe d'histogramme (bar).
        self.axes = ax
        self.fig = fig
        self.x_data = x_data
        self.y_data = y_data
        self.y_limit = y_limit
        self.reset_bars(x_data)

    def reset_bars(self, x_data):
        self.x_data = x_data
        self.axes.clear()
        self.y_data = [0] * len(self.x_data)
        self.y_bars = self.axes.bar(self.x_data, self.y_data)

    def update_plot(self):
        # TODO: Reproduire la mise-à-jour du graphique.
        for bar, y in zip(self.y_bars, self.y_data):
            bar.set_height(y)  # TODO: Mettre à jour les barres de l'histogramme (y_bars) avec les données (y_data).
        # TODO: Mettre à jour la portée de l'axe verticale au multiple de y_limit le plus proche de la valeur
        #  maximale en y.
        plt.ylim(0, self.y_limit * math.ceil((max(self.y_data)+1)/self.y_limit))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


# TODO: Hériter de la classe TwitchBot
class MyBot(TwitchBot):
    def __init__(self, logs_folder: str, quotes: dict[str, list[str]], votes_plot: VotesPlot):
        # TODO: Construire la classe parent en lui passant le dossier de journaux.
        # TODO: Garder le dictionnaire de citations (paramètre `quotes`) dans une variable d'instance.
        # TODO: Garder le graphique dans une variable d'instance `votes_plot`.
        super().__init__(logs_folder)
        self.quotes = quotes
        self.votes_plot = votes_plot

    # TODO: Ajouter une commande "say_hi" (à l'aide du décorateur TwitchBot.new_command) qui répond avec un message de
    #  la forme: "My name is <nom-du-bot>. You killed my father. Prepare to die.", où <nom-du-bot> est le nom du
    #  compte utilisé par le chatbot. Indice : Dans la méthode connect_and_join de TwitchBot, le nom (nickname) du bot
    #  est gardé comme attribut.
    @TwitchBot.new_command(0)
    def say_hi(self, cmd: Chatbot.Command):
        self.send_privmsg(f"My name is {self.nickname}. You killed my father. Prepare to die.")

    # TODO: Ajouter une commande "quote" qui répond de trois façons selon ce qui suit le nom de la commande dans le
    #  message. Si un nom de catégorie est donné (on trouve les paramètres de la commande dans cmd.params) : Si la
    #  catégorie est connue, on envoie au hasard une citation venant de cette catégorie si elle est connue. Sinon,
    #  on envoie un message disant que la catégorie est inconnue (ex. "Unrecognized category 'la_catégorie'"). Si
    #  aucune catégorie n'est fournie, on choisit au hasard une catégorie puis une citation (comme dans l'exemple du
    #  chapitre 8)
    @TwitchBot.new_command
    def quote(self, cmd: Chatbot.Command):

        category = cmd.params

        if category is not None:
            if category in self.quotes:
                msg = random.choice(self.quotes[category])
            else:
                msg = f"Unrecognized category {category}. Possible categories are {','.join(self.quotes.keys())}"
        else:
            category = random.choice(tuple(self.quotes.keys()))
            msg = random.choice(self.quotes[category])
        self.send_privmsg(msg)

    # TODO: Ajouter une commande "vote" qui reproduit le comportement de la même commande de l'exemple du chapitre 10
    @TwitchBot.new_command(0)
    def vote(self, cmd: Chatbot.Command):
        vote = cmd.params
        # TODO: Trouver l'index de la valeur votée dans les noms des barres (votes_plot.x_data).
        try:
            index = self.votes_plot.x_data.index(vote)
        except ValueError:
            index = -1

        if index != -1:
            self.votes_plot.y_data[index] += 1
        else:
            self.send_privmsg(f"Les votes possibles sont: {','.join(self.votes_plot.x_data)}")

    # TODO: Ajouter une commande "start_new_vote" qui réinitialise les barres du graphique avec les valeurs en
    #  paramètre de la commande (éléments séparés d'un espace).
    @TwitchBot.new_command(0)
    def start_new_vote(self, cmd: Chatbot.Command):
        if cmd.params is not None:
            self.votes_plot.reset_bars(cmd.params.split(" "))
            self.send_privmsg(f"Reseted plot! New votes options are {','.join(self.votes_plot.x_data)}")
        else:
            self.send_privmsg("Please enter parameters for the new vote!")
