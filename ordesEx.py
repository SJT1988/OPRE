from pymongo import MongoClient 
import json

def main():
    client = MongoClient()

    db = client.get_database("220711_w3")

    collection = db.Orders

    '''
    with open("orders.json", 'r') as f:
        file_data = json.load(f)

    collection.insert_many(file_data)
    '''
    # finding the sum of the amount field, calling that field 'total amount', grouping by 'customerName'
    # SELECT customerName, SUM(amount) AS total_amount From Orders GROUP BY customerName;
    sumAllOrders = collection.aggregate([{'$group': {'_id': '$customerName', 'total_amount':{'$sum': '$amount'}}}])
    countAllOrders = collection.aggregate([{'$group': {'_id': '$customerName', 'total_orders':{'$sum': 1}}}])

    for elem in sumAllOrders:
        print(elem)
    print('\n\n')
    for elem in countAllOrders:
        print(elem)
if __name__ == '__main__':
    main()