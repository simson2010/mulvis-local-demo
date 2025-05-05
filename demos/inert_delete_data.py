from configs import demo_collection_name, client,data_path
from configs import embed_text, load_data


def split_data():
    all_text = load_data()
    all_text = all_text.split("\n\n")
    return all_text

id = 1
def inert_data():
    global id
    all_text = split_data()
    for text in all_text:
        res = embed_text(text)
        client.insert(
            collection_name=demo_collection_name,
            data=[
                {
                    "id": id,
                    "vector": res[0],
                    "text": text,
                    "title": "黑神话：悟空",
                    "file_name": data_path
                }
            ]
        )       
        id += 1

def delete_data():
    client.delete(
        collection_name=demo_collection_name,
        expr="id = 1"
    )

if __name__ == "__main__":
    inert_data()


