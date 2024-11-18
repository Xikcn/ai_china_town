import requests

# 定义模板字符串
template = "Once upon a time in a {location}, there was a {character} who {action}."

# 替换模板中的占位符
location = "far, far away land"
character = "brave knight"
action = "fought against the evil dragon"

# 构建最终的提示
prompt = template.format(location=location, character=character, action=action)

# API 服务的 URL
api_url = "http://127.0.0.1:11434/api/embed"

# 请求体
data = {
    "model": "qwen2.5:32b",
    "input": "你好"
}

# 发送 POST 请求
response = requests.post(api_url, json=data)

# 检查响应状态码
if response.status_code == 200:
    # 获取生成的文本
    generated_text = response.text
    print(generated_text)

else:
    print(f"Error: {response.status_code}")
    print(response.text)


