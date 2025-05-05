from pymilvus import MilvusClient
from configs import demo_collection_name, client,data_path
from configs import embed_text, load_data

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)

# 4. Single vector search
def search(text):
    query_vector = embed_text(text)
    res = client.search(
        collection_name=demo_collection_name, 
        anns_field="vector",
        data=[query_vector[0]],
        output_fields=["id", "text", "title", "file_name"],
        limit=5
    )
    return res

if __name__ == "__main__":
    search_keyword = "作者"
    res = search(search_keyword)
    hits = res[0]
    all_text = ""
    for hit in hits:
        all_text += hit.entity["text"] + "\n"
        print("++" * 10, "\n")
    print(all_text)

    # for hits in res:
    #     print(len(hits), "\n",hits[2].entity,"\n")
    #     for hit in hits:
    #         print(hit.id, hit.distance, hit.text[0:50], hit.title, hit.file_name, "\n")
