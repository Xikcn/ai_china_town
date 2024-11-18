import requests

# 定义模板字符串
template = "在{location}这个地方的很久以前, 有一位{character} 去 {action}，请你续写完这个故事"

# 替换模板中的占位符
location = "F小镇"
character = "勇士"
action = "对抗邪恶的巨龙"

# 构建最终的提示
prompt = template.format(location=location, character=character, action=action)

# API 服务的 URL
api_url = "http://127.0.0.1:11434/api/generate"

# 请求体
data = {
    "model": "qwen2.5",
    "prompt": prompt,
    "stream": False
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


