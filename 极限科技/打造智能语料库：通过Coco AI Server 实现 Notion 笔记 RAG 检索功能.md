---
tags:
  - 极限科技
category: 极限
title: sss
tasks: sss
---


本文将详细介绍如何将 Notion 作为语料库，部署 CoCo Server 的 RAG（Retrieval-Augmented Generation）功能。我们将使用 Easysearch 作为语料库存储 Notion 素材，并通过 ollama 进行 LLM 推理。

### 1. 环境准备

#### 1.1 启动 Easysearch
首先，启动 Easysearch 作为语料库，用于存储 Notion 的素材。

#### 1.2 启动 ollama
接下来，启动 ollama，用于进行 LLM 推理。

#### 1.3 启动 CoCo Server
启动 CoCo Server，默认端口为 9000。

![CoCo Server 启动界面](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217142649790.png)

### 2. CoCo App 连接与登录

#### 2.1 连接 CoCo Server
通过 CoCo App 连接 Server，并输入相关信息。

![CoCo App 连接界面](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217142816787.png)

#### 2.2 使用 GitHub 登录
登录时选择使用 GitHub 账号进行认证。

![GitHub 登录界面](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217142837884.png)

#### 2.3 获取 OAuth 回调信息
登录成功后，系统会重定向并返回 OAuth 回调信息。我们需要抓取以下信息，后续将使用该 token 换取访问 CoCo Server AI 的 key：

```
coco://oauth_callback?code=cupibub55o1cfqbveps0q804ai6aj14in3u91xjhvuk8s7ixirjsq2j9mmyyeut91nmgjwz0b494ngpk&request_id=eb94762b-f054-4710-9c6cf20889d3&provider=coco-cloud
```

![OAuth 回调信息](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217142925920.png)

### 3. 认证流程

#### 3.1 获取临时 Token
首先，访问以下 URL 获取临时 Token：

```
http://localhost:9000/sso/login/github?provider=coco-cloud&product=coco&request_id=dd9825e1-ebd3-4c84-9e3f-7ccb0421c508
```

该请求将返回一个临时 Token，例如 `XXABC`。

#### 3.2 换取 Access Token
使用上一步获取的临时 Token，通过以下命令换取 Access Token：

```bash
curl -H'X-API-TOKEN: XXABC' "http://localhost:9000/auth/request_access_token?request_id=dd9825e1-ebd3-4c84-9e3f-7ccb0421c508"
```

返回的 Token 即为所需的 Access Token。

#### 3.3 使用 Postman 获取 Token
在 Postman 中执行上述步骤，获取 `access_token` 和过期时间。

![Postman 获取 Token](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217143134946.png)

### 4. 使用 Python 脚本自动化认证流程

以下 Python 脚本可用于自动化解析 OAuth 回调信息并获取 Access Token：

```python
import requests

def parse_oauth_callback(url):
    query_params = {param.split('=')[0]: param.split('=')[1] for param in url.split('?')[1].split('&')}
    code = query_params.get("code")
    request_id = query_params.get("request_id")
    return code, request_id

def request_access_token(code, base_url, request_id):
    url = f"{base_url}/auth/request_access_token?request_id={request_id}"
    headers = {"X-API-TOKEN": code}
    response = requests.get(url, headers=headers)
    return response.json()

# 示例输入
oauth_callback_url = """
coco://oauth_callback?code=cupibub55o1cfqbveps0q804ai6aj151wu4in3u91xjhvuk8s7ixirjsq2j9mmyyeut91nmgjwz0b494ngpk&request_id=eb94762b-f054-4710-9c6a-0cf2088729d3&provider=coco-cloud
"""
base_url = "http://localhost:9000"

# 解析 code 和 request_id
code, request_id = parse_oauth_callback(oauth_callback_url)

# 发送请求
token_response = request_access_token(code, base_url, request_id)
print(token_response)
```

### 5. 查看用户信息

使用获取的 `access_key` 可以查看用户信息：

```python
import requests

url = "http://localhost:9000/account/profile"

payload = {}
headers = {
  'X-API-TOKEN': 'cupichb55o1cfqbveq90zwomyxs791ul3esbxxt480c8dzgvdtjtvmcnsld4a5v0wvx9l9ofcf1'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
```

### 6. 注册 Notion Connector

以下 Python 脚本用于注册 Notion Connector：

```python
import requests
import json

def update_connector(base_url, api_token, connector_name, data):
    url = f"{base_url}/connector/{connector_name}?replace=true"
    headers = {
        "X-API-TOKEN": api_token,
        "Content-Type": "application/json"
    }
    response = requests.put(url, headers=headers, data=json.dumps(data))
    return response.json()

base_url = "http://localhost:9000"
api_token = "<token>"

notion_data = {
    "name": "Notion Docs Connector",
    "description": "Fetch the docs metadata for notion.",
    "icon": "/assets/connector/notion/icon.png",
    "category": "website",
    "tags": ["docs", "notion", "web"],
    "url": "http://coco.rs/connectors/notion",
    "assets": {
        "icons": {
            "default": "/assets/connector/notion/icon.png",
            "web_page": "/assets/connector/notion/icon.png",
            "database": "/assets/connector/notion/database.png",
            "page": "/assets/connector/notion/page.png"
        }
    }
}

response_notion = update_connector(base_url, api_token, "notion", notion_data)
print(response_notion)
```
在Easysearch中看到创建Notion的Connector：

![image.png](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/20250217213310.png)

### 7. 配置 Notion Connector

#### 7.1 修改 Notion 配置文件
修改 Notion 配置文件以激活检索功能：

![Notion 配置文件修改](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217210840104.png)

#### 7.2 申请 Notion API Key
在 Notion 官网申请 API Key：[Notion API Key](https://www.notion.so/profile/integrations)

![Notion API Key 申请](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217212252851.png)

#### 7.3 配置权限与展示 API Key
配置完成后，设置权限并展示 API Key：

![Notion API Key 展示](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217212349650.png)

#### 7.4 配置 Notion Connector
使用以下 Python 脚本配置 Notion Connector：

```python
import requests
import json

def create_datasource(base_url, api_token, data):
    url = f"{base_url}/datasource/"
    headers = {
        "X-API-TOKEN": api_token,
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

# 示例输入
base_url = "http://localhost:9000"
api_token = "<api-key>"

datasource_data = {
    "name": "My Notion",
    "type": "connector",
    "connector": {
        "id": "notion",
        "config": {
            "token": "<notion token>"
        }
    }
}

# 发送 POST 请求
response = create_datasource(base_url, api_token, datasource_data)
print(response)
```

#### 7.5 设置 Notion 集成
在 Notion 中设置集成，以便 CoCo Server 能够搜索到相关内容：

![Notion 集成设置](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217212508943.png)


### 8. 验证检索功能

![image.png](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/20250217213558.png)

![image.png](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/20250217213454.png)

![](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/20250217213454.png)

#### 8.1 查看 CoCo Server 日志
在 CoCo Server 日志中确认 Notion 检索功能已启用：

![CoCo Server 日志](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217210810825.png)

#### 8.2 在搜索栏检索
最后，您可以在搜索栏中检索到 Notion 笔记内容：

![Notion 检索结果](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250217211620791.png)

至此，您已成功将 Notion 作为语料库部署到 CoCo Server 的 RAG 功能中。