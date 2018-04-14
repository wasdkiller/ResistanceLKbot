# -*- coding: utf-8 -*-
import configuration
import common
import dbFunction

admin = configuration.admin

def privateDocument(bot, message):
    if(message.from_user.id == admin and message.reply_to_message != None):
        try:
            bot.send_document(chat_id=message.reply_to_message.forward_from.id, data=message.document.file_id, caption=message.caption, parse_mode='HTML')
        except:
            print('Cannot send message to pm user')
        return
    if(message.from_user.id != admin):
        bot.forward_message(chat_id=admin, from_chat_id=message.chat.id, message_id=message.message_id)

def mentionAll(bot, message):
    if (common.checkAdmin(bot, message.chat.id, message.from_user.id)):
        if(message.chat.type != 'private'):
            mentionedUser = common.getName(message.from_user)
            text = mentionedUser + ' @ <b>' + message.chat.title + '</b> : ' + message.caption
            for userid in dbFunction.getAllUsers(message.chat.id):
                try:
                    bot.send_document(chat_id=userid, data=message.document.file_id, caption=text, parse_mode='HTML')
                except:
                    print('@all mention failed')

def mentionOne(bot, message):
    if (message.chat.type != 'private'):
        listUser = common.mentionedList(message.chat.id, message.caption)
        if (message.reply_to_message != None):
            if (message.reply_to_message.from_user.is_bot == False):
                if (dbFunction.isAvailable(message.chat.id, message.reply_to_message.from_user.id)):
                    try:
                        bot.send_message(chat_id=message.reply_to_message.from_user.id,
                                         text=common.getName(
                                             message.from_user) + ' @ <b>' + message.chat.title + '</b> : reply as a Photo',
                                         parse_mode='HTML')
                    except:
                        print('reply to photo failed')
                    listUser.append(str(message.reply_to_message.from_user.id))
                    listUser = list(set(listUser))
        if(len(listUser)>0):
            mentionedUser = common.getName(message.from_user)
            text = mentionedUser + ' @ <b>' + message.chat.title + '</b> : ' + message.caption
            for uname in listUser:
                try:
                    bot.send_document(chat_id=uname, data=message.document.file_id, caption=text, parse_mode='HTML')
                except:
                    print('single mention/subscribe failed')