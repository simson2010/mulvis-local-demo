from pymilvus import MilvusClient, DataType

demo_collection_name = 'my_collection_2'

data_path = "/home/ericpan/mulvis_local/data/黑悟空wiki.txt"

def load_data():
    global data_path
    # 加载文本文件内容
    with open(data_path, 'r', encoding='utf-8') as file:
        all_text = file.read()
    return all_text


all_text = load_data()

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)


from FlagEmbedding import BGEM3FlagModel

model = BGEM3FlagModel('BAAI/bge-m3',  
                        use_fp16=False) # Setting use_fp16 to True speeds up computation with a slight performance degradation

def embed_text(input_text):
    sentences_1 = [input_text]
   
    # embeddings_1 = model.encode(sentences_1, 
    #                             batch_size=12, 
    #                             max_length=8192, # If you don't need such a long length, you can set a smaller value to speed up the encoding process.
    #                             )['dense_vecs']
    embeddings_1 = model.encode(sentences_1)['dense_vecs']
    # embeddings_2 = model.encode(sentences_2)['dense_vecs']
    # similarity = embeddings_1 @ embeddings_2.T
    print(embeddings_1)
    return embeddings_1
    # [[0.6265, 0.3477], [0.3499, 0.678 ]]



if __name__ == "__main__":
    all_text = "hello world"
    res = embed_text(all_text)
    print(res)
