import re
from enum import Enum

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

    def read_chat(self, filename:str) :
        print(" --- START READ " + filename)

        chat = open('data/direct_chats/'+filename, mode = 'r', encoding='utf-8')
        Lines = chat.readlines()
        chat.close()

        count = 0
        for line in Lines:
            #if count % 100 == 0 : print(count)
            if count == 35 : break # JUST FOR DEBUGGING (Interrupt after 5 lines)

            self.extract(line)
            count += 1

        if self.chat[0].message.startswith("Messages and calls are end-to-end encrypted.") : 
            self.chat.pop(0)

        """ for line in self.chat : 
            pprint(vars(line)) """

        self.print_statistics()

        print(" --- END READ " + filename)

    def extract(self, line:str) : 
        # check if this line is a new message
        if re.match(r'^\[\d\d\.\d\d\.\d\d, \d\d:\d\d:\d\d\]', line) :
            result = re.search(r'^\[(.*?)\](.*?)\:(\s\S.*)', line)
            
            timestamp = result.group(1).strip().replace("\u200e","")
            person = result.group(2).strip().replace("\u200e","")
            message = result.group(3).strip().replace("\u200e","")
            
            message_type = self.return_message_type(message)

            singleChatLineObject = self.directChatObject(timestamp, person, message, message_type)
            self.chat.append(singleChatLineObject)
        else :
            self.chat[-1].message = self.chat[-1].message + "\n" + line

    def return_message_type(self, message:str) : 
        if "audio omitted" in message : 
            return self.MessageTypes.AUDIO
        elif "image omitted" in message : 
            return self.MessageTypes.IMAGE
        elif "video omitted" in message : 
            return self.MessageTypes.VIDEO
        elif "GIF omitted" in message : 
            return self.MessageTypes.GIF
        elif "sticker omitted" in message : 
            return self.MessageTypes.STICKER
        elif "document omitted" in message : 
            return self.MessageTypes.DOCUMENT
        else :
            return self.MessageTypes.TEXT

    def print_statistics(self) : 
        print(" ---- Number of Messages in Chat: " + str(len(self.chat)))
        print(" ---- Number of TEXT MESSAGES send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.TEXT, self.chat))))
        print(" ---- Number of IMAGES send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.IMAGE, self.chat))))
        print(" ---- Number of GIFS send: " + str(sum(map(lambda x : x.message_type == self.MessageTypes.GIF, self.chat))))



