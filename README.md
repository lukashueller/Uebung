# WhatsAppWordPredicton & ChatAnalyzer

# TODOS
- remove direct and group chat flags
- check if the defaults are correct

### This project allows you to deeply evaluate your own WhatsApp chat history. 

## 1. What is the aim of the project?

Even though other messaging services such as Telegram or Threema are becoming increasingly popular worldwide, WhatsApp remains the world’s most popular messenger with more than two billion active users per month (as of 02/22) [[Source]](https://de.statista.com/themen/1973/instant-messenger). WhatsApp is followed by the Chinese messaging alternative WeChat and Facebook Messenger. However, all alternatives of the messenger WhatsApp, which now belongs to the META Group, are used daily by only 20% of the population in Germany. In a survey from 2021 [[Source]](https://www.messengerpeople.com/de/whatsapp-nutzerzahlen-deutschland), more than 60% of respondents said they use WhatsApp daily.

It is impressive that there are only a few tools that train NLP models based on chat histories of the world’s most popular messenger. Therefore in addition to a statistical analysis of chat histories, our tool enables the training of a next word prediction model that makes input suggestions based on the chat history and the pre-trained BERT model.

## 2. How-To: Download WhatsApp chat history (iPhone)
1. Select the chat you are interested in and open it.
2. Click on the name of your chat partner / chat group to go to the information page of the chat.
3. Scroll down to the bottom and click on `Export Chat`.
4. Select `Without Media`.
5. A .zip archive of the chat has now been created. We recommend you to send the file directly to your MacBook via AirDrop. There you just need to unzip it in the appropriate folder and you can start analyzing.

*A tutorial on how to create the chat archive on Android will be available soon.*

## 3. Setup and Run WhatsApp sentiment Analyser 
**Clone repository and import data**  
*Advice: You don't need to export your own chat history to test our code. We have also provided two sample chat histories in the repository.*  
If you have your own chat histories, save them in the /data folder in the appropriate subfolder. The two subfolders are for differentiating between 1:1 chats and group chats.

**Install required modules:**
```console
pip3 install -r requirements.txt
```

**Downloads Stopwords**
In order to run the script nltk must have downloaded the stopword list. To do this, run the following command:
```console
python -m nltk.downloader stopwords
```

This script has two main functions:
1. Analyze a Whatsapp-Chat and show interesting statistics, such as number of messages, most used emoijs and most used words (excluding stop-words).
2. An interactive tool, that predicts the next word or part of word. The prediction is based on the one hand on the BERT language model and on the other hand on a simple language model based on the data from the WhatsApp chat.

**Flags**
```console
-p, --path : path to the chat-export (txt-file)
-s, --statistics : flag to indicate, that the program should print chat statistics
-e, --emoji : specify the number of emojis the statistic should contain (default 10; -1 for all)
-w, --words : specify the number of words the statistic should contain (default 15; -1 for all]
-i, --interactive : flag to indicate, that the programm should start the interactive mode, with the next-word prediction
```

## Examples
**Show statistics for a direct chat**
```console
python3 main.py -p /data/direct_chats/example.txt -s
```

**Start interactive next word predictions for a direct chat**
```console
python3 main.py -p /data/direct_chats/example.txt -i
```

**Run the analyser**
```console
python3 main.py -p /data/direct_chats/example.txt
```

**Specify the number of printed statistics**  
Display only the 5 most frequent occurrences:
```console
python3 main.py -p /data/direct_chats/example.txt -e 5 -w 5
```
Display all occurences:
```console
python3 main.py -p /data/direct_chats/example.txt -e -1 -w -1
```

*Attention: currently the code only works with German or English WhatsApp exports!*
*The next word pretictions uses the german version of BERT, the chat-individual predictions works with both languages.*

Check `--help` for more information.
