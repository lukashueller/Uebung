import click
import logging
import coloredlogs
from sklearn.feature_extraction.text import CountVectorizer
from nltk.tokenize import TweetTokenizer


import curses

from py_classes.direct_chat_reader import DirectChatReader
from py_classes.statistics_printer import StatisticsPrinter
from py_classes.models.MessageTypes import MessageTypes


@click.command()
@click.option("-p", "--path", "path", type=str, help="The path of the text file to analyze", required=True)
@click.option("-d", "--direct", help="Analyze a private chat.", is_flag=True)
@click.option("-g", "--group", help="Analyze a group chat.", is_flag=True)
@click.option("-i", "--interactive", help="Interactively predict new words.", is_flag=True)
@click.option("-s", "--statistics", help="Show chat statistics.", is_flag=True)
@click.option("-e", "--emoji", "number_print_emojis", type=int, default=10,
              help="Type \"-1\" to get all emojis; otherwise only the requested number of most common emojis will be "
                   "displayed (default: 10)")
@click.option("-w", "--words", "number_print_words", type=int, default=15,
              help="type \"-1\" to get all words; otherwise only the requested number of most words emojis will be "
               "displayed (default: 15)")


def main(path: str, direct: bool, group: bool, interactive: bool, statistics: bool, number_print_emojis: int, number_print_words: int):
    logging.info(" > WHATSAPP ANALYSER STARTED")
    if direct and group:
        logging.error("You can only use either private or group chats at a time.")
    elif direct:
        chat_data = DirectChatReader().read_chat(path)

        if statistics:
            StatisticsPrinter().print_statistics(chat_data[0], chat_data[1], number_print_emojis, number_print_words)
        if interactive:
            next_word_prediction(chat_data[0])
    elif group:
        logging.error("Group chat analysis is not supported at the moment.")
    else:
        logging.error("You have not what type of chat you want to analyse. Check --help for more information.")

    logging.info(" > WHATSAPP ANALYSER TERMINATED")



def next_word_prediction(chat_data):
    NGRAM_MAX = 5

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.mousemask(1)
    stdscr.keypad(True)

    docs = [message.message for message in chat_data if message.message_type == MessageTypes.TEXT]
    vectorizer = CountVectorizer(analyzer='word', tokenizer=TweetTokenizer().tokenize, ngram_range=(1, NGRAM_MAX), max_df=1.0, min_df=0.0,
                                 max_features=None)

    counts = vectorizer.fit_transform(docs)  # counts = document term matrix

    features = vectorizer.get_feature_names_out()
    sum_vec = counts.sum(axis=0).tolist()[0]



    query = ""
    results = []
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Start typing: (Esc to quit) ", curses.A_REVERSE)
        stdscr.addstr(1, 0, query, )
        for i, res in enumerate(results[:10]):
            stdscr.addstr(2+i, len(query), res[1], )

        event = stdscr.getch()
        if event == curses.KEY_MOUSE:
            _, _, my, _, _ = curses.getmouse()
            if 2 <= my < len(results[:10])+2:
                query += results[my-2][1]
        else:
            try:
                key = chr(event)
                if key in ['KEY_BACKSPACE', '\b', '\x7f']:
                    query = query[:-1]
                if event == 27:
                    break
                else:
                    query += key
            except:
                pass
        can_complete_word = query[-1:] != " "
        results = get_predictions(can_complete_word, preprocess_input(query, vectorizer), NGRAM_MAX, features, sum_vec)

    # ending curses session
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


def preprocess_input(text, vectorizer):
    tokenizer = vectorizer.build_tokenizer()
    preprocessor = vectorizer.build_preprocessor()
    return tokenizer(preprocessor(text))


def get_predictions(can_complete_word, input_array, NGRAM_MAX, features, sum_vec):
    preprocessed_input = input_array[-NGRAM_MAX:]
    results = []

    for ngram_length in range(len(preprocessed_input), 0, -1):
        search_string = " ".join(preprocessed_input) + ("" if can_complete_word else " ")
        result = [
            (sum_vec[i], f[len(search_string):] if len(search_string) > 0 else " " + f, ngram_length)
            for (i, f)
            in enumerate(features)
            if f.startswith(search_string) and f.count(
                " ") <= ngram_length and f != search_string
        ]
        result = sorted(result, key=lambda x: -x[0])
        result = filter(lambda x: not x[1] in map(lambda x: x[1], results), result)
        results += result

        preprocessed_input.pop(0)

        if len(results) >= 10:
            break
    return results






if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    coloredlogs.install(level='DEBUG')

    logging.debug('DEBUG')
    logging.info('INFO')
    logging.warning('WARNUNG')
    logging.error('ERROR')
    logging.critical('CRITICAL')

    main()
