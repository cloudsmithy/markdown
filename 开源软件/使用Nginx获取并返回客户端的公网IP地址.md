

在某些场景下，我们需要快速获取客户端的公网IP地址。虽然有许多在线服务（如IP Address Lookup、IPv4/IPv6检测工具或https://checkip.amazonaws.com/）可以提供此功能，但通过自建Nginx服务来实现这一需求，不仅灵活可控，还能更好地满足个性化需求。

下面是一个简单的Nginx配置示例，用于返回客户端的公网IP地址。

## 配置Nginx返回客户端IP地址

如果你希望Nginx直接返回客户端的IP地址，可以通过在`location`块中使用`$remote_addr`变量来实现。以下是一个完整的配置示例：

```nginx
server {
    listen 80;

    location /get_ip {
        default_type 'application/json';
        return 200 '{"ip_addr": "$remote_addr"}';
    }
}
```

### 配置说明：
1. **`listen 80;`**  
   监听80端口，处理HTTP请求。

2. **`location /get_ip { ... }`**  
   定义一个路径为`/get_ip`的请求处理块。当客户端访问`/get_ip`时，Nginx会执行该块中的指令。

3. **`default_type 'application/json';`**  
   设置响应的默认MIME类型为`application/json`，确保客户端能够正确解析返回的JSON数据。

4. **`return 200 '{"ip_addr": "$remote_addr"}';`**  
   返回一个HTTP状态码为200的响应，内容为一个JSON对象，其中`ip_addr`字段的值为客户端的IP地址（通过`$remote_addr`变量获取）。

### 示例响应
当客户端访问`/get_ip`路径时，Nginx会返回如下格式的JSON响应：

```json
{"ip_addr": "客户端IP地址"}
```

例如，如果客户端的IP地址是`203.0.113.1`，则响应为：

```json
{"ip_addr": "203.0.113.1"}
```

---

## 总结
通过以上配置，你可以快速搭建一个简单的Nginx服务，用于返回客户端的公网IP地址。这种方式不仅高效，还能根据需求进一步扩展功能，例如记录IP地址、限制访问频率等。如果你需要更复杂的功能，可以结合Nginx的其他模块和变量来实现。