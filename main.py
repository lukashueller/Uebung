
import click

from direct_chat_reader import DirectChatReader

@click.command()
@click.option("-d", "--direct", "direct_chat_filename", type=str, help="The name of the text file to analyze the one to one whatsapp-chat")
@click.option("-g", "--group", "group_chat_filename", type=str, help="The name of the text file to analyze the group whatsapp-chat")

def run(direct_chat_filename : str, group_chat_filename : str) :
    print(" - WHATSAPP ANALYSER STARTED")
    if direct_chat_filename and group_chat_filename:
        print("You can only upload one chat at the moment.")
    elif direct_chat_filename :
        DirectChatReader().read_chat(direct_chat_filename)
    elif group_chat_filename : 
        print("Group chat analysis is not supportet at the moment.")
    else : 
        print("You have not specified a path to upload a chat history. Check --help for more information.")
    
    print(" - WHATSAPP ANALYSER TERMINATED")

if __name__ == "__main__":
    run()
