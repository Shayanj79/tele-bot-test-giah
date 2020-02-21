from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CallbackContext, CommandHandler, CallbackQueryHandler
from auth_tok import token
from data import Facts
from data import sortData
import random

class Data():
    initialStartMessage = 'Do you like Trains? Are you interested in the Solar System? Would you like to know Medical facts? If so then this is the right Bot for you!'

    initialKeyboardMarkup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Train Facts", callback_data="train"), InlineKeyboardButton("Medical Facts", callback_data="medical")],
            [InlineKeyboardButton("Planetary Facts", callback_data="planet")],
            [InlineKeyboardButton("Leaderboards", callback_data="leaderboard")]
        ]
    )
    newKeyboardMarkup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Hate It 😠", callback_data="hate"), InlineKeyboardButton("Love It 😍", callback_data="love")],
            [InlineKeyboardButton("Back", callback_data="backVote")]
        ]
    )
    likedKeyboardMarkup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Changed my mind", callback_data="hate"), InlineKeyboardButton("Loved It 😍", callback_data="love")],
            [InlineKeyboardButton("Back", callback_data="backVote")]
        ]
    )
    hatedKeyboardMarkup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Hated It 😠", callback_data="hate"), InlineKeyboardButton("Changed my mind 😍", callback_data="love")],
            [InlineKeyboardButton("Back", callback_data="backVote")]
        ]
    )
    leaderBoardMarkup = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Back", callback_data="backLeader")]
        ]
    )

class BotHandler():
    def __init__(self):
        self.updater = Updater(token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.queue = self.updater.job_queue
        self.dispatcher.add_handler(CommandHandler('start', self.start))
        self.dispatcher.add_handler(CallbackQueryHandler(self.initButtonClicked, pass_user_data=True))
        self.PersistentScoreSave = dict() #dict of list of scores to save
        self.PersistentNum = dict() #dict of list of vote values
    def initiate(self):
        print("Starting")
        self.updater.start_polling()
        self.updater.idle()
    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(Data.initialStartMessage, reply_markup=Data.initialKeyboardMarkup)
    def initButtonClicked(self, update: Update, context: CallbackContext):
        query = update.callback_query
        which = query.data
        print(f"Button {which} pressed by {query.from_user['first_name']}")
        print(self.PersistentScoreSave)
        if which in ["train", "medical", "planet"]:
            data = random.choices(getattr(Facts, which), k=5)
            string = ""
            counter = 1
            for each in data:
                string += f'{counter}. {each["text"]}\n'
                counter += 1
            #remove final newline
            string = string[:-1]
            query.message.edit_text(string, reply_markup=Data.newKeyboardMarkup)
            self.PersistentScoreSave[query.from_user['id']] = data
            query.answer(f"Here are {which} facts..")
        elif which in ["love", "hate", "backVote"]:
            if which == "hate":
                self.PersistentNum[query.from_user['id']] = -1
                query.answer(":(")
                query.message.edit_reply_markup(reply_markup=Data.hatedKeyboardMarkup)
            elif which == "love":
                self.PersistentNum[query.from_user['id']] = 1
                query.answer(":)")
                query.message.edit_reply_markup(reply_markup=Data.likedKeyboardMarkup)
            elif which == "backVote":
                if query.from_user['id'] in self.PersistentNum:
                    for each in self.PersistentScoreSave[query.from_user['id']]:
                        each["score"] += self.PersistentNum[query.from_user['id']]
                    sortData()
                    del self.PersistentNum[query.from_user['id']]
                query.answer("Ok")
                query.message.edit_text(Data.initialStartMessage, reply_markup=Data.initialKeyboardMarkup)
                del self.PersistentScoreSave[query.from_user['id']]
        elif which in ["leaderboard", "backLeader"]:
            if which == "leaderboard":
                query.answer("Showing for All")
                data = "Top Medical\n"
                for i in range(3):
                    data += f"{i+1}. {Facts.medical[i]['text']}\n"
                data += '\nTop Planetary\n'
                for i in range(3):
                    data += f"{i+1}. {Facts.planet[i]['text']}\n"
                data += '\nTop Train\n'
                for i in range(3):
                    data += f"{i+1}. {Facts.train[i]['text']}\n"
                data = data[:-1]
                query.message.edit_text(data, reply_markup=Data.leaderBoardMarkup)
            elif which == "backLeader":
                query.answer("Ok")
                query.message.edit_text(Data.initialStartMessage, reply_markup=Data.initialKeyboardMarkup)
bot = BotHandler()
bot.initiate()
