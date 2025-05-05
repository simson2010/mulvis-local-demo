from pymilvus import MilvusClient, DataType

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)

res = client.list_collections()

print(res)

for collection_name in res:
    collection_desc = client.describe_collection(
        collection_name=collection_name
    )
    print(collection_desc)
# print(res)

# client.rename_collection(
#     old_name="my_new_collection",
#     new_name="my_collection_1"
# )