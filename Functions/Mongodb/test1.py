sql = [
    {'$match': {
        'trans_details.asset.data.id': transaction_id}},
    {'$unwind': '$trans_details'},
    {'$match': {
        'trans_details.asset.data.id': transaction_id}},
    {'$sort': {'height': -1}},
    {'$limit': 1}
]