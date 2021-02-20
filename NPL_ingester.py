import json
from google.cloud import language

def NLP_analysis(filename):
  if filename=="":
    return print("301-file does not exist")

  with open('event.json') as f:
    data=json.load(f)


  for x in data:
    if x["File_name"]==filename:
      client =language.client()
      document=client.document_text(x["content metdata"]["text"])
      sent_analysis=document.analyze_sentiment()
      x["content metdata"]["sentiment"]=sent_analysis.sentiment
      sent_analysis=document.analyze_entities()
      x["content metdata"]["entities"]=sent_analysis.entities

      with open('event.json',"w") as g:
        json.dump(data,g)

      return print("300-NLP successful")

  return print("301-file does not exist")

NLP_analysis("")
