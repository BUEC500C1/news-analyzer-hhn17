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






def Create(filename, file_ID, author):
  with open('event.json') as f:
    data=json.load(f)

  #new_data={"File_name":filename, "FILE_ID":file_ID,"Author":author,"text":"insert here","Upload time":"current time","Modified time":"current time"}
  new_data = data_temp
  new_data["File_name"]=filename
  new_data["FILE_ID"]=file_ID
  new_data["Author"]=author

  for x in data:
    if x["File_name"]==new_data["File_name"] and x["FILE_ID"]==new_data["FILE_ID"] and x["Author"]==new_data["Author"]:
      return print("101-File already exist")



  data.append(new_data)

  with open('event.json',"w") as f:
    data=json.dump(data,f)
  
  return print("100-create successful")

def Delete(filename, file_ID, author):
  with open('event.json') as f:
    data=json.load(f)

  for x in data:
    if x["File_name"]==filename and x["FILE_ID"]==file_ID and x["Author"]==author:
      data.remove(x)
      with open('event.json',"w") as f:
        data=json.dump(data,f)
      return print("120-delete successful")

  return print("121-can't delete due to file not exist or permission not granted")

def Update(filename, file_ID, author):
  with open('event.json') as f:
    data=json.load(f)

  for x in data:
    if x["File_name"]==filename and x["FILE_ID"]==file_ID and x["Author"]==author:
      #x["text"]="updated text"
      x["Modified time"]="new time"
      with open('event.json',"w") as f:
        data=json.dump(data,f)
      return print("110-update successful")

    return print("111-can't update due to file not exist or permission not granted")



Create("A1",123,"SS")
Update("A1",123,"SS")
