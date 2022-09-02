import click
import logging
import coloredlogs

import curses

from py_classes.direct_chat_reader import DirectChatReader
from py_classes.statistics_printer import StatisticsPrinter
from py_classes.german_bert import BERT
from py_classes.ngram_predictor import NGRAM_Predictor


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
        logging.error(
            "You can only use either private or group chats at a time.")
    elif direct:
        chat_data = DirectChatReader().read_chat(path)

        if statistics:
            StatisticsPrinter().print_statistics(
                chat_data[0], chat_data[1], number_print_emojis, number_print_words)
        if interactive:
            next_word_prediction(chat_data[0])
    elif group:
        logging.error("Group chat analysis is not supported at the moment.")
    else:
        logging.error(
            "You have not what type of chat you want to analyse. Check --help for more information.")

    logging.info(" > WHATSAPP ANALYSER TERMINATED")


def next_word_prediction(chat_data):

    my_bert = BERT()
    my_ngram_predictor = NGRAM_Predictor(chat_data)

    my_ngram_predictor.predict_next_word("Hey maus ")

    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    curses.mousemask(1)
    stdscr.keypad(True)

    query = ""
    ngram_results = []
    bert_results = []
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Start typing: (Esc to quit) ", curses.A_REVERSE)
        stdscr.addstr(11, 0, query, )
        for i, res in enumerate(bert_results[:10]):
            try:
                stdscr.addstr(1+i, len(query), res, curses.COLOR_BLUE)
            except:
                pass

        for i, res in enumerate(ngram_results[:10]):
            try:
                stdscr.addstr(12+i, len(query), res, curses.COLOR_GREEN)
            except:
                pass

        event = stdscr.getch()
        if event == curses.KEY_MOUSE:
            _, _, my, _, _ = curses.getmouse()
            if 12 <= my < len(ngram_results[:10])+12:
                query += ngram_results[my-12]
            if 1 <= my < 11:
                query += bert_results[my-1]
        else:
            try:
                if event == 127:
                    query = query[:-1]
                elif event == 27:
                    break
                else:
                    key = chr(event)
                    query += key
            except:
                pass
        if query != "":
            ngram_results = my_ngram_predictor.predict_next_word(query)
            bert_results = my_bert.get_bert_predictions(query)

    # ending curses session
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


if __name__ == "__main__":
    logging.basicConfig(encoding='utf-8', level=logging.DEBUG)

    coloredlogs.install(level='INFO')

    main()
