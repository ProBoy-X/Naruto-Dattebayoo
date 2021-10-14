import os
import subprocess
import sys
from time import sleep
from typing import List

from telegram import Bot, Update, TelegramError
from telegram.ext import CommandHandler, run_async

from Naruto import dispatcher
from Naruto.modules.helper_funcs.chat_status import dev_plus


@run_async
@dev_plus
def leave(bot: Bot, update: Update, args: List[str]):
    if args:
        chat_id = str(args[0])
        try:
            bot.leave_chat(int(chat_id))
            update.effective_message.reply_text("Beep boop, I left that soup!.")
        except TelegramError:
            update.effective_message.reply_text("Beep boop, I could not leave that group(dunno why tho).")
    else:
        update.effective_message.reply_text("Send a valid chat ID")


@run_async
@dev_plus
def gitpull(bot: Bot, update: Update):
    sent_msg = update.effective_message.reply_text("ᴄʜᴀɴɢᴇs ʜᴜᴇ ʜ sᴀʏᴀᴅ..🤔 ʀᴇsᴛᴀʀᴛ ʜᴏʀᴀ ʜᴜ..")
    subprocess.Popen('git pull', stdout=subprocess.PIPE, shell=True)

    sent_msg_text = sent_msg.text + "\n\n ᴄʜᴀɴɢᴇs ʜᴜᴇ ʜ sᴀʏᴀᴅ..🤔 ʀᴇsᴛᴀʀᴛ ʜᴏʀᴀ ʜᴜ.."

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("ʀᴇsᴛᴀʀᴛᴇᴅ.!")

    os.system('restart.bat')
    os.execv('start.bat', sys.argv)


@run_async
@dev_plus
def restart(bot: Bot, update: Update):
    update.effective_message.reply_text("Starting a new instance and shutting down this one")

    os.system('restart.bat')
    os.execv('start.bat', sys.argv)


LEAVE_HANDLER = CommandHandler("leave", leave, pass_args=True)
GITPULL_HANDLER = CommandHandler("gitpull", gitpull)
RESTART_HANDLER = CommandHandler("reboot", restart)

dispatcher.add_handler(LEAVE_HANDLER)
dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "DEV"
__handlers__ = [LEAVE_HANDLER, GITPULL_HANDLER, RESTART_HANDLER]
