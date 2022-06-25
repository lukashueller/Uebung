from collections import Counter
from py_classes.models.MessageTypes import MessageTypes

class StatisticsPrinter():
    def print_statistics(self, preprocessed_chat, emojiArray, print_emojis) : 
        self.print_message_type_statistics(preprocessed_chat)
        self.print_emoji_statistics(emojiArray, print_emojis)

    def print_message_type_statistics(self, preprocessed_chat) :
        print(" --- MESSAGE TYPE STATISTICS:")
        print(" ---- Number of Messages in Chat: " + str(len(preprocessed_chat)))
        print(" ---- Number of TEXT MESSAGES send: " + str(sum(map(lambda x : x.message_type == MessageTypes.TEXT, preprocessed_chat))))
        print(" ---- Number of AUDIOS send: " + str(sum(map(lambda x : x.message_type == MessageTypes.AUDIO, preprocessed_chat))))
        print(" ---- Number of IMAGES send: " + str(sum(map(lambda x : x.message_type == MessageTypes.IMAGE, preprocessed_chat))))
        print(" ---- Number of VIDEOS send: " + str(sum(map(lambda x : x.message_type == MessageTypes.VIDEO, preprocessed_chat))))
        print(" ---- Number of GIFS send: " + str(sum(map(lambda x : x.message_type == MessageTypes.GIF, preprocessed_chat))))
        print(" ---- Number of STICKERS send: " + str(sum(map(lambda x : x.message_type == MessageTypes.STICKER, preprocessed_chat))))
        print(" ---- Number of DOCUMENTS send: " + str(sum(map(lambda x : x.message_type == MessageTypes.DOCUMENT, preprocessed_chat))))
        
    def print_emoji_statistics(self, emojiArray, print_emojis) :
        print(" --- EMOJI STATISTICS:")
        print(("{:<8} {:>8}").format('  EMOJI','NUMBER'))
        emojiCounter = Counter(emojiArray).most_common()

        for i, item in enumerate(emojiCounter) :
            print(("{:<8} {:>5}").format("    " + item[0], item[1]))
            if print_emojis != "all" and i == 10 : break 
