from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer

from bisect import bisect_left
from py_classes.models.MessageTypes import MessageTypes


class NGRAM_Predictor:
    NGRAM_MAX = 5

    feature_matrix = None
    features = None
    sum_vec = None

    vectorizer = None

    def __init__(self, chat_data):
        docs = [message.message for message in chat_data if message.message_type == MessageTypes.TEXT]
        self.vectorizer = CountVectorizer(analyzer='word', tokenizer=TweetTokenizer().tokenize, ngram_range=(1, self.NGRAM_MAX), max_df=1.0, min_df=0.0,
                                     max_features=None)

        counts = self.vectorizer.fit_transform(docs)  # counts = document term matrix

        self.features = self.vectorizer.get_feature_names_out()
        self.sum_vec = counts.sum(axis=0).tolist()[0]
        self.feature_matrix = [(f, self.sum_vec[i]) for i, f in enumerate(self.features)] # This is already sorted

    def preprocess_input(self, text):
        tokenizer = self.vectorizer.build_tokenizer()
        preprocessor = self.vectorizer.build_preprocessor()
        return tokenizer(preprocessor(text))

    def predict_next_word(self, input_text):
        can_complete_word = input_text[-1:] != " "
        input_array = self.preprocess_input(input_text)
        return self.get_predictions(can_complete_word, input_array)

    def get_predictions(self, can_complete_word, input_array):
        preprocessed_input = input_array[-self.NGRAM_MAX:]
        results = []

        for ngram_length in range(len(preprocessed_input), 0, -1):
            sss = " ".join(preprocessed_input) + ("" if can_complete_word else " ")
            sse = sss[:-1] + chr(ord(sss[-1])+1)
            start_index = bisect_left(self.features, sss)
            end_index = bisect_left(self.features, sse)

            result = [
                (self.sum_vec[i], self.features[i][len(sss):] if len(sss) > 0 else " " + self.features[i], ngram_length)
                for i
                in range(start_index, end_index+1)
            ]

            result = [
                res
                for res
                in result
                if res[1].count(" ") <= ngram_length and res[1] != sss and res[1] != ""
            ]

            result = sorted(result, key=lambda x: -x[0])
            result = filter(lambda x: not x[1] in [res[1] for res in results], result)
            results += result

            preprocessed_input.pop(0)

            if len(results) >= 10:
                break
        return [result[1] for result in results]
