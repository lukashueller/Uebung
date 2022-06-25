import emoji
from collections import Counter
from py_classes.models.MessageTypes import MessageTypes
from sklearn.feature_extraction.text import CountVectorizer

class StatisticsPrinter():
    def print_statistics(self, preprocessed_chat, emojiArray, number_print_emojis, number_print_words) : 
        self.print_message_type_statistics(preprocessed_chat)
        self.print_emoji_statistics(emojiArray, number_print_emojis)
        self.print_word_count(preprocessed_chat, number_print_words)

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
        
    def print_emoji_statistics(self, emojiArray, number_print_emojis) :
        print(" --- EMOJI STATISTICS:")
        print(("{:<8} {:>8}").format('   EMOJI','NUMBER'))
        emojiCounter = Counter(emojiArray).most_common()

        for i, item in enumerate(emojiCounter) :
            if number_print_emojis is None and i > 10: break   # default number of displayed emojis
            if (number_print_emojis is not None) and (number_print_emojis != "all") and (int(number_print_emojis) == i) : break
            print(("{:<8} {:>5}").format("    " + item[0], item[1]))

    def print_word_count(self, preprocessed_chat, number_print_words):
        print(" --- WORD COUNT STATISTICS:")
        ## Source: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python (modified)
        def give_emoji_free_text(text):
            return emoji.get_emoji_regexp().sub(r'', text)

        messages_as_text = ""
        for message in preprocessed_chat:
            if message.message_type == MessageTypes.TEXT :
                message_text = give_emoji_free_text(message.message)
                for char in '-.,?\n':
                    message_text=message_text.replace(char,' ').lower()
                messages_as_text += message_text + " "

        wordsCounter = Counter(messages_as_text.split()).most_common()

        print(("{:<13} {:>10}").format('   WORD','     NUMBER'))
        for i, item in enumerate(wordsCounter) :
            if number_print_words is None and i > 15: break   # default number of displayed words
            if (number_print_words is not None) and (number_print_words != "all") and (int(number_print_words) == i) : break
            print(("{:<15} {:>8}").format("    " + item[0], item[1]))
