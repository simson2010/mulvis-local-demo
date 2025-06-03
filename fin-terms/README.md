# 金融术语搜索系统

## 项目概述
本项目是一个基于 Milvus 向量数据库的金融术语搜索系统，能够通过语义相似度快速查找相关金融术语。

## 主要功能
- 金融术语的向量化存储
- 基于语义相似度的术语搜索
- 可配置的返回结果数量
- RESTful API 接口

## 技术栈
- Python 3
- FastAPI
- Milvus Lite
- Sentence Transformers
- Pandas

## 项目结构
```plaintext
fin_terms/
├── main.py # FastAPI 主程序，API 路由定义
├── db/
│ └── fin_data.db # Milvus Lite 数据库文件
├── src/
│ └── search_terms.py # Milvus 搜索与向量化逻辑封装
└── client.py # 命令行客户端，调用 API 进行查询、
```

## 环境依赖

- Python 3.11+
- FastAPI
- Uvicorn
- pymilvus
- sentence-transformers
- requests

安装依赖（建议使用虚拟环境）：

```bash
pip install fastapi uvicorn pymilvus sentence-transformers requests
```

## 数据准备

请确保 `db/find_data.db` 已存在且包含名为 `financial_terms` 的 Collection。  
如未准备好数据，请先运行数据加载脚本（此部分请根据你的实际数据加载流程补充）。

在根目录运行：
```bash
python fin-terms/src/load_data_to_db.py
```

## 启动服务

在根目录下运行：

```bash
uvicorn fin-temrs.main:app --reload
```

服务启动后，访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) 可查看自动生成的 Swagger API 文档并在线测试。

## API 使用说明

### 1. 搜索接口

- **路径**：`POST /search`
- **请求体**：

  ```json
  {
    "query": "ABCD",
    "top_k": 5
  }
  ```

- **返回示例**：

  ```json
  {
    "query": "ABCD",
    "results": [
      {"term": "实际匹配到的术语1", "distance": 0.123},
      {"term": "实际匹配到的术语2", "distance": 0.234}
    ]
  }
  ```

### 2. 健康检查

- **路径**：`GET /`
- **返回**：

  ```json
  {"message": "金融术语搜索 API 运行中"}
  ```

## 命令行客户端

你可以使用 `client.py` 作为命令行客户端，交互式输入查询内容并获取结果：

```bash
python fin-terms/client.py
```

## 运行效果：

```plaintext
请输入要查询的内容: stock
请输入返回结果数量 (默认5): 5
搜索结果：
1. Stock (distance: 1.0)
2. Full Stock (distance: 0.8341772556304932)
3. Cheap Stock (distance: 0.8158348202705383)
4. Stock-For-Stock (distance: 0.787199079990387)
5. Half Stock (distance: 0.786156177520752)
```

## 目录与模块说明

- `main.py`：API 路由与请求处理，调用 `src/search_terms.py` 封装的 Milvus 搜索逻辑。
- `src/search_terms.py`：负责 Milvus Lite 的连接、向量化和搜索功能的封装。
- `client.py`：命令行客户端，便于本地测试 API。
- `db/fin_data.db`：Milvus Lite 数据库文件，需提前准备好。

## 常见问题

- **ModuleNotFoundError**：请确保目录名、文件名不含 `-`，并使用下划线 `_`。
- **Milvus Collection 不存在**：请先运行数据加载脚本，确保数据库和 Collection 已创建。

## 贡献与许可

如需贡献代码或反馈问题，请提交 Issue 或 Pull Request。  
本项目遵循 MIT 许可证。



