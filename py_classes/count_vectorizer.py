from collections import Counter
from py_classes.models.MessageTypes import MessageTypes
import nltk

from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

nltk.download('stopwords')

german_stop_words = nltk.corpus.stopwords.words('german')


class CountVectorizer_Printer():

    def print_count_vectorizer(self, preprocessed_chat):
        docs = []
        for message in preprocessed_chat:
            if message.message_type == MessageTypes.TEXT:
                docs.append(message.message)

        vectorizer = CountVectorizer(stop_words=frozenset(german_stop_words))
        vectors = vectorizer.fit_transform(docs)

        vector_dimensions = vectorizer.get_feature_names_out()

        dataframe = pd.DataFrame(data=vectors.toarray(),
                                 columns=vector_dimensions)

        print(" --- COUNT VECTORIZER")
        print(" ---- Vector Dataframe:")
        print(dataframe)

        count_vec = CountVectorizer(stop_words="english", analyzer='word', ngram_range=(
            1, 3), max_df=0.7, min_df=1, max_features=None)

        count_train = count_vec.fit(docs)

        print(" ---- ngram(1,3) List:")
        print(count_vec.get_feature_names())
