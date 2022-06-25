import click

from py_classes.direct_chat_reader import DirectChatReader
from py_classes.statistics_printer import StatisticsPrinter

@click.command()
@click.option("-d", "--direct", "direct_chat_filename", type=str, help="The name of the text file to analyze the one to one whatsapp-chat")
@click.option("-g", "--group", "group_chat_filename", type=str, help="The name of the text file to analyze the group whatsapp-chat")
@click.option("-e", "--emoji", "print_emojis", type=str, help="type \"all\" to get all emojis; otherwise only the 10 most common emojis will be displayed")

def run(direct_chat_filename : str, group_chat_filename : str, print_emojis : str) :
    print(" - WHATSAPP ANALYSER STARTED")
    if direct_chat_filename and group_chat_filename:
        print("You can only upload one chat at the moment.")
    elif direct_chat_filename :
        chat_data = DirectChatReader().read_chat(direct_chat_filename)
        print(chat_data[1])
        StatisticsPrinter().print_statistics(chat_data[0], chat_data[1], print_emojis)
    elif group_chat_filename : 
        print("Group chat analysis is not supportet at the moment.")
    else : 
        print("You have not specified a path to upload a chat history. Check --help for more information.")
    
    print(" - WHATSAPP ANALYSER TERMINATED")

if __name__ == "__main__":
    run()
