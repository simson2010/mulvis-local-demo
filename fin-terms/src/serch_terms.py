from pymilvus import MilvusClient
from sentence_transformers import SentenceTransformer

class MilvusSearcher:
    def __init__(self, db_path, collection_name, embedding_model_name):
        self.db_path = db_path
        self.collection_name = collection_name
        self.embedding_model_name = embedding_model_name
        self.client = None
        self.embedding_model = None
        self._init_resources()

    def _init_resources(self):
        print(f"尝试连接到 Milvus Lite 数据库: {self.db_path}")
        self.client = MilvusClient(self.db_path)
        if not self.client.has_collection(self.collection_name):
            raise RuntimeError(f"Collection '{self.collection_name}' 不存在。请先运行数据加载脚本。")
        print(f"Collection '{self.collection_name}' 获取成功。")
        print("成功连接到 Milvus Lite。")
        print(f"加载 Embedding 模型: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        print("Embedding 模型加载成功。")

    def search(self, query, top_k=5):
        query_vector = self.embedding_model.encode(query).tolist()
        search_params = {
            "metric_type": "COSINE",
            "params": {"nprobe": 10}
        }
        results = self.client.search(
            collection_name=self.collection_name,
            data=[query_vector],
            limit=top_k,
            output_fields=["term"]
        )
        formatted_results = []
        for hit in results[0]:
            formatted_results.append({
                "term": hit.entity.get("term"),
                "distance": hit.distance
            })
        return formatted_results