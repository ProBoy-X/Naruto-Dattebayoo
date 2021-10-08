import html
from typing import List

from telegram import Bot, Update, ParseMode
from telegram.error import BadRequest
from telegram.ext import CommandHandler, Filters, run_async
from telegram.utils.helpers import mention_html

from Naruto import dispatcher, LOGGER, DEV_USERS, SUDO_USERS, TIGER_USERS
from Naruto.modules.disable import DisableAbleCommandHandler
from Naruto.modules.helper_funcs.chat_status import (bot_admin, user_admin, is_user_ban_protected, can_restrict,
                                                     is_user_admin, is_user_in_chat, connection_status)
from Naruto.modules.helper_funcs.extraction import extract_user_and_text
from Naruto.modules.helper_funcs.string_handling import extract_time
from Naruto.modules.log_channel import loggable, gloggable


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪᴅ ᴛʜᴇᴇᴋ ʜ ɴᴀ ᴠᴍʀᴏᴏ..👀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɴɪ ᴍɪʟᴀ ʏᴇ ᴄʜᴜᴛɪʏᴀ..☹️☹️")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("ᴡᴀᴀʜʜ ʙsᴅᴋ.!! ʟᴜɴᴅ ᴘʀɪᴢᴇ ᴍɪʟᴇɢᴀ ᴛᴜᴊʜᴇ ɪsᴋᴇ ʟɪʏᴇ.😂")
        return log_message

    # dev users to bypass whitelist protection incase of abuse
    if is_user_ban_protected(chat, user_id, member) and user not in DEV_USERS:
        message.reply_text("ᴀᴅᴍɪɴ ʜ ʏᴇ.. ɴɪ ᴋʀ sᴀᴋᴛᴀ ɪsᴇ ʙᴀɴ.☹️")
        return log_message

    log = (f"<b>{html.escape(chat.title)}:</b>\n"
           f"#BANNED\n"
           f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
           f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}")
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(chat.id, "Banned user {}.".format(mention_html(member.user.id, member.user.first_name)),
                        parse_mode=ParseMode.HTML)
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text('ʟᴏᴅᴀ ʙᴀɴɴᴇᴅ.😁', quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s", user_id, chat.title, chat.id,
                             excp.message)
            message.reply_text("sᴏʀʀʏ.. ʙᴀɴ ɴɪ ʜᴜᴀ ʏᴇ..😐 ")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def temp_ban(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪᴅ ᴛʜᴇᴇᴋ ʜ ɴᴀ ᴠᴍʀᴏᴏ..👀")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɴɪ ᴍɪʟᴀ ʏᴇ ᴄʜᴜᴛɪʏᴀ..☹️☹️")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("ᴡᴀᴀʜʜ ʙsᴅᴋ.!! ʟᴜɴᴅ ᴘʀɪᴢᴇ ᴍɪʟᴇɢᴀ ᴛᴜᴊʜᴇ ɪsᴋᴇ ʟɪʏᴇ.😂")
        return log_message

    if is_user_ban_protected(chat, user_id, member):
        message.reply_text("sᴏʀʀʏ..🥺")
        return log_message

    if not reason:
        message.reply_text("ᴋᴀʙ ᴛᴀᴋ ʙᴀɴ ᴋʀɴᴀ ʜ ɪsᴇ.? ᴍᴛʟʙ ᴋɪᴛɴᴀ ᴛɪᴍᴇ , ᴅɪɴ.?")
        return log_message

    split_reason = reason.split(None, 1)

    time_val = split_reason[0].lower()
    if len(split_reason) > 1:
        reason = split_reason[1]
    else:
        reason = ""

    bantime = extract_time(message, time_val)

    if not bantime:
        return log_message

    log = (f"<b>{html.escape(chat.title)}:</b>\n"
           "#TEMP BANNED\n"
           f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
           f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}\n"
           f"<b>Time:</b> {time_val}")
    if reason:
        log += "\n<b>Reason:</b> {}".format(reason)

    try:
        chat.kick_member(user_id, until_date=bantime)
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(chat.id, f"Banned! User {mention_html(member.user.id, member.user.first_name)} "
                                 f"will be banned for {time_val}.",
                        parse_mode=ParseMode.HTML)
        return log

    except BadRequest as excp:
        if excp.message == "Reply message not found":
            # Do not reply
            message.reply_text(f"Banned! User will be banned for {time_val}.", quote=False)
            return log
        else:
            LOGGER.warning(update)
            LOGGER.exception("ERROR banning user %s in chat %s (%s) due to %s",
                             user_id, chat.title, chat.id, excp.message)
            message.reply_text("Well damn, I can't ban that user.")

    return log_message


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def punch(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat
    user = update.effective_user
    message = update.effective_message
    log_message = ""

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪᴅ ᴛʜᴇᴇᴋ ʜ ɴᴀ ᴠᴍʀᴏᴏ..👀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɴɪ ᴍɪʟᴀ ʏᴇ ᴄʜᴜᴛɪʏᴀ..☹️☹️")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("sᴏʀʀʏ..🥺")
        return log_message

    if is_user_ban_protected(chat, user_id):
        message.reply_text("ᴡᴀᴀʜʜ ʙsᴅᴋ.!! ʟᴜɴᴅ ᴘʀɪᴢᴇ ᴍɪʟᴇɢᴀ ᴛᴜᴊʜᴇ ɪsᴋᴇ ʟɪʏᴇ.😂")
        return log_message

    res = chat.unban_member(user_id)  # unban on current user = kick
    if res:
        # bot.send_sticker(chat.id, BAN_STICKER)  # banhammer marie sticker
        bot.sendMessage(chat.id, f"ʟᴇ ʙsᴅᴋ!! {mention_html(member.user.id, member.user.first_name)}.",
                        parse_mode=ParseMode.HTML)
        log = (f"<b>{html.escape(chat.title)}:</b>\n"
               f"#KICKED\n"
               f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
               f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}")
        if reason:
            log += f"\n<b>Reason:</b> {reason}"

        return log

    else:
        message.reply_text("sᴏʀʀʏ..🥺 ɴɪ ᴋʀ sᴀᴋᴛᴀ ɪsᴇ ᴋɪᴄᴋ..")

    return log_message


@run_async
@bot_admin
@can_restrict
def punchme(bot: Bot, update: Update):
    user_id = update.effective_message.from_user.id
    if is_user_admin(update.effective_chat, user_id):
        update.effective_message.reply_text("ᴊʏᴀᴅᴀ ɢᴀɴᴅ ᴍᴛ ғᴜʟᴀ ʙsᴅᴋ ᴀᴅᴍɪɴ ʜ ᴛᴏ..😒")
        return

    res = update.effective_chat.unban_member(user_id)  # unban on current user = kick
    if res:
        update.effective_message.reply_text("No problem.")
    else:
        update.effective_message.reply_text("Huh? I can't :/")


@run_async
@connection_status
@bot_admin
@can_restrict
@user_admin
@loggable
def unban(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    log_message = ""

    user_id, reason = extract_user_and_text(message, args)

    if not user_id:
        message.reply_text("ɪᴅ ᴛʜᴇᴇᴋ ʜ ɴᴀ ᴠᴍʀᴏᴏ..👀.")
        return log_message

    try:
        member = chat.get_member(user_id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɴɪ ᴍɪʟᴀ ʏᴇ ᴄʜᴜᴛɪʏᴀ..☹️☹️")
            return log_message
        else:
            raise

    if user_id == bot.id:
        message.reply_text("ᴡᴀᴀʜʜ ʙsᴅᴋ.!! ʟᴜɴᴅ ᴘʀɪᴢᴇ ᴍɪʟᴇɢᴀ ᴛᴜᴊʜᴇ ɪsᴋᴇ ʟɪʏᴇ.😂")
        return log_message

    if is_user_in_chat(chat, user_id):
        message.reply_text("ʙᴀɴᴅᴀ ʙʜᴀɢ ɢᴀʏᴀ ɢʀᴏᴜᴘ sᴇ..😂")
        return log_message

    chat.unban_member(user_id)
    message.reply_text("ʙᴜʟᴀ ʟᴏ ɪssᴇ ᴠᴀᴘɪs..🤓")

    log = (f"<b>{html.escape(chat.title)}:</b>\n"
           f"#UNBANNED\n"
           f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
           f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}")
    if reason:
        log += f"\n<b>Reason:</b> {reason}"

    return log


@run_async
@connection_status
@bot_admin
@can_restrict
@gloggable
def selfunban(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user

    if user.id not in SUDO_USERS or user.id not in TIGER_USERS:
        return

    try:
        chat_id = int(args[0])
    except:
        message.reply_text("Give a valid chat ID.")
        return

    chat = bot.getChat(chat_id)

    try:
        member = chat.get_member(user.id)
    except BadRequest as excp:
        if excp.message == "User not found":
            message.reply_text("ɴɪ ᴍɪʟᴀ ʏᴇ ᴄʜᴜᴛɪʏᴀ..☹️☹️")
            return
        else:
            raise

    if is_user_in_chat(chat, user.id):
        message.reply_text("Aren't you already in the chat??")
        return

    chat.unban_member(user.id)
    message.reply_text("Yep, I have unbanned you.")

    log = (f"<b>{html.escape(chat.title)}:</b>\n"
           f"#UNBANNED\n"
           f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}")

    return log


__help__ = """
 - /punchme: punchs the user who issued the command

*Admin only:*
 - /ban <userhandle>: bans a user. (via handle, or reply)
 - /tban <userhandle> x(m/h/d): bans a user for x time. (via handle, or reply). m = minutes, h = hours, d = days.
 - /unban <userhandle>: unbans a user. (via handle, or reply)
 - /punch <userhandle>: Punches a user out of the group, (via handle, or reply)
"""

BAN_HANDLER = CommandHandler("ban", ban, pass_args=True)
TEMPBAN_HANDLER = CommandHandler(["tban", "tempban"], temp_ban, pass_args=True)
PUNCH_HANDLER = CommandHandler("punch", punch, pass_args=True)
UNBAN_HANDLER = CommandHandler("unban", unban, pass_args=True)
ROAR_HANDLER = CommandHandler("roar", selfunban, pass_args=True)
PUNCHME_HANDLER = DisableAbleCommandHandler("punchme", punchme, filters=Filters.group)

dispatcher.add_handler(BAN_HANDLER)
dispatcher.add_handler(TEMPBAN_HANDLER)
dispatcher.add_handler(PUNCH_HANDLER)
dispatcher.add_handler(UNBAN_HANDLER)
dispatcher.add_handler(ROAR_HANDLER)
dispatcher.add_handler(PUNCHME_HANDLER)

__mod_name__ = "BAN"
__handlers__ = [BAN_HANDLER, TEMPBAN_HANDLER, PUNCH_HANDLER, UNBAN_HANDLER, ROAR_HANDLER, PUNCHME_HANDLER]
