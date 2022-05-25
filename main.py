import telebot
import chess.engine, chess

bot = telebot.TeleBot("5382490304:AAHAVgrcmrKFoSx2pNrjVpsAYF8aeQlz-Bc")

engine = chess.engine.SimpleEngine.popen_uci("/app/stockfish")
engine.configure({"Skill Level":1})

games = {}
ai = {}

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
/toggleai - toggleai
/show - show board
""")

@bot.message_handler(commands=['startgame'])
def start_game(message):
    try:
        games[message.chat.id] = chess.Board()
        ai[message.chat.id] = False
        bot.reply_to(message, "Game Started\n" + who_to_play(games[message.chat.id].turn))
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['toggleai'])
def start_game(message):
    try:
        if ai[message.chat.id] == True:
            ai[message.chat.id] = False
        else:
            ai[message.chat.id] = True
        bot.reply_to(message, "AI:\n" + str(ai[message.chat.id]))
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['show'])
def start_game(message):
    try:
        # make work with png
        #url = "https://fen2png.com/api/?fen=" + urllib.parse.quote(games[message.chat.id].fen())
        url = "http://www.fen-to-image.com/image/" + games[message.chat.id].fen()[0:-13]
        bot.send_photo(message.chat.id, url)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True)
def try_move(message):
    try:
        games[message.chat.id].push_san(message.text)
        if ai[message.chat.id]:
            result = engine.play(games[message.chat.id], chess.engine.Limit(time=0.1))
            bot.send_message(message.chat.id, games[message.chat.id].san(result.move))
            games[message.chat.id].push(result.move)
    except Exception as e:
        bot.reply_to(message, e)
    finally:
        if games[message.chat.id].is_game_over():
            bot.send_message(message.chat.id, "Game Over")
        else:
            bot.reply_to(message, who_to_play(games[message.chat.id].turn))


bot.infinity_polling()