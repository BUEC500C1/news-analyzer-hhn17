# news-analyzer-hhn17
news-analyzer-hhn17 created by GitHub Classroom

Project 2 Final phase:

Final product:
The aplication is currently hosted on a AWS virtual machine, accessible through the link: http://3.135.222.23/.
To access, create your own author name. Please write down you author ID as this is unchangeable and your only way to login.
Or use the provided account:

Name: Test

ID: e0b6ca1c-d98f-4b97-9a4f-5ac42bccbbb3

If there is any problem, please contact the git owner.

The application consists of 5 modules in total: a file uploader, a text ingester, a NLP analysis, a frontend client and a query module. The database used is mongodb. 

-File uploader:
The file uploader receive a pdf or txt file, extract the text and upload them to the database. 


-Text ingester:
Accept pdf file and convert them to text using pdfminer. Similar to file uploader but do not allow update or delete operation. 
Pass the text through google NLP for sentiment score

-Google NLP:
Pass the text through Google cloud NLP to extract the sentiment analysis and score. Currently, there is no support for user interface to access this data

-Query:
Allow user to enter a string then search the database for that string. Return all file containing the string but user can only access file uploaded by them

-Frontend module:
The user interface. The user can register by entering a unique username. A random author ID will be generated for this author name and the author will have to remember it to login. Currently support the upload, update and search operation. 


Issues:
Currently, some features such as sentiment analysis and deletion are not supported on the UI and can only be access through command line. Github workflow test is also not supported. 



