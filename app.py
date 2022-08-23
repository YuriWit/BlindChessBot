import telebot
import chess.engine, chess.pgn, chess, os, random

bot = telebot.TeleBot(os.sys.argv[1])

engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')
engine.configure({'Skill Level':1})

games = {}
ai = {}

def turnMsg(bool):
    return 'White to play' if bool else 'Black to play'

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, 'Type /help for command list')

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message,'''
/help - this list
/startgame - to start a new game
/show - show board
/aiOn - turn auto ai response on
/aiOff - turn auto ai response Off
/aiMove - make ai move
/png - get all game moves 
''')

@bot.message_handler(commands=['startgame'])
def start_game(message):
    try:
        if message.chat.id not in games:
            games[message.chat.id] = {'board':chess.Board(), 'ai': False, 'moves':[]}
        else:
            games[message.chat.id]['board'] = chess.Board()
            games[message.chat.id]['moves'] = []
        bot.send_message(message.chat.id, 'Game Started')
        if games[message.chat.id]['ai'] and random.choice([True, False]):
            result = engine.play(games[message.chat.id]['board'], chess.engine.Limit(time=0.1))
            games[message.chat.id]['moves'].append(games[message.chat.id]['board'].san(result.move))
            bot.send_message(message.chat.id, games[message.chat.id]['board'].san(result.move))
            games[message.chat.id]['board'].push(result.move)
        bot.send_message(message.chat.id, turnMsg(games[message.chat.id]['board'].turn))
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['show'])
def show(message):
    try:
        # make work with png
        #url = 'https://fen2png.com/api/?fen=' + urllib.parse.quote(games[message.chat.id].fen())
        url = 'http://www.fen-to-image.com/image/' + games[message.chat.id]['board'].fen()
        bot.send_photo(message.chat.id, url)
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['aiOn'])
def aiOn(message):
    try:
        games[message.chat.id]['ai'] = True
        bot.reply_to(message, 'ai On')
    except Exception as e:
        bot.reply_to(message, e)

@bot.message_handler(commands=['aiOff'])
def aiOff(message):
    try:
        games[message.chat.id]['ai'] = False
        bot.reply_to(message, 'ai Off')
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
        bot.send_message(message.chat.id, png)

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(func=lambda message: True)
def try_move(message):
    try:
        games[message.chat.id]['board'].push_san(message.text)
        if games[message.chat.id]['ai']:
            result = engine.play(games[message.chat.id]['board'], chess.engine.Limit(time=0.1))
            bot.send_message(message.chat.id, games[message.chat.id]['board'].san(result.move))
            games[message.chat.id]['board'].push(result.move)
    except Exception as e:
        bot.reply_to(message, e)
    finally:
        if games[message.chat.id]['board'].is_game_over():
            bot.send_message(message.chat.id, 'Game Over')
        else:
            bot.reply_to(message, turnMsg(games[message.chat.id]['board'].turn))


bot.infinity_polling()