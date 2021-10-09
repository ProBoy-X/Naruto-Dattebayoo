from functools import wraps

from telegram import Bot, Chat, ChatMember, Update, ParseMode

from Naruto import dispatcher, DEL_CMDS, WHITELIST_USERS, TIGER_USERS, SUPPORT_USERS, SUDO_USERS, DEV_USERS


def is_whitelist_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return any(user_id in user for user in [WHITELIST_USERS, TIGER_USERS, SUPPORT_USERS, SUDO_USERS, DEV_USERS])


def is_support_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return user_id in SUPPORT_USERS or user_id in SUDO_USERS or user_id in DEV_USERS


def is_sudo_plus(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    return user_id in SUDO_USERS or user_id in DEV_USERS


def is_user_admin(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (chat.type == 'private'
            or user_id in SUDO_USERS
            or user_id in DEV_USERS
            or chat.all_members_are_administrators):
        return True

    if not member:
        member = chat.get_member(user_id)

    return member.status in ('administrator', 'creator')


def is_bot_admin(chat: Chat, bot_id: int, bot_member: ChatMember = None) -> bool:
    if chat.type == 'private' or chat.all_members_are_administrators:
        return True

    if not bot_member:
        bot_member = chat.get_member(bot_id)

    return bot_member.status in ('administrator', 'creator')


def can_delete(chat: Chat, bot_id: int) -> bool:
    return chat.get_member(bot_id).can_delete_messages


def is_user_ban_protected(chat: Chat, user_id: int, member: ChatMember = None) -> bool:
    if (chat.type == 'private'
            or user_id in SUDO_USERS
            or user_id in DEV_USERS
            or user_id in WHITELIST_USERS
            or user_id in TIGER_USERS
            or chat.all_members_are_administrators):
        return True

    if not member:
        member = chat.get_member(user_id)

    return member.status in ('administrator', 'creator')


def is_user_in_chat(chat: Chat, user_id: int) -> bool:
    member = chat.get_member(user_id)
    return member.status not in ('left', 'kicked')


def dev_plus(func):
    @wraps(func)
    def is_dev_plus_func(bot: Bot, update: Update, *args, **kwargs):

        user = update.effective_user

        if user.id in DEV_USERS:
            return func(bot, update, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()
        else:
            update.effective_message.reply_text("ᴘᴇʀᴍɪssɪᴏɴ ɴɪ ʜ ᴀᴘᴋᴏ ʏᴇ ᴄᴏᴍᴍᴀɴᴅ ᴅᴇɴᴇ ᴋɪ..")

    return is_dev_plus_func


def sudo_plus(func):
    @wraps(func)
    def is_sudo_plus_func(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat

        if user and is_sudo_plus(chat, user.id):
            return func(bot, update, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()
        else:
            update.effective_message.reply_text("ᴄʜᴜᴘᴘ ᴋʀ.. ᴀᴅᴍɪɴ ʙᴀɴᴊᴀ ᴘʜʟᴇ ғɪʀ ᴄᴏᴍᴍᴀɴᴅ ᴅᴇɴᴀ ᴍᴜᴊʜᴇ.!!")

    return is_sudo_plus_func


def support_plus(func):
    @wraps(func)
    def is_support_plus_func(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat

        if user and is_whitelist_plus(chat, user.id):
            return func(bot, update, *args, **kwargs)
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()

    return is_support_plus_func


def whitelist_plus(func):
    @wraps(func)
    def is_whitelist_plus_func(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat

        if user and is_whitelist_plus(chat, user.id):
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text("ᴀᴘᴋᴇ ᴘᴀss ᴀᴄᴄᴇss ɴɪ ʜ ʏᴇ ᴜsᴇ ᴋʀɴᴀ ᴋᴀ..\nғᴏʀ ᴀɴʏ ʜᴇʟᴘ ᴊᴏɪɴ @DatteBayooSupport")

    return is_whitelist_plus_func


def user_admin(func):
    @wraps(func)
    def is_admin(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat

        if user and is_user_admin(chat, user.id):
            return func(bot, update, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()
        else:
            update.effective_message.reply_text("ᴄʜᴜᴘᴘ ᴋʀ.. ᴀᴅᴍɪɴ ʙᴀɴᴊᴀ ᴘʜʟᴇ ғɪʀ ᴄᴏᴍᴍᴀɴᴅ ᴅᴇɴᴀ ᴍᴜᴊʜᴇ.!!")

    return is_admin


def user_admin_no_reply(func):
    @wraps(func)
    def is_not_admin_no_reply(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat

        if user and is_user_admin(chat, user.id):
            return func(bot, update, *args, **kwargs)
        elif not user:
            pass
        elif DEL_CMDS and " " not in update.effective_message.text:
            update.effective_message.delete()

    return is_not_admin_no_reply


def user_not_admin(func):
    @wraps(func)
    def is_not_admin(bot: Bot, update: Update, *args, **kwargs):
        user = update.effective_user
        chat = update.effective_chat

        if user and not is_user_admin(chat, user.id):
            return func(bot, update, *args, **kwargs)
        elif not user:
            pass

    return is_not_admin


def bot_admin(func):
    @wraps(func)
    def is_admin(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat
        update_chat_title = chat.title
        message_chat_title = update.effective_message.chat.title

        if update_chat_title == message_chat_title:
            not_admin = "ᴀᴅᴍɪɴ ɴɪ ʙᴀɴᴀʏᴀ ᴍᴜᴊʜᴇ ɪɴ ʟᴏɢᴏ ɴᴇ..🥺"
        else:
            not_admin = f"ᴀᴅᴍɪɴ ɴɪ ʙᴀɴᴀʏᴀ ᴍᴜᴊʜᴇ ɪɴ ʟᴏɢᴏ ɴᴇ..🥺 <b>{update_chat_title}</b>! ɪss ɢʀᴜᴘ ᴍ.."

        if is_bot_admin(chat, bot.id):
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(not_admin, parse_mode=ParseMode.HTML)

    return is_admin


def bot_can_delete(func):
    @wraps(func)
    def delete_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat
        update_chat_title = chat.title
        message_chat_title = update.effective_message.chat.title

        if update_chat_title == message_chat_title:
            cant_delete = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ.."
        else:
            cant_delete = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ <b>{update_chat_title}</b>! ɪss ɢʀᴏᴜᴘ ᴍ.."

        if can_delete(chat, bot.id):
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(cant_delete, parse_mode=ParseMode.HTML)

    return delete_rights


def can_pin(func):
    @wraps(func)
    def pin_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat
        update_chat_title = chat.title
        message_chat_title = update.effective_message.chat.title

        if update_chat_title == message_chat_title:
            cant_pin = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ.."
        else:
            cant_pin = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ <b>{update_chat_title}</b>! ɪss ɢʀᴏᴜᴘ ᴍ.."

        if chat.get_member(bot.id).can_pin_messages:
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(cant_pin, parse_mode=ParseMode.HTML)

    return pin_rights


def can_promote(func):
    @wraps(func)
    def promote_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat
        update_chat_title = chat.title
        message_chat_title = update.effective_message.chat.title

        if update_chat_title == message_chat_title:
            cant_promote = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ.."
        else:
            cant_promote = (f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ <b>{update_chat_title}</b>! ɪss ɢʀᴏᴜᴘ ᴍ.")
            

        if chat.get_member(bot.id).can_promote_members:
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(cant_promote, parse_mode=ParseMode.HTML)

    return promote_rights


def can_restrict(func):
    @wraps(func)
    def restrict_rights(bot: Bot, update: Update, *args, **kwargs):
        chat = update.effective_chat
        update_chat_title = chat.title
        message_chat_title = update.effective_message.chat.title

        if update_chat_title == message_chat_title:
            cant_restrict = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ.."
        else:
            cant_restrict = f"sᴏʀʀʏ🥺 ʀɪɢʜᴛ ɴɪ ʜ ᴍᴇʀᴇ ᴘᴀss.. ᴀᴅᴍɪɴ ʙᴀɴᴀᴏ ᴏʀ ғᴜʟʟ ʀɪɢʜᴛs ᴅᴏᴏ <b>{update_chat_title}</b>! ɪss ɢʀᴏᴜᴘ ᴍ.."

        if chat.get_member(bot.id).can_restrict_members:
            return func(bot, update, *args, **kwargs)
        else:
            update.effective_message.reply_text(cant_restrict, parse_mode=ParseMode.HTML)

    return restrict_rights


def connection_status(func):
    @wraps(func)
    def connected_status(bot: Bot, update: Update, *args, **kwargs):
        conn = connected(bot, update, update.effective_chat, update.effective_user.id, need_admin=False)

        if conn:
            chat = dispatcher.bot.getChat(conn)
            update.__setattr__("_effective_chat", chat)
            return func(bot, update, *args, **kwargs)
        else:
            if update.effective_message.chat.type == "private":
                update.effective_message.reply_text("/connect ʙʜᴇᴊᴏ ᴊɪs ɢʀᴏᴜᴘ ᴍ ᴀᴀᴘ ᴏʀ ᴍᴀɪ ᴄᴏᴍᴍᴏɴ ʜᴀɪ..")
                return connected_status

            return func(bot, update, *args, **kwargs)

    return connected_status


# Workaround for circular import with connection.py
from Naruto.modules import connection

connected = connection.connected
