import nltk
import re
import json


from collections import Counter
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

#reading negative words from file
negFile = open("negativeWords.txt", "r")
negText = negFile.read()
negTokens = negText.split("\n")

#reading positive words from file
posFile = open("positiveWords.txt","r")
posText = posFile.read()
posTokens = posText.split("\n")


tweetFile = open("tweets.json","r").read()
f = open("sentimentaloutputfinal.json","w+")
tweets = eval(tweetFile)

output = []
for tweet in tweets:
    polarityCount = 0
    posCounter = 0
    negCounter = 0
    tweetTxt = tweet.get("text")
    #removing symbols
    tweetTxt = re.sub('[^a-z0-9A-Z ]+', '', tweetTxt)
    #removing urls
    tweetTxt = re.sub(r"http\S+|http", '', tweetTxt)
    #removing stopwords
    tweetTxt = re.sub(r'\b(' + 'is|was|the|there|here|what|which|who|whom|this|there|that|these|those' + r')\b\s*', '', tweetTxt.lower())
    #stemming
    tweetTxt = re.sub(r"(ed\b|ly\b|es\b|ing\b)", " ", tweetTxt)
    tokens = nltk.word_tokenize(tweetTxt)
    new_token = nltk.pos_tag(tokens)
    adj = [];
    str = '';
    for idx, token in enumerate(new_token):
        if ((token[1] == 'JJ' or token[1] =='JJR' or token[1]=='JJS' )and ((new_token[idx - 1][0] == 'not') or ((new_token[idx - 1][1] == 'DT' or new_token[idx - 1][1] == 'IN') and new_token[idx - 2][0] == 'not'))):
            str = 'not' + token[0]
            adj.append(str)
        elif (token[1] == 'JJ' or token[1] =='JJR' or token[1]=='JJS'):
            adj.append(token[0])

    for word in adj:
        for pos in posTokens:
            #changing case
            if (word.lower() == 'not' + pos):
                negCounter = negCounter + 1
            if(word.lower() == pos):
                posCounter = posCounter + 1

    for word in adj:
        for neg in negTokens:
            if (word.lower() == 'not' + neg):
                posCounter = posCounter + 1
            if (word.lower() == neg):
                negCounter = negCounter + 1

    polarityCount = posCounter - negCounter

    if (polarityCount > 0):
        polarity = "positive"
    elif (polarityCount < 0):
        polarity = "negative"
    else:
        polarity = "neutral"


    polar = {}
    polar[tweetTxt] = polarity
    output.append(polar)
f.write(json.dumps(output))




















