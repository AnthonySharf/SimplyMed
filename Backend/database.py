from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["simplymed"]
collection = db["drug_info"]

def get_drug(drug_name):
    return collection.find_one({"drug_name": drug_name}, {"_id": 0}) # Exclude the _id field from the result because Python can't query it

def save_drug(drug_name, adverse_events, drug_profile):
    collection.insert_one({
        "drug_name": drug_name,
        "adverse_events": adverse_events,
        "drug_profile": drug_profile
    })