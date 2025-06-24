
刚拿到懒猫微服的时候，了解到这个机器完全使用DNS 来访问是很吃惊的。拒不完全使用经验，大概是机器里部署了一套私有的 DNS server，然后广播到整个局域网。而公网上的则是heiyu.space，通过 whois 查看，公网的 domain 是在腾讯云购买的。

![image-20250513092022572](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250513092022572.png)



所以应该是两套的解析结构，局域网访问的时候，就先用机器部署的私有 domain 进行解析，如果使用流量或者在外边，就是走互联网上DNSPod的解析记录。这个结论属于猜测，因为很多公有云也确实四这么做的，一个公开托管的 domain 用来互联网解析，一个 VPC 内的 private domain 用来解析 VPC 内部的地址。

懒猫微服和传统的NAS又很大的不同，如果作为小白玩家可以很快上手，当做 Sass 服务来用。但对于专业玩家，总有一种技术的强迫症，总用抽丝剥茧，从 Saas 一点点解析到 Iass，然后一点把懒猫编程能够公开访问的私有云。

比如网络。可以通过 dig 或者 nslookup 来解析

```
dig xxx.heiyu.space +short
dig xxx.heiyu.space AAAA +short
```

但是，DNS 解析这里慢慢就出现问题了。在某次上传文件到懒猫网盘的时候，我发现速度慢的可怜，几乎是走了公网。在 VIP 答疑群里得知，流量应该是从代理转了一圈，然后回来的，所以慢，剩下的就是解决这个问题了。

那么办法就是放行白名单，不让他走代理，由于是 DNS 访问，而很多代理的规则是根据域名匹配的，所以要去改这个匹配规则。当然如果你用nmtui 配置静态 IP 地址的话，那么内网访问也是没有问题了，直接走上级路由的默认路由表即可。

![image-20250513094205439](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250513094205439.png)



而白名单主要是放行， *.heiyu.space 和 *.lazycat.cloud 这两个域名，heiyu.space 是穿透服务，lazycat.cloud 是官网和论坛。



不同的软件有不同的设置办法，比如说用DOMAIN-SUFFIX来替代域名的泛解析，所以放行的时候heiyu.space 这这样子就好。我在修改配置文件的时候用DOMAIN-SUFFIX 匹配*.heiyu.space 不生效，花了不少的时间。实际不需要再写一次 * 号。

![image.png](https://dl.playground.lazycat.cloud/guidelines/459/9ed1bbce-73b0-4ce9-8e22-fb20d6c8b21c.png)



而最终落到配置文件上就是这样的。（之前写DOMAIN-SUFFIX,*.lazycat.cloud,DIRECT）一直不生效。

```
rules:
- DOMAIN-SUFFIX,lazycat.cloud,DIRECT
- DOMAIN-SUFFIX,heiyu.space,DIRECT
- DOMAIN-SUFFIX,deepseek.com,DIRECT
```

也总结一下其他规则吧，最常见的类型有这些：

### 1）DOMAIN

- 只匹配**某个域名本身**。
- 举例：`gs.apple.com` → 只有访问 `gs.apple.com` 才会命中。

### 2）DOMAIN-SUFFIX

- 匹配**所有以这个后缀结尾的域名**。
- 举例：`apple.com` → `gs.apple.com`、`itunes.apple.com` 都会命中。

### 3）DOMAIN-KEYWORD

- 匹配**包含某个关键词的所有域名**。
- 举例：`apple` → `apple.com`、`gs.apple.com`、`appleabc.xyz` 都会命中。

### 4）IP-CIDR

- 匹配**某个 IP 地址段**。
- 举例：`192.168.0.0/16` → 匹配 192.168 开头的所有 IP。

> 这些是规则写法里最基本的几种，掌握了就能应对绝大多数情况。


![image.png](https://lzc-playground-1301583638.cos.ap-chengdu.myqcloud.com/guidelines/459/ae810d7f-7410-489c-9017-987a12234160.png "image.png")



