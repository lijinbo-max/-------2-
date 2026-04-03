import os
import time
import requests
import json
from datetime import datetime

# API调用统计数据
api_stats = {
    "total_calls": 0,
    "successful_calls": 0,
    "failed_calls": 0,
    "total_response_time": 0,
    "last_call_time": None
}

# API错误处理和重试机制
def call_api_with_retry(url, headers, data, max_retries=3, retry_delay=1):
    """带重试机制的API调用"""
    global api_stats
    start_time = time.time()
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=data, timeout=30)
            response.raise_for_status()  # 检查响应状态码
            
            # 更新统计数据
            api_stats["total_calls"] += 1
            api_stats["successful_calls"] += 1
            api_stats["total_response_time"] += time.time() - start_time
            api_stats["last_call_time"] = datetime.now().isoformat()
            
            return True, response.json()
        except requests.exceptions.RequestException as e:
            api_stats["total_calls"] += 1
            api_stats["failed_calls"] += 1
            api_stats["last_call_time"] = datetime.now().isoformat()
            
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # 指数退避
                continue
            else:
                return False, str(e)

# API密钥安全管理
def get_api_key():
    """安全获取API密钥"""
    try:
        # 优先从环境变量获取
        api_key = os.getenv("GLM4_API_KEY")
        if api_key and api_key != "your-api-key-here":
            return api_key
        
        # 从.env文件获取
        with open('.env', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('GLM4_API_KEY='):
                    api_key = line.split('=', 1)[1]
                    if api_key and api_key != "your-api-key-here":
                        return api_key
    except Exception as e:
        print(f"获取API密钥失败: {str(e)}")
    
    return None

# 保存API统计数据
def save_api_stats():
    """保存API统计数据到文件"""
    try:
        with open('api_stats.json', 'w', encoding='utf-8') as f:
            json.dump(api_stats, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"保存API统计数据失败: {str(e)}")

# 加载API统计数据
def load_api_stats():
    """从文件加载API统计数据"""
    global api_stats
    try:
        with open('api_stats.json', 'r', encoding='utf-8') as f:
            loaded_stats = json.load(f)
            api_stats.update(loaded_stats)
    except Exception as e:
        print(f"加载API统计数据失败: {str(e)}")

# 初始化API管理器
load_api_stats()

# API调用函数
def call_glm4_api(prompt, model="glm-4-flash", temperature=0.7):
    """调用GLM-4-Flash API"""
    api_key = get_api_key()
    if not api_key:
        return False, "API密钥未配置"
    
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": temperature
    }
    
    success, result = call_api_with_retry(url, headers, data)
    save_api_stats()  # 保存统计数据
    
    return success, result

# 获取API统计信息
def get_api_stats():
    """获取API统计信息"""
    return api_stats
