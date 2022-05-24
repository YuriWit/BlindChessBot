from email import message
import telebot
import chess
import requests
import urllib

bot = telebot.TeleBot("5382490304:AAHAVgrcmrKFoSx2pNrjVpsAYF8aeQlz-Bc")

games = {}

def who_to_play(bool):
    if bool:
        return "White to play"
    else:
        return "Black to play"

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Type /help for command list")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message,"""
/startgame - to start a new game
/stopgame - to end current game
/mistakes - to list errors for players
""")

@bot.message_handler(commands=['startgame'])
def start_game(message):
    try:
        games[message.chat.id] = chess.Board()
        bot.reply_to(message, "Game Started\n" + who_to_play(games[message.chat.id].turn))
    except Exception as e:
        print(e)

@bot.message_handler(commands=['show'])
def start_game(message):
    try:
        # make work with png
        #url = "https://fen2png.com/api/?fen=" + urllib.parse.quote(games[message.chat.id].fen())
        url = "http://www.fen-to-image.com/image/" + games[message.chat.id].fen()[0:-13]
        bot.send_photo(message.chat.id, url)
    except Exception as e:
        print(e)


@bot.message_handler(func=lambda message: True)
def try_move(message):
    try:
        games[message.chat.id].push_san(message.text)
    except Exception as e:
        bot.reply_to(message, e)
    finally:
        if games[message.chat.id].is_game_over():
            bot.reply_to(message, "Game Over")
        else:
            bot.reply_to(message, who_to_play(games[message.chat.id].turn))


bot.infinity_polling()