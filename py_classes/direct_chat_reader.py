import re
import emoji
from py_classes.models.MessageTypes import MessageTypes

from pprint import pprint

class DirectChatReader():
    class directChatObject(object):
        def __init__(self, timestamp, person, message, messageType):
            self.timestamp = timestamp
            self.person = person
            self.message = message
            self.message_type = messageType
    
    chat = []
    emojiArray = []

    def read_chat(self, filename:str) :
        print(" --- START READ " + filename)

        chat = open('data/direct_chats/'+filename, mode = 'r', encoding='utf-8')
        Lines = chat.readlines()
        chat.close()

        count = 0
        for line in Lines:
            #if count == 5 : break # JUST FOR DEBUGGING (Interrupt after 5 lines)

            self.extract(line)
            count += 1

        if self.chat[0].message.startswith("Messages and calls are end-to-end encrypted.") or self.chat[0].message.startswith("Nachrichten und Anrufe sind Ende-zu-Ende-verschlüsselt.") : 
            # Currently, we only check whether the switch to E:E Encryption took place at the start of the chat. Here it would have to be iterated over self.chat()
            self.chat.pop(0)

        """ for line in self.chat : 
            pprint(vars(line)) """

        print(" --- END READ " + filename)
        return self.chat, self.emojiArray

    def extract(self, line:str) : 
        if re.match(r'\[\d\d\.\d\d\.\d\d, \d\d:\d\d:\d\d\]', line) or " omitted" in line or " weggelassen" in line: # THIS IS CURRENTLY A WORKAROUND ... DONT KNOW WHY THE REGEX ISTN'T WORKING
            result = re.search(r'\[(.*?)\](.*?)\:(\s\S.*)', line)
            
            timestamp = result.group(1).strip().replace("\u200e","")
            person = result.group(2).strip().replace("\u200e","")
            message = result.group(3).strip().replace("\u200e","")
            emojisFromMessage = ''.join(c for c in message if c in emoji.UNICODE_EMOJI['en'])

            if len(emojisFromMessage) != 0 :
                for singleEmoji in emojisFromMessage : 
                    self.emojiArray.append(singleEmoji)
            
            message_type = self.return_message_type(message)

            singleChatLineObject = self.directChatObject(timestamp, person, message, message_type)
            self.chat.append(singleChatLineObject)
        else :
            self.chat[-1].message = self.chat[-1].message + "\n" + line

    def return_message_type(self, message:str) : 
        if "audio omitted" in message or "Audio weggelassen" in message: 
            return MessageTypes.AUDIO
        elif "image omitted" in message or "Bild weggelassen" in message: 
            return MessageTypes.IMAGE
        elif "video omitted" in message or "Video weggelassen" in message: 
            return MessageTypes.VIDEO
        elif "GIF omitted" in message or "GIF weggelassen" in message: 
            return MessageTypes.GIF
        elif "sticker omitted" in message or "Sticker weggelassen" in message: 
            return MessageTypes.STICKER
        elif "document omitted" in message or "Dokument weggelassen" in message: 
            return MessageTypes.DOCUMENT
        else :
            return MessageTypes.TEXT
