import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 获取API密钥
api_key = os.getenv("GLM4_API_KEY")
if not api_key:
    print("请在.env文件中配置GLM-4-Flash API密钥")
    exit(1)

# 构建测试提示
prompt = "你好，请问你是谁？"

# 调用GLM-4-Flash API
url = "https://open.bigmodel.cn/api/mt/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
data = {
    "model": "glm-4-flash",
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ],
    "temperature": 0.7
}

print("正在测试GLM-4-Flash API...")
try:
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response_data}")
    
    if "choices" in response_data and len(response_data["choices"]) > 0:
        print("\nAI回复:")
        print(response_data["choices"][0]["message"]["content"])
    else:
        print("\nAPI调用失败")
except Exception as e:
    print(f"发生错误: {str(e)}")
