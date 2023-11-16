from pymongo import MongoClient
import settings
import pandas as pd

try:
    client = MongoClient(settings.MONGO_STRING)
    db = client[settings.DATABASE]
except Exception as e:
    print("Error in connection")
    raise e


def fetch_one_data_line(collection_name, data_name):
    try:
        collection = db[collection_name]
        data = collection.find_one({"Name": data_name})
        return data
    except Exception as e:
        print('Error in data fetching')


def fetch_all_data_lines(collection_name):
    collection = db[collection_name]
    _data = collection.find({})
    data_list = []
    for document in _data:
        data_list.append(document)
    return pd.DataFrame(data_list)


def send_one_data(collection_name, df_line):
    collection = db[collection_name]
    collection.insert_one(df_line)
    print(f"Insert Data Successfully")


def send_many_data(collection_name, df):
    print(df)
    data_list = df.to_dict(orient="records")
    collection = db[collection_name]
    collection.insert_many(data_list)
    print(f'Insert Multi Data Successfully')


def count_row_in_collection(collection_name):
    collection = db[collection_name]
    return int(collection.estimated_document_count({}))


def query_database(collection_name, start_date, end_date):
    try:
        collection = db[collection_name]
        _data = collection.find({})
        data_list = []
        for document in _data:
            data_list.append(document)
        df = pd.DataFrame(data_list)
        return df.to_csv(f'CSV/{start_date}-{end_date}.csv')
    except Exception as e:
        print("Error querying database:", e)
        return pd.DataFrame().to_csv(f'CSV/{start_date}-{end_date}.csv')


def fetch_all_medicine_name(collection_name):
    names = None
    try:
        collection = db[collection_name]
        result = collection.find({}, {'Name': 1})
        names = [doc["Name"] for doc in result]
    except Exception as e:
        names = []
        print(str(e))
    return names


def update_medicine_quantity(medicine_name, quantity_sold):
    collection = db["availablestock"]
    medicine_details = collection.find_one({"Name": medicine_name})

    if medicine_details:
        new_quantity = medicine_details["Boxes"] - quantity_sold
        collection.update_one({"_id": medicine_details["_id"]}, {"$set": {"Boxes": new_quantity}})
        print("Quantity updated successfully.")
    else:
        print("Medicine not found in availablestock.")
