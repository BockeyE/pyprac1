sql = [
    {'$match': {
        'trans_details.asset.data.id': ""}},
    {'$unwind': '$trans_details'},
    {'$match': {
        'trans_details.asset.data.id': ""}},
    {'$sort': {'height': -1}},
    {'$limit': 1}
]

# --file--,指的是这个py本身的路径
print(__file__)