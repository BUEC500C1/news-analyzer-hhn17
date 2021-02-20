import json

data_temp={
  "File_name":"",
  "FILE_ID":"",
  "Author":"",
  "Upload time":"",
  "Modified time":"",
  "Notes":"",
  "Permission":"",
  "content metadata":[{
  "tags":"",
  "source":"",
  "sentiment":"",
  "sentiment score":"",
  "entity":"",
  "text":""
  }]
}


def new_ingester(url):
  if url == "":
    return print("201-link not found")

  #will implement html to text using beautifulSoup

new_ingester("")