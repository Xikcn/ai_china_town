import requests

# VLLM 服务的 URL
url = "http://localhost:8000/v1/chat/completions"

# 请求参数
payload = {
    "model": "/home/xik/models/qwen/qwen2-0___5b",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "天空为什么是蓝色的？"}
    ],
    "temperature": 0.7,
    "top_p": 0.8,
    "repetition_penalty": 1.05,
    "max_tokens": 512
}

# 设置请求头
headers = {
    "Content-Type": "application/json"
}

# 发送 POST 请求
response = requests.post(url, json=payload, headers=headers)

# 检查响应状态码
if response.status_code == 200:
    # 解析响应内容
    result = response.json()
    print("Generated Text:", result.get("choices", [{}])[0].get("message", {}).get("content"))
else:
    print("Request failed with status code:", response.status_code)
    print("Response content:", response.content)