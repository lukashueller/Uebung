import emoji
from collections import Counter
import logging

import numpy as np

from py_classes.models.MessageTypes import MessageTypes
from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import TfidfTransformer


class StatisticsPrinter:
    german_stop_words = stopwords.words('german')

    def print_statistics(self, preprocessed_chat, emoji_array, number_print_emojis, number_print_words):
        chat_text_data = [chat for chat in preprocessed_chat if
                          chat.message_type == MessageTypes.TEXT]  # only contains TEXT messages

        self.print_message_type_statistics(preprocessed_chat)
        self.print_emoji_statistics(emoji_array, number_print_emojis)
        self.print_word_count(preprocessed_chat, number_print_words)

    @staticmethod
    def print_message_type_statistics(preprocessed_chat):
        print(" --- MESSAGE TYPE STATISTICS:")
        print(" ---- Chat Duration: " + str(
            (preprocessed_chat[-1].timestamp - preprocessed_chat[0].timestamp)) + " (" + str(
            preprocessed_chat[0].timestamp.date()) + " - " + str(preprocessed_chat[-1].timestamp.date()) + ")")
        print(" ---- Number of Messages in Chat: " + str(len(preprocessed_chat)))
        print(" ---- Number of TEXT MESSAGES send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.TEXT, preprocessed_chat))))
        print(" ---- Number of AUDIOS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.AUDIO, preprocessed_chat))))
        print(" ---- Number of IMAGES send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.IMAGE, preprocessed_chat))))
        print(" ---- Number of VIDEOS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.VIDEO, preprocessed_chat))))
        print(" ---- Number of GIFS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.GIF, preprocessed_chat))))
        print(" ---- Number of STICKERS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.STICKER, preprocessed_chat))))
        print(" ---- Number of DOCUMENTS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.DOCUMENT, preprocessed_chat))))
        print(" ---- Number of CONTACTS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.CONTACT, preprocessed_chat))))
        print(" ---- Number of LOCATIONS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.LOCATION, preprocessed_chat))))
        print(" ---- Number of OTHERS send: " + str(
            sum(map(lambda x: x.message_type == MessageTypes.OTHER, preprocessed_chat))))

    @staticmethod
    def print_emoji_statistics(emoji_array, number_print_emojis):
        print(" --- EMOJI STATISTICS:")
        print("{:>8} {:>8}".format('EMOJI', 'NUMBER'))
        emoji_counter = Counter(emoji_array).most_common()

        for i, item in enumerate(emoji_counter):
            if i >= int(number_print_emojis):
                break
            print("{:>5} {:>8}".format(item[0], item[1]))

    def print_word_count(self, preprocessed_chat, number_print_words):
        print(" --- WORD COUNT STATISTICS:")

        # Source: https://stackoverflow.com/questions/33404752/removing-emojis-from-a-string-in-python (modified)
        def give_emoji_free_text(text):
            return emoji.replace_emoji(text, replace='')

        messages_as_text = ""
        for message in preprocessed_chat:
            if message.message_type == MessageTypes.TEXT:
                message_text = give_emoji_free_text(message.message)
                for char in '-.,?\n':
                    message_text = message_text.replace(char, ' ').lower()
                messages_as_text += message_text + " "

        word_counter = Counter(messages_as_text.split()).most_common()
        word_counter = self.word_counter_wo_stop_words(word_counter)
        print("   NUMBER OF DIFFERENT WORDS:" + str(len(word_counter)))

        print("{:^13} {:^12}".format('WORD', 'NUMBER'))
        for i, item in enumerate(word_counter):
            if (number_print_words != "all") and (int(number_print_words) == i):
                break
            print("    {0:<9} {1:>8}".format(item[0], item[1]))

    def word_counter_wo_stop_words(self, word_counter):
        def filter_stop_words(item):
            if item[0] in self.german_stop_words:
                return False
            else:
                return True

        filtered_words = list(filter(filter_stop_words, word_counter))
        print(" ---- FILTERED " + str(len(word_counter) - len(filtered_words)) + " stop words. (" + str(
            len(self.german_stop_words)) + " were possible)")
        return filtered_words

    """
    #TODO
    - use tuple based on sender -> A always writes "Hey B" and vice versa
    - use BERT
        - can we combine BERT and a custom solution? Maybe weighted: Bert 50% and most used tuples 50%
    """
