import telebot
import chess.engine, chess.pgn, chess, os, random

bot = telebot.TeleBot(os.sys.argv[1])

engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')
engine.configure({'Skill Level':1})

games = {}

def turnMsg(bool):
    return 'White to play' if bool else 'Black to play'

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Type /help for command list')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message,'''
/help
/startgame
/pause
/unpause
/turn
/show
/png
/aiOn
/aiOff
/aiMove
''')

@bot.message_handler(commands=['startgame'])
def start_game(message):
    try:
        if message.chat.id not in games:
            games[message.chat.id] = {'board':chess.Board(), 'ai': False, 'on':True}
        else:
            games[message.chat.id]['board'] = chess.Board()
            games[message.chat.id]['on'] = True
        bot.reply_to(message, 'Game Started')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['pause'])
def pause(message):
    try:
        games[message.chat.id]['on'] = False
        bot.reply_to(message, 'paused')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['unpause'])
def unpause(message):
    try:
        games[message.chat.id]['on'] = True
        bot.reply_to(message, 'unpaused')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['turn'])
def turn(message):
    try:
        bot.reply_to(message, 'White' if games[message.chat.id]['board'].turn else "Black")
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['show'])
def show(message):
    try:
        url = 'http://www.fen-to-image.com/image/' + games[message.chat.id]['board'].fen()
        bot.send_photo(message.chat.id, url)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['png'])
def png(message):
    try:
        b = chess.Board()
        moves = games[message.chat.id]['board'].move_stack
        png = ''
        for i in range(len(moves)):
            if i%2==0:
                png += str(int(i/2+1)) + '. '
            png += b.san(moves[i]) + ' '
            b.push(moves[i])
        bot.reply_to(message, png)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['aiOn'])
def aiOn(message):
    try:
        games[message.chat.id]['ai'] = True
        bot.reply_to(message, 'On')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['aiOff'])
def aiOff(message):
    try:
        games[message.chat.id]['ai'] = False
        bot.reply_to(message, 'Off')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['aiMove'])
def aiMove(message):
    try:
        result = engine.play(games[message.chat.id]['board'], chess.engine.Limit(time=0.1))
        bot.send_message(message.chat.id, games[message.chat.id]['board'].san(result.move))
        games[message.chat.id]['board'].push(result.move)
    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True)
def try_move(message):
    try:
        print(message)
        if not games[message.chat.id]['on']:
            return
        games[message.chat.id]['board'].push_san(message.text)
        if games[message.chat.id]['board'].is_game_over():
            bot.send_message(message.chat.id, 'Game Over')
            return
        if games[message.chat.id]['ai']:
            result = engine.play(games[message.chat.id]['board'], chess.engine.Limit(time=0.1))
            bot.send_message(message.chat.id, games[message.chat.id]['board'].san(result.move))
            games[message.chat.id]['board'].push(result.move)
            if games[message.chat.id]['board'].is_game_over():
                bot.send_message(message.chat.id, 'Game Over')
    except Exception as e:
        bot.reply_to(message, e)


bot.infinity_polling()