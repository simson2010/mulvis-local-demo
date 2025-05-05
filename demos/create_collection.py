from pymilvus import MilvusClient, DataType
from configs import demo_collection_name

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)

def createCollection():
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
    schema.add_field(field_name="text", datatype=DataType.VARCHAR, max_length=8192)
    schema.add_field(field_name="title", datatype=DataType.VARCHAR, max_length=512)
    schema.add_field(field_name="file_name", datatype=DataType.VARCHAR, max_length=512)

    index_params = client.prepare_index_params()

    index_params.add_index(
        field_name="id",
        index_type="AUTOINDEX"
    )

    index_params.add_index(
        field_name="vector", 
        index_type="AUTOINDEX",
        metric_type="COSINE"
    )


    client.create_collection(
        collection_name=demo_collection_name,
        schema=schema,
        index_params=index_params
    )

    res = client.get_load_state(
        collection_name=demo_collection_name
    )

    print(f"Collection {demo_collection_name} , state : {res}")

def deleteCollection():
    client.drop_collection(
        collection_name=demo_collection_name
    )

if __name__ == "__main__":
    deleteCollection()
    createCollection()

