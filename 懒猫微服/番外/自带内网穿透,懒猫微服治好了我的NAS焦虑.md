知道懒猫微服是一两年前，最初的印象是极客机甲风格，有颜值有性能有。近期入手也是出于朋友推荐,主要还是喜欢自带的内网穿透功能,虽然家里有公网IP，但是不定时会被运营商封端口（不止常用端口），总是一阵一阵的，询问运营商也没有一个明确的结论，倒不如选一个商业的产品然后省去自己折腾的时间吧

虽然我一直很想DIY这样一款产品，开源的大多是KVM-base的方案，或者还有商业的EXSI。毕竟个人精力有限，一直搁置到现在，然后随着事情越来越多，就购买了一台来玩玩，也脱胎换骨当甲方提需求。官网如下：https://lazycat.cloud/

![image-20250504201210064](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250504201210064.png)

机器是这样的，浓浓的机甲风格连，着运行了几天也一点都不烫。之前还担心炒豆子的问题，其实相对于白天的噪音几乎是没有的。

- i5-1135G7，现在来看不算最新的，不过也比很多NAS强很多了，手动@群晖

- 32G内存（只能一个盘位，所以加满了）

- 2.5寸 2T 原装HDD（预算有限，目前还在测试阶段，自带的盘是叠瓦盘，介意的话可以自己买盘替换）

  

![image-20250504200345665](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250504200345665.png)



neofetch能看到是基于Debian12的。然后开发团队在上层构建自己的应用，只是ssh需要额外申请，不过一会就批了。

![image-20250504202608288](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250504202608288.png)



提供全平台的客户端，该有的都有了，这里开发适配应该花了不少时间吧。

![image-20250504195908460](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250504195908460.png)





MacOS客户端的界面如下, 如果通过web访问就是这样，和传统的群晖有个主页不一样，这个更像是服务导向的，对于小白来说，只需要按照Sass的方式来使用，比如文件备份，时间机器，异地组网。而对于技术人员来讲，我个人觉得是更加吃力一些，要搞清楚每个服务是怎么启动的，怎么保证网络传输，怎么保证HA，尽管懒猫团队已经实现了这些，但是出于职业习惯，还是希望抽丝剥茧，搞清楚从Iass到Sass的原理，然后学一学背后的哲学，以及在懒猫的商店上架自己应用，还有把应用接入懒猫的SSO系统。

![image-20250504171611929](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250504171611929.png)



关于服务嘛，是大多数玩家最喜欢的地方，有专门的N 对1答疑，7*18服务比7 *24 听起来要靠谱很多，只能说专业，太专业了。团队是deepin二次创业出来的，都是技术流，所以懂用户，在群里可以做深度的技术答疑。在我之前的感受就是，玩nas的太多是爱好者，很多不懂Linux和开发，或者懂技术的都是理论派，对自己host-server或者application没有兴趣。以前的同事能因为这个结缘，由于彼此方向不同更多会集中在Iass和network的层面，而端对端的解决方案甚少。

但是懒猫让我看到了未来nas进化的方向，从硬件  - Iass -pass - Sass 做了全套的定制，也做了我一直想做而没有做完的事情，最早我的想发是在Centos上用docker跑很服务，然后用NFS做share，然后用KVM做虚拟化层，然后用商业的方案做异地组网。尽管过过程十分坎坷，遇到了硬盘噪音，纯开源项目支持不到位，商业方案售后不专业等问题，最后就只在内网使用，走了很多弯路吧。



相信懒猫的这个价格，如果用AWS的话，最多半年就烧光credit了。有如此专业的团队来支持，治好了我的NAS焦虑。



![image-20250504201658519](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250504201658519.png)




文章来源：



![image.png](https://lzc-playground-1301583638.cos.ap-chengdu.myqcloud.com/guidelines/459/c24bffd1-eb1f-40fa-9dc6-bc5dc9337601.png "image.png")
