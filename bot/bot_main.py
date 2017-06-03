import telebot
import bot.bot_config as config
import bot.const as const


bot = telebot.TeleBot(config.BOT_TOKEN)

history = {}


def send_msg_type(chat_id):
    markup_start = telebot.types.ReplyKeyboardMarkup(True, True)
    markup_start.row('vs AI', 'vs human')
    bot.send_message(chat_id, const.msg_choose_type, reply_markup=markup_start)


def send_msg_wrong_type(chat_id):
    bot.send_message(chat_id, const.msg_wrong_type)


def bot_start():
    print('bot is activated')

    @bot.message_handler(commands=['start'])
    def handle_command(message):
        history[str(message.chat.id)] = {'state': const.state_start}
        send_msg_type(message.chat.id)

    @bot.message_handler(commands=['restart'])
    def handle_command(message):
        print('RESTART')
        if message.chat.id in history:
            pass
        else:
            history[str(message.chat.id)] = {'state': const.state_start}

    @bot.message_handler(content_types=['text'])
    def handle_command(message):
        if str(message.chat.id) in history:
            cur_state = history[str(message.chat.id)]['state']
            print('cur_state:::', cur_state)

            if cur_state == const.state_start:
                if message.text == const.var_vs_ai:
                    cur_state = const.state_choose_type
                elif message.text == const.var_vs_human:
                    cur_state = const.state_choose_type
                else:
                    send_msg_wrong_type(message.chat.id)
                    print('type incorrect')
            elif cur_state == const.state_choose_type:
                pass
            elif cur_state == const.state_choose_difficulty:
                pass
            elif cur_state == const.state_playing:
                pass
            else:
                pass
        else:
            bot.send_message(message.chat.id, 'enter /start - to start the game')

    bot.polling(none_stop=True, interval=0.5)


if __name__ == '__main__':
    bot_start()
