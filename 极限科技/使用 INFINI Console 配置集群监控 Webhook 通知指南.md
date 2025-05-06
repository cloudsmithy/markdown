---
title: 实现 INFINI Console 与 GitHub 的单点登录集成：一站式身份验证解决方案
date: 2025-03-25 20:40:00
tags: [GitHub, OAuth, SSO, INFINI]
categories: 极限科技
---

在集群管理中，监控关键指标如 CPU、内存、磁盘、JVM 等是至关重要的。对于 Easysearch 及 ES 生态系统，还需要关注集群本身的指标，例如搜索延迟、集群状态、节点移除等。INFINI Console 不仅提供了默认的监控指标，还支持用户自定义监控项。当监控数值达到预设阈值时，系统可以通过 Webhook 发送通知至 Slack、飞书等平台。

## 监控配置流程

### 1. 告警对象与通知渠道设置

在 INFINI Console 中，首先需要配置监控对象和通知渠道：

![告警对象与通知渠道设置](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232436697.png)

### 2. 告警中心管理

通过告警中心可以集中管理所有监控告警：

![告警中心](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232210867.png)

### 3. 告警详情查看

每个告警事件都提供详细信息查看功能：

![告警详情](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232101332.png)

### 4. 告警历史记录

系统完整记录所有历史告警信息：

![告警历史](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232049862.png)

## Webhook 实现示例

以下是用 Python 实现的 Webhook 接收服务：

```python
from flask import Flask, request, jsonify
import json
from pprint import pprint

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # 获取并处理请求数据
    raw_data = request.data
    decoded_data = raw_data.decode('utf-8')
    data = json.loads(decoded_data)

    # 打印接收到的数据
    print("Received data:")
    pprint(data)

    # 返回响应
    return jsonify({
        "status": "success",
        "message": "Webhook received"
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

## Webhook 配置步骤

1. 在 Console 中添加 Webhook 配置：

![Webhook配置](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232130342.png)

1. 查看捕获的告警信息：

![告警捕获](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221231859416.png)

## 飞书 Webhook 集成

### 1. 创建飞书群组

在飞书客户端创建新的群组：

![创建群组](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232028845.png)

### 2. 添加自定义机器人

选择添加自定义机器人：

![添加机器人](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221232003541.png)

### 3. 配置机器人信息

设置机器人名称和描述：

![机器人配置](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221231949682.png)

### 4. 获取 Webhook URL

完成配置后获取 Webhook 地址：

![Webhook URL](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250221231933502.png)

通过以上配置，即可实现集群监控告警的实时通知，确保系统运维人员能够及时响应各种异常情况。
