# SentimentalAndSemanticAnalysis

### Sentimental Analysis

 - Sentimental analysis was performed from the raw data collected with twitter search API. 
   
 -  Regular expressions were used for cleaning the
   raw data
   - POS tagging is done with NLTK Library
- The tweets were analysed as positive or negative from the words tagged as adjectives and it is compared with a list of positive and negative words.
- The output is a JSON file with tweets along with its polarity .

### Semantic Analysis

 - Semantic analysis was performed for the historical news data to
   retrieve the document with a specific keyword by ranking them based  on cosine similarity and document distance. 
- Regular expressions were  used to: - retrieve the articles from the SGM files, stemming,cleaning the extracted files by removing urls, symbols.
- The concept of vector space model was used to determine TF-IDF Frequency of the documents.
   


