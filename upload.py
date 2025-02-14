from pymongo import MongoClient
import json
from datetime import datetime

from pymongo.server_api import ServerApi

uri = "mongodb+srv://pg29072003:IELq4hnKx1umfelk@cluster0.jbeey.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Select database and collection
db = client["facebook_ads"]
collection = db["zara_ads"]

# Read JSON data
with open("zara_ads.json", "r") as file:
    ads_data = json.load(file)

# Add timestamp and insert data into MongoDB
for ad in ads_data:
    ad["timestamp"] = datetime.utcnow()

result = collection.insert_many(ads_data)
print(f"{len(result.inserted_ids)} ads inserted into MongoDB!")

# Verify insertion
print(f"Total ads in database: {collection.count_documents({})}")
print("Sample ad:", collection.find_one())

# Close MongoDB connection
client.close()
