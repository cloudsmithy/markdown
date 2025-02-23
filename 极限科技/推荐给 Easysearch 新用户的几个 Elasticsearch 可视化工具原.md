

Easysearch 作为国产化的 Elasticsearch（ES）替代方案，兼容 Elasticsearch 生态系统中的多种工具。本文将介绍几款适合 Easysearch 用户的可视化工具，帮助您更高效地管理和查询数据。

### 1. Elasticsearch Head 插件

在ES培训经常提到的Elasticsearch Head 是一款基于浏览器的插件，适合不想部署 Kibana 等复杂工具的用户。它提供了简洁的界面，方便用户查看集群状态、索引分布、分片信息等。

#### 主要功能：
- **索引分布查看**  
  ![image-20250220212800529](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220212800529.png)

- **索引详细信息**  
  ![image-20250220214716206](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214716206.png)

- **分片信息查看**  
  ![image-20250220214729464](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214729464.png)

- **DSL 查询**  
  ![](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214752552.png)

### 2. Elasticvue 插件

Elasticvue 是一款高评分、高颜值的 Chrome 插件，功能全面，适合需要更丰富功能的用户。

#### 主要功能：
- **节点信息查看**  
  ![](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214619935.png)

- **索引查看**  
  ![image-20250220214619935](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214619935.png)

- **DSL 查询**  
  ![image-20250220214557277](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214557277.png)

- **快照存储库管理**  
  ![image-20250220214520263](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214520263.png)

### 3. Cerebro

Cerebro 是一款需要自行部署的工具，建议使用 Docker 进行安装。为了避免端口冲突和 TLS 认证错误，可以通过 Gateway 进行转发。

#### 部署步骤：
```bash
docker run -p 9100:9000 lmenezes/cerebro
```

#### 主要功能：
- **集群管理**  
  ![image-20250220214359979](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220214359979.png)

- **网络请求处理**  
  Cerebro 有自己的后端服务，请求并非直接从浏览器发出。因此，启动 Docker 容器时，避免连接 `localhost`，以免进入容器内部。  
  ![image-20250220213719116](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220213719116.png)
  
查看索引信息：


![](https://fastly.jsdelivr.net/gh/bucketio/img2@main/2025/02/20/1740059765108-238d61b9-8cb7-419e-be71-65729cfa146d.png)


可视化功能一览：

![image-20250220215239365](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250220215239365.png)

### 4. 认证与安全

对于需要密码认证的连接，可以使用以下两种方式：
1. **直接连接**：  
   `https://admin:xxxxx@localhost:9200/`

2. **Base64 编码凭证**：  
   可以使用 Postman 或其他工具生成 Base64 编码的凭证，并在请求头中传递。

```python
import requests

url = "https://localhost:9200"
payload = ""
headers = {
  'Authorization': 'Basic YWRtaW46NzllYTM4MzMwMmM2OGZiYWM0MDc='
}

response = requests.request("GET", url, headers=headers, data=payload)
print(response.text)
```

### 总结

以上工具各有特色，用户可以根据自己的需求选择合适的工具。无论是简单的浏览器插件，还是功能更强大的 Cerebro，都能帮助您更好地管理和查询 Easysearch 集群。