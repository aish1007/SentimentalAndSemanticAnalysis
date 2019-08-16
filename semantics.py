import re
from os import listdir
from os.path import isfile, join
import math

documentlist = [];

totalfiles = [f for f in listdir("reuters") if isfile(join("reuters", f))]
for fileidx,files in enumerate(totalfiles,start = 0):
    f = open("reuters/" + "reut2-"+str(fileidx)+".sgm", "r").read()
    extract = re.findall(r'(<BODY>(.*?)</BODY>)', f, flags=re.DOTALL)
    for idx, content in enumerate(extract):
        newcontent = content[1]
        newcontent = newcontent.replace("\n", " ")
        #removing symbols
        newcontent = re.sub('[^A-Za-z0-9 ]+', '', newcontent)
        newcontent = ' '.join(newcontent.split())
        #removing urls
        newcontent = re.sub(r"http\S+|http", '', newcontent)
        #stemming
        newcontent = re.sub(r"(ed\b|ly\b|es\b|ing\b)", " ", newcontent)
        file = {}
        file["docname"] =  str(idx)
        file["content"] = newcontent.lower()
        documentlist.append(file)


#calculating term frequency
print("calculaating term freq")
termfreq = {}
occurence = 0

#calculating unique words
for singlefiles in documentlist:
    content = singlefiles.get("content")
    words = content.split(" ")
    for word in words:
        word = word.lower()
        if not word in termfreq:
            termfreq.update({word:occurence})

#cslculating term occurence in all files
for singlefiles in documentlist:
    content = singlefiles.get("content")
    words = content.split(" ")
    fileUniq = []
    for word in words:
        word = word.lower()
        if not word in fileUniq:
            fileUniq.append(word)

    uniqwords = termfreq.keys()
    for unique in uniqwords:
        for word in fileUniq:
            if(unique == word):
                occurence = termfreq.get(word) + 1
                termfreq[word] = occurence

#calculating idf for all words
print("idf calculation")
idf = {}
for word in termfreq.keys():
    idfcal = math.log2(len(documentlist)/termfreq.get(word))
    idf[word] = idfcal

#multiplying tf and idf
print("multiplying tf and idf")
termfrewWords = termfreq.keys()
idfwords = idf.keys()
totalfiles = []
for singlefiles in documentlist:
    documentList = [];
    content = singlefiles.get("content")
    words = content.split(" ")
    uniqq = []
    for word in words:
        word = word.lower()
        if not word in uniqq:
            uniqq.append(word)

    for word in uniqq:
       for term in termfrewWords:
            for idfsingle in idfwords:
                if(word == term and word == idfsingle):
                    tfIdf = termfreq.get(word)*idf.get(word)
                    documentList.append({word:tfIdf})


    filenew = {}
    filenew["docname"] = singlefiles.get("docname")
    filenew["article"] = documentList
    totalfiles.append(filenew)

#calculating doc distance
print("calculating doc distance")
distanceList = []
for files in totalfiles:
    arr = files.get("article")
    docname = files.get('docname')
    distance = 0
    for allwords in arr:
        wordkeys = allwords.keys()
        for word in wordkeys:
         distance = distance + (allwords.get(word)**2)
         sqrt = math.sqrt(distance)
    #distanceList.append({docname:sqrt})
    distanceList.append({"docname":docname, "distance" : sqrt})

#calculating query distance
print("calculating query distance")
queryTF = termfreq.get("canada")
querytfIDF = 0
arrlist = totalfiles[0].get('article')
for word in arrlist:
    obj = word.keys()
    for o in obj:
        if(o == 'canada'):
            querytfIDF = word.get('canada')

#calculating qd
qd = (1/queryTF)*(querytfIDF)
if(qd >= 0):
    qd = math.sqrt(qd)
else:
    qd=0

#calculating cosine similarity
docCosineList = []
for idx,file in enumerate(totalfiles,start = 1):
    arr = file.get('article')
    docname = file.get('docname')
    for word in arr:
        for dist in distanceList:
            obj = word.keys()
            for o in obj:
              if(o == 'canada'):
               if(dist.get("docname") == docname):
                   dist = dist.get("distance")
                   x = querytfIDF * qd
                   y = dist * qd
                   cosine = 0
                   if(x!=0 and y!=0):
                       cosine = (x / y)
                       file = {}
                       file["docname"]=docname
                       file["cosine"]=cosine
                       docCosineList.append(file)


print("ranked documents")
print(docCosineList)

newlist = sorted(docCosineList, key=lambda m: m['cosine'],reverse=True)
topfile = newlist[0].get('docname')
outputsemantics = open("semanticsoutput.txt","w+")
for file in documentlist:
    if(file.get("docname") == topfile):
        print("DOCUMENT NUMBER - ", file.get("docname"))
        print("CONTENT -",file.get("content"))
        outputcontent = file.get("content")
        outputsemantics.write(outputcontent)






