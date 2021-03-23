import os
db_name = os.environ.get("DB_NAME","clientDB")
monog_address = os.environ.get("MONGO_ADDRESS","mongodb://localhost:27017/")
sentiment_api = os.environ.get("SENTIMENT_API","http://localhost:8118/api/v1/getSentiment")