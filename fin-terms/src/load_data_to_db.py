import pandas as pd
from pymilvus import Collection, CollectionSchema, FieldSchema, DataType, connections, MilvusClient
import os
# 导入一个用于生成 embeddings 的库，这里以 sentence-transformers 为例
from sentence_transformers import SentenceTransformer

# 定义文件路径
csv_file_path = 'fin-terms/data/fin-terms.csv'
# 定义 Milvus Lite 数据库文件的存储路径
# Milvus Lite 会在这个目录下创建和管理数据文件
milvus_data_path = 'fin-terms/db/fin_data.db'

# 确保数据目录存在
os.makedirs(os.path.dirname(milvus_data_path), exist_ok=True)

# 1. 加载 CSV 文件
try:
    df = pd.read_csv(csv_file_path)
    print(f"成功加载文件: {csv_file_path}")
    print(f"文件包含 {len(df)} 条记录")
    # 假设 CSV 文件有一列包含术语，列名为 'term'
    # 请根据您的实际 CSV 文件列名进行调整
    terms = df['term'].tolist()
except FileNotFoundError:
    print(f"错误: 文件未找到 {csv_file_path}")
    exit()
except KeyError:
    print("错误: CSV 文件中未找到 'term' 列。请检查您的 CSV 文件并修改代码中的列名。")
    exit()


# 2. 初始化 Milvus Lite 连接
# 使用 uri 参数指定数据路径，这适用于 Milvus Lite
# 如果您使用的是 Milvus Standalone/Cluster，连接方式会有所不同 (host, port)
try:
    client = MilvusClient(milvus_data_path)

except Exception as e:
    print(f"连接 Milvus 失败: {e}")
    exit()

# 3. 定义 Milvus Collection Schema
collection_name = "financial_terms"
vector_dim = 384 # 根据您选择的 embedding 模型调整维度

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="term", dtype=DataType.VARCHAR, max_length=512),
    FieldSchema(name="term_vector", dtype=DataType.FLOAT_VECTOR, dim=vector_dim)
]
schema = CollectionSchema(fields, description="金融术语及其向量")

# 检查 Collection 是否已存在，如果不存在则创建
if not client.has_collection(collection_name):
    client.create_collection(
        collection_name=collection_name,
        schema=schema
    )
    print(f"Collection '{collection_name}' 创建成功。")
else:
    print(f"Collection '{collection_name}' 已存在，跳过创建。")

index_params = client.prepare_index_params()
index_params.add_index(
    field_name="term_vector",  # 指定要为哪个字段创建索引，这里是向量字段
    index_type="AUTOINDEX",  # 使用自动索引类型，Milvus会根据数据特性选择最佳索引
    metric_type="COSINE",  # 使用余弦相似度作为向量相似度度量方式
    params={"nlist": 1024}  # 索引参数：nlist表示聚类中心的数量，值越大检索精度越高但速度越慢
)

client.create_index(
    collection_name=collection_name,
    index_params=index_params
)

# 4. 加载 Embedding 模型
# 选择一个合适的预训练模型
try:
    model = SentenceTransformer('all-MiniLM-L6-v2') # 这是一个常用的、维度为 384 的模型
    print("Embedding 模型加载成功。")
except Exception as e:
    print(f"加载 Embedding 模型失败: {e}")
    print("请检查您的网络连接或尝试其他模型。")
    exit()

# 5. 生成 Embeddings 并准备数据
print("生成术语向量...")
# 分批处理以节省内存
batch_size = 100
entities = []
for i in range(0, len(terms), batch_size):
    batch_terms = terms[i:i+batch_size]
    batch_vectors = model.encode(batch_terms).tolist() # 生成向量并转换为列表
    for j in range(len(batch_terms)):
        entities.append({
            "term": batch_terms[j],
            "term_vector": batch_vectors[j]
        })
    print(f"已处理 {min(i + batch_size, len(terms))} / {len(terms)} 条记录")

# 6. 插入数据到 Collection
if entities:
    print(f"准备插入 {len(entities)} 条记录到 Collection '{collection_name}'...")
    try:
        # Milvus Lite 插入数据
        insert_result = client.insert(
            collection_name=collection_name,
            data=entities
        )
        print(f"数据插入成功。插入 ID 范围: {insert_result.primary_keys}")

        # 加载 Collection 到内存以便搜索
        print("加载 Collection 到内存...")
        client.load()
        print("Collection 加载成功，可以进行搜索了。")

    except Exception as e:
        print(f"插入数据或创建索引失败: {e}")
else:
    print("没有数据需要插入。")

# 7. 关闭连接 (可选，程序结束时会自动关闭)
# connections.disconnect("default")
# print("Milvus 连接已关闭。")

print("\n数据加载和索引过程完成。")
print(f"Milvus 数据库文件存储在: {milvus_data_path}")
