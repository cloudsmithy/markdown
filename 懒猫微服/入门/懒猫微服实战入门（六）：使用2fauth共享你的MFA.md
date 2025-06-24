标题有点绕口，甚至听起来有点反直觉。

故事的背景是这样的，去参加了AWS的活动给的账户强制开MFA，但是我们还想团队内部share使用，于是产生了这个需求。

登录到AWS的控制台强制开了MFA，而且在第一次注册的时候强制绑定多因子验证。这也就意味着，其他人如果想登录这个账户就得随时call我，然后我去发给他数据验证码，这实在很不方便，所以想到了共享的MFA的需求。

![image-20250516164159950](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516164159950.png)







头几天逛商店看到的，觉得项目有点意思就下载了，没想到这么快用到了。懒猫商店，一键部署很方便，当成Saas服务来用，完全不考虑部署运维的事情。

![image-20250516163824579](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516163824579.png)



之前给小伙伴开了懒猫微服的账户，共享了planka来看项目进度，这次把2fauth的权限也添加给他。

![image-20250516163911970](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516163911970.png)

首先我这边先注册管理员的账户，默认是登录页面，需要切换一下。

![image-20250516164749502](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516164749502.png)

登录之后会提示绑定一下这个账户的MFA，我就是为了不在手机上安装MFA软件才用这个的，就不要套娃了。反正外面还有懒猫的验证系统，那个还有TLS加密，安全码验证。

![image-20250516164845425](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516164845425.png)



选择不绑定设备之后，在这里导入需要设置的MFA，这可以用摄像头或者导入二维码文件。我用的电脑端，所以直接在应用处截图，然后导入到这里了。

![image-20250516164821161](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516164821161.png)



点击最下面的导入，然后选择二维码 - 上传 就可以了。

![image-20250516165311672](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516165311672.png)



导入之后是这样的，可以二次确认签发机构。

![image-20250516165259782](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516165259782.png)

然后把生成的6位数字填写到aws控制台上，就可以成功验证了。

![image-20250516165435265](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516165435265.png)



在2fauth控制台上是这样的，点开就可以查看6位数字验证码。

![image-20250516165711375](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516165711375.png)



那么回到一开始的话题，怎么共享给其他账户呢？点击下方 - 管理员 - 用户 ，然后我们来新建一个普通用户。步骤基本和前面的一致。



![image-20250516165543137](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516165543137.png)



本来以为有用户组一类的概念，把两个用户和MFA放在一个组里达到share的目的，结果发现这个分组完全是用来区分的TAG。也没有找到把用户加到组里的操作。那就从管理员导出，再从下一个用户导入吧。



首先试了二维码，但是导入的时候就提示server error。于是查了了wiki，都是其他MFA软件导入2fauth的。无奈只能只能导出配置文件。名字叫做2fauth_export.json

![image-20250516170143799](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516170143799.png)





登录新用户的时候新建，然后选择文本文件。导入刚才的配置文件就可以了。



![image-20250516165311672](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250516165311672.png)

配置文件基本长这样：

```
{
  "app": "2fauth_v5.3.2",
  "schema": 1,
  "datetime": "2025-05-16T08:35:07.676665Z",
  "data": [
    {
      "otp_type": "totp",
      "account": "Q",
      "service": "AWS SSO",
      "icon": null,
      "icon_mime": null,
      "icon_file": null,
      "secret": "secretsss",
      "digits": 6,
      "algorithm": "sha1",
      "period": 30,
      "counter": null,
      "legacy_uri": "otpauth://totp/"
    }
  ]
}
```



整个过程有点绕，有人说每个人手机安装google authenticator扫一下不就好了吗？



**为什么采取这个方案？**

1. 之前用手机安装类似软件，每次去三里屯维修的时候都说返厂要把数据抹掉，下次还得重新绑定，还有一些软件只认MFA不认人。

   这过程不光折腾的够呛，而且Apple本身的问题还要MFA来买单。

2. 起初是想做一个类似于团队共享MFA的场景的，类似于RBAC，控制起来很灵活，但是实际体验下来是没有达到的。

3. 把最早的MFA二维码截图share出去也能扫，但是不确定有效时间。