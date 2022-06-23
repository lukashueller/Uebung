import re
import emoji
from enum import Enum
from collections import Counter

from pprint import pprint

class DirectChatReader():
    class MessageTypes(Enum):
        TEXT = 1
        AUDIO = 2
        IMAGE = 3
        VIDEO = 4
        GIF = 5
        STICKER = 6
        DOCUMENT = 7
    
    class directChatObject(object):
        def __init__(self, timestamp, person, message, messageType):
            self.timestamp = timestamp
            self.person = person
            self.message = message
            self.message_type = messageType
    
    chat = []
    emojiArray = []
    emojiDict = {}

    def read_chat(self, filename:str) :
        print(" --- START READ " + filename)

        chat = open('data/direct_chats/'+filename, mode = 'r', encoding='utf-8')
        Lines = chat.readlines()
        chat.close()

        count = 0
        for line in Lines:
            #if count % 100 == 0 : print(count)
            #if count == 35 : break # JUST FOR DEBUGGING (Interrupt after 5 lines)

            self.extract(line, count)
            count += 1

        if self.chat[0].message.startswith("Messages and calls are end-to-end encrypted.") or self.chat[0].message.startswith("Nachrichten und Anrufe sind Ende-zu-Ende-verschlüsselt.") : 
            self.chat.pop(0)

        """ for line in self.chat : 
            pprint(vars(line)) """

        print(" --- END READ " + filename)

        self.print_statistics()

    def extract(self, line:str, count:int) : 
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
            return self.MessageTypes.AUDIO
        elif "image omitted" in message or "Bild weggelassen" in message: 
            return self.MessageTypes.IMAGE
        elif "video omitted" in message or "Video weggelassen" in message: 
            return self.MessageTypes.VIDEO
        elif "GIF omitted" in message or "GIF weggelassen" in message: 
            return self.MessageTypes.GIF
        elif "sticker omitted" in message or "Sticker weggelassen" in message: 
            return self.MessageTypes.STICKER
        elif "document omitted" in message or "Dokument weggelassen" in message: 
            return self.MessageTypes.DOCUMENT
        else :
            return self.MessageTypes.TEXT

    def print_statistics(self) : 
        print(" --- MESSAGE TYPE STATISTICS:")
        print(" ---- Number of Messages in Chat: " + str(len(self.chat)))
        print(" ---- Number of TEXT MESSAGES send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.TEXT, self.chat))))
        print(" ---- Number of AUDIOS send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.AUDIO, self.chat))))
        print(" ---- Number of IMAGES send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.IMAGE, self.chat))))
        print(" ---- Number of VIDEOS send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.VIDEO, self.chat))))
        print(" ---- Number of GIFS send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.GIF, self.chat))))
        print(" ---- Number of STICKERS send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.STICKER, self.chat))))
        print(" ---- Number of DOCUMENTS send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.DOCUMENT, self.chat))))
        
        print(" --- EMOJI STATISTICS:")
        print(("{:<8} {:>8}").format('  EMOJI','NUMBER'))
        emojiCounter = Counter(self.emojiArray)
        emojiCounter = emojiCounter.most_common()
        for item in emojiCounter:
            print(("{:<8} {:>5}").format("    " + item[0], item[1]))

