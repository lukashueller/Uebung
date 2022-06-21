import re
#from pprint import pprint

class DirectChatReader():
    class directChatObject(object):
        def __init__(self, timestamp, person, text):
            self.timestamp = timestamp
            self.person = person
            self.text = text
    
    chat = []

    def read_chat(self, filename:str) :
        print(" --- START READ " + filename)

        chat = open('data/direct_chats/'+filename, mode = 'r', encoding='utf-8')
        Lines = chat.readlines()
        chat.close()

        count = 0
        for line in Lines:
            #if count % 1000 == 0 : print(count)
            #if count == 100 : break # JUST FOR DEBUGGING (Interrupt after 5 lines)

            self.extract(line)
            count += 1

        if self.chat[0].text.startswith("Messages and calls are end-to-end encrypted.") : 
            self.chat.pop(0)

        #for line in self.chat : 
        #    pprint(vars(line))

        print(" --- END READ " + filename)

    def extract(self, line:str) : 
        #print(re.split(']|:', line, 2))
        if line.startswith("[") :
            result = re.search(r'\[(.*?)\](.*?)\:(\s\S.*)', line)
            
            singleChatLineObject = self.directChatObject(
                result.group(1).strip().replace("\u200e",""),
                result.group(2).strip().replace("\u200e",""),
                result.group(3).strip().replace("\u200e","")
            )
            self.chat.append(singleChatLineObject)
        else :
            self.chat[-1].text = self.chat[-1].text + "\n" + line
