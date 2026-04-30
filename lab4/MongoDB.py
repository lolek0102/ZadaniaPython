from pymongo import MongoClient
import requests

print("Start programu")

client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=3000)

print("Sprawdzam MongoDB...")
client.server_info()
print("MongoDB działa")

db = client.lab4
networks = db["networks"]

networks.delete_many({})

print("Pobieram dane z API...")
response = requests.get("https://api.geckoterminal.com/api/v2/networks")
data = response.json()["data"]

print("Wstawiam dane...")
networks.insert_many(data)

pipeline = [
    {"$group": {"_id": "$type", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}
]
pipeline2 = [
    {"$group": {"_id": "$attributes.name", "count": {"$sum": 1}}},
    {"$sort": {"_id": 1}}
]

print("Liczba sieci per typ:")
for doc in networks.aggregate(pipeline):
    print(doc)

print("\nSieci:")
for doc in networks.aggregate(pipeline2):
    print(doc)

client.close()
print("Koniec")