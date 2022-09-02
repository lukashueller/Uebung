import re
import emoji
import logging
import datetime
from py_classes.models.MessageTypes import MessageTypes

from pprint import pprint


class DirectChatReader:
    class DirectChatObject(object):
        def __init__(self, timestamp, person, message, messageType):
            self.timestamp = timestamp
            self.person = person
            self.message = message
            self.message_type = messageType

    chat = []
    emojiArray = []

    def read_chat(self, filepath: str):
        logging.info(" >>> START READ " + filepath)

        chat = open(filepath, mode='r', encoding='utf-8')
        lines = chat.readlines()
        chat.close()

        count = 0
        for line in lines:
            self.extract(line)
            count += 1

        logging.info(" >>> END READ " + filepath)
        return self.chat, self.emojiArray

    def extract(self, line: str):
        if re.match(r'\u200e?\[\d\d\.\d\d\.\d\d, \d\d:\d\d:\d\d\]', line):
            result = re.search(r'\[(.*?)\](.*?)\:(\s\S.*)', line)

            timestamp = result.group(1).strip().replace("\u200e", "")
            timestamp = datetime.datetime.strptime(timestamp, "%d.%m.%y, %H:%M:%S")
            person = result.group(2).strip().replace("\u200e", "")
            raw_message = result.group(3).strip()
            message = raw_message.replace("\u200e", "")
            emojis_from_message = ''.join(emoji.distinct_emoji_list(message))

            if len(emojis_from_message) != 0:
                for singleEmoji in emojis_from_message:
                    self.emojiArray.append(singleEmoji)

            message_type = self.return_message_type(raw_message)

            single_chat_line_object = self.DirectChatObject(timestamp, person, message, message_type)
            self.chat.append(single_chat_line_object)
        else:
            self.chat[-1].message = self.chat[-1].message + "\n" + line

    @staticmethod
    def return_message_type(message: str):
        if message == "\u200eaudio omitted" or "\u200eAudio weggelassen" in message:
            return MessageTypes.AUDIO
        elif message == "\u200eimage omitted" or "\u200eBild weggelassen" in message:
            return MessageTypes.IMAGE
        elif message == "\u200evideo omitted" or "\u200eVideo weggelassen" in message:
            return MessageTypes.VIDEO
        elif message == "\u200eGIF omitted" or "\u200eGIF weggelassen" in message:
            return MessageTypes.GIF
        elif message == "\u200esticker omitted" or "\u200eSticker weggelassen" in message:
            return MessageTypes.STICKER
        elif "\u200edocument omitted" in message or "\u200eDokument weggelassen" in message:
            return MessageTypes.DOCUMENT
        elif "\u200eLocation: " in message or "\u200eStandort: " in message:
            return MessageTypes.LOCATION
        elif "\u200eContact card omitted" in message or "\u200eKontaktkarte ausgelassen" in message:
            return MessageTypes.CONTACT
        elif "\u200e" in message: # catch all system messages and media messages in other languages
            return MessageTypes.OTHER
        else:
            return MessageTypes.TEXT
