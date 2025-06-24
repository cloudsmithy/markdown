之前我的infinilabs Console 一直跑在群晖里，由于和 Coco-AI 的默认端口冲突，导致经常忘记端口信息，群晖里运行着 Easysearch，Elasticsearch、OpenSearch 三个大集群，也想慢慢迁移到其他性能高的机器上去，正好最近购买了懒猫微服，能够让我做应用的迁移，顺便还得能上架一些应用。



## Infinilabs.console 是什么？

如果你用过 Elasticsearch，那就一定知道 Kibana。Infinilabs Console，就是极限科技团队开发的国产可视化控制台，是一个面向 Easysearch、Elasticsearch 和 OpenSearch 的运维、监控、数据管理平台，可以看作是国产版的 Kibana 替代品。

最初接触这个款产品的时候让我眼前一亮，它能够借助Easysearch 或者 Elasticsearch 的REST API 来连接集群，同时也高效地管理和监控 Elasticsearch、OpenSearch 以及 INFINI Easysearch 等搜索引擎集群，提供统一的运维、监控、安全和数据管理能力。这一点其实是 Kibana 比不了的，尽管是老牌软件，但是初学 ES 的时候Kibana 连接 ES 要查 log 设置一些 key，这个整个部署过程就花了一个小上午的时间。而且跨版本，跨引擎来支持的能力也是其他可视化工具无法比拟的。简单来说，真的很符合国人的使用习惯。



首先我们可以在连接的时候不同的引擎（Easysearch、Elasticsearch、OpenSearch ），以及你集群的位置（线下还是在各种云上），同时支持 HTTP 和 HTTPS 的连接。

![连接集群](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250509103447515.png)



连接之后，可以看到已经正确识别出来了的Easysearch、Elasticsearch和OpenSearch，并且抓取了相应的数据监控，比如基本的集群状态，节点数量，索引，分片以及文档的数量，还有磁盘和 JVM 的占用。



![集群信息](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250509103439985.png)

执行 DSL 的时候可以开启多个 TAB 页这个是我最喜欢的功能，尤其在做集群迁移的时候再也不用找不同的系统去登录了，这里手动@aws 的 OpenSearch。除此之外，做快照传到 S3 的时候也不用担心 access_key 读不到的问题了。曾经我是托管OpenSearch 的用户，托管节点有诸多问题，无法登录，由于服务本身的问题导致业务滞后（升级卡住，看门狗不定时杀进程），做快照必须借助 Postman来传递 IAM 凭证。但，换了Infinilabs console 和Easysearch 之后，整个世界都清净了。

![DSL 开发工具](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250509103527869.png)



GitHub 项目地址如下：https://github.com/infinilabs/console



## 为什么选择了懒猫商店？

懒猫微服解决了我日常使用 NAS 的几个痛点：

- 装了一堆服务（Redis、MinIO、MeiliSearch、Adminer、Swagger UI……），入口太分散；
- 每次看容器状态都要 `docker ps` 一把梭；
- Homepage 要手动配置，配置文件写起来太繁琐；



部署成功后会给到一个域名，然后通过域名访问可以自动解析内外网的 IP 地址，同时也自带了路由守卫功能来重定向到懒猫的 SSO，

而在传统 NAS 部署 Authentik 然后再去应用端做 SSO 的适配应该是 NAS 玩家的终极梦想，而上架商店之后自动集成了这样的认证系统（也是单点登录）。然后，在外边的时候也可以监控和操作自己的 ES 集群啦～（随地大小班的理由又多了一条）



![保护应用的 SSO](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250509110532533.png)

因为上架的应用是 HTTP 的，懒猫微服还能自动做了一个 TLS 传输，用的他们自己域名，然后通过 https 访问Infinilabs Console。





![自带 TLS](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250509110738032.png)





除此之外还自带了dozzle，可以很方便查看安装应用的上架信息，毕竟对于开发者来说，装机玩 NAS 是兴趣，但是搭建好之后的维护问题也同样劳心费力，真的一点都不想浪费时间和精力，那么杂活就交给平台来管理吧。

![查询应用日志](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250509113301412.png)





进入懒猫微服的【应用商店】，搜索：`infinilabs.console`一键安装并启动，打开浏览器，开始使用Infinilabs Console 吧～


![image.png](https://lzc-playground-1301583638.cos.ap-chengdu.myqcloud.com/guidelines/459/5cde62de-530b-4364-95a6-033fd289cb98.png "image.png")

地址如下：

https://lazycat.cloud/appstore/#/shop/detail/xu.infinilabs.console

## 相关链接

- infinilabs.console 介绍：https://infinilabs.cn/products/console/
- infinilabs Github介绍：https://infinilabs.cn/products/console/
- 懒猫微服上架地址：https://lazycat.cloud/
- 懒猫微服官网：https://lazycat.cloud/



![image.png](https://lzc-playground-1301583638.cos.ap-chengdu.myqcloud.com/guidelines/459/c4ab5141-2854-4536-b95e-35001d6cc3f2.png "image.png")


