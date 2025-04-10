import pandas as pd
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "motogp_db"
COLLECTION_NAME = "riders_data"
FILE_PATH = "C:/Users/hmark/Desktop/Big Data Project/RidersSummary.csv"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

df = pd.read_csv(FILE_PATH)

data = df.to_dict(orient="records")

collection.insert_many(data)

print("Data import completed successfully!")
