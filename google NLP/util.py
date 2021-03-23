# Imports the Google Cloud client library
from google.cloud import language_v1


# Instantiates a client

def  get_sentiments(text):
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment 
    result = process_score(sentiment)   
    return result, sentiment.score, sentiment.magnitude

def process_score(sentiment):
    """
    threshold for negative and positive or mix sentiment
    NOTE: we are not considering magnitude in sentiment score
    """
    
    if sentiment.score == 0:
        return "neutral"
    elif sentiment.score > 0:
        return "positive"
    else:
        return "negative"
    
    