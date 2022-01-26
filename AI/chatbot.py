import os
import random
import shutil

from chatterbot import ChatBot, filters
import datetime
import threading
import time
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer


bot = ChatBot(
    'Bobby',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.db',
    logic_adapters=[
        "chatterbot.logic.BestMatch"
    ],
    read_only=True
)

#trainer = ChatterBotCorpusTrainer(bot)
trainer = ListTrainer(bot)
current_conversations = {}


def conversation_deleter():
    while 1:
        for conversation in current_conversations.values():
            if (datetime.datetime.now() - conversation.last_res_time).total_seconds() > 300:
                print(f'Deleted conversation {conversation.ID}')
                os.remove(f"{conversation.ID}.db")
                del current_conversations[conversation.ID]
                break
        time.sleep(1)


def get_bot_from_ID(ID: int):
    for conversationID in current_conversations:
        if int(conversationID) == ID:
            return current_conversations[conversationID]

    return None

class chatbot:
    def __init__(self, server_id: int):
        self.ID = server_id
        shutil.copy('database.db', f'{self.ID}.db')
        self.bot = ChatBot(
            'Bobby',
            storage_adapter='chatterbot.storage.SQLStorageAdapter',
            database_uri=f'sqlite:///{self.ID}.db',
            logic_adapters=[
                "chatterbot.logic.BestMatch"
            ],
            filters=[
                "chatterbot.filters.RepetitiveResponseFilter"
            ],
            read_only=True
        )
        self.trainer = ListTrainer(self.bot)

        current_conversations[self.ID] = self

    def get_response(self, statement: str):
        try:
            res = bot.get_response(statement)
            return res
        except Exception as ex:
            return None

    def train(self, statement: str, prev_statement: str):
        try:
            self.trainer.train([prev_statement, statement])
        except Exception as ex:
            print('Exception while training: ' + str(ex))
