# WhatsAppSentimentAnalysis

### This project allows you to deeply evaluate your own WhatsApp chat history. 

## 1. What is the aim of the project?

Even though other messaging services such as Telegram or Threema are becoming increasingly popular worldwide, WhatsApp remains the world’s most popular messenger with more than two billion active users per month (as of 02/22) [[Source]](https://de.statista.com/themen/1973/instant-messenger). WhatsApp is followed by the Chinese messaging alternative WeChat and Facebook Messenger. However, all alternatives of the messenger WhatsApp, which now belongs to the META Group, are used daily by only 20% of the population in Germany. In a survey from 2021 [[Source]](https://www.messengerpeople.com/de/whatsapp-nutzerzahlen-deutschland), more than 60% of respondents said they use WhatsApp daily.

Many tools (such as WHATSAAN) allow only statistical analysis of the chat in terms of used words, emojis or the activity of the chat. Almost no other project tries to take a closer look at the content of a chat. Therefore, we decided to use Natural Language Processing (NLP) to analyze chat histories in more depth and set the following research questions for the project work:

## 2. Research questions
1. Is it possible to identify the topic(s) of a chat using NLP?
2. Is it possible to deduce what the communication is used for? (Work chat, friendly exchange, etc.)
3. Is it possible to analyze the sentiment of a chat using NLP?
## 3. How-To: Download WhatsApp chat history (iPhone)
1. Select the chat you are interested in and open it.
2. Click on the name of your chat partner / chat group to go to the information page of the chat.
3. Scroll down to the bottom and click on `Export Chat`.
4. Select `Without Media`.
5. A .zip archive of the chat has now been created. We recommend you to send the file directly to your MacBook via AirDrop. There you just need to unzip it in the appropriate folder and you can start analyzing.

*A tutorial on how to create the chat archive on Android will be available soon.*

## 4. Setup and Run WhatsApp sentiment Analyser 
**Clone repository and import data**  
*Advice: You don't need to export your own chat history to test our code. We have also provided two sample chat histories in the repository.*  
If you have your own chat histories, save them in the /data folder in the appropriate subfolder. The two subfolders are for differentiating between 1:1 chats and group chats.

**Install required modules:**
```console
sudo pip3 install Click
sudo pip3 install emoji
sudo pip3 install -U nltk
```

**Downloads Stopwords**
```console
python -m nltk.downloader stopwords
```

**Run the analyser**
```console
python3 main.py -d "example.txt"
```

**Specify the number of printed statistics**  
Display only the 5 most frequent occurrences:
```console
python3 main.py -d "example.txt" -e 5 -w 5
```
Display all occurences:
```console
python3 main.py -d "example.txt" -e "all" -w "all"
```

*Attention: currently the code only works with German or English WhatsApp exports!*

Check `--help` for more information.
