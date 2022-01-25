import random

from chatterbot import ChatBot, filters
import datetime
import threading
import time
# Uncomment the following lines to enable verbose logging
# import logging
# logging.basicConfig(level=logging.INFO)
from chatterbot.response_selection import get_first_response
# Create a new instance of a ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
#from chatterbot.trainers import UbuntuCorpusTrainer
bot = ChatBot(
    'Bobby',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db',
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ]
)
#trainer = UbuntuCorpusTrainer(bot)
#trainer.train()
#trainer = ChatterBotCorpusTrainer(bot)
#
#trainer.train(
#    "chatterbot.corpus.english.greetings"
#)

current_conversations = {}


def conversation_deleter():
    while 1:
        for conversation in current_conversations.values():
            if (datetime.datetime.now() - conversation.last_res_time).total_seconds() > 60:
                print(f'Deleted conversation {conversation.ID}')
                del current_conversations[conversation.ID]
                break
        time.sleep(1)


def get_bot_from_ID(ID: int):
    return bot

class chatbot:
    def __init__(self, name: str):
        self.ID = 0

    def get_response(self, statement: str):
        try:
            print('Getting response')
            res = bot.get_response(statement)
            print('Got response')
            return res
        except Exception as ex:
            return None
