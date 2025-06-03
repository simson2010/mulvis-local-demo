import requests

def main():
    # 让用户输入查询内容
    query = input("请输入要查询的内容: ")
    top_k = input("请输入返回结果数量 (默认5): ")
    if not top_k.strip():
        top_k = 5
    else:
        top_k = int(top_k)

    # 构造请求体
    payload = {
        "query": query,
        "top_k": top_k
    }

    # 发送 POST 请求
    try:
        response = requests.post(
            "http://127.0.0.1:8000/search",
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        print("搜索结果：")
        for idx, item in enumerate(data.get("results", []), 1):
            print(f"{idx}. {item['term']} (distance: {item['distance']})")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == "__main__":
    main()
