from pymilvus import MilvusClient

# import os
# os.chdir(os.path.dirname(os.path.abspath(__file__)))
from configs import data_path , client 
from create_collection import demo_collection_name 


def load_collection_normal():

    client.load_collection(
        collection_name=demo_collection_name
    )

    res = client.get_load_state(
        collection_name=demo_collection_name
    )

    print(res)

def load_collection_and_fields():
    client.load_collection(
        collection_name=demo_collection_name,
        # highlight-next-line
        load_fields=["id", "vector"], # Load only the specified fields
        skip_load_dynamic_field=True # Skip loading the dynamic field
    )

    res = client.get_load_state(
        collection_name=demo_collection_name
    )

    print(res)

def release_collection():
    client.release_collection(
        collection_name=demo_collection_name
    )

    # res = client.get_load_state(
    #     collection_name=demo_collection_name
    # )

    # print(res)



if __name__ == "__main__":
    release_collection()
    # load_collection_normal()
    load_collection_and_fields()

    release_collection()