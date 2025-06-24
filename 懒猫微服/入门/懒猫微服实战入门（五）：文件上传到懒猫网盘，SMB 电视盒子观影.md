# 懒猫微服实战入门（五）：文件上传到懒猫网盘，SMB 电视盒子观影



作为一个合格的 NAS，肯定要有文件共享的功能，一般我们常用的是 SMB，NFS 和 WebDav这三种，然后需要设置共享目录和用户权限。

懒猫网盘提供了一个开箱即用的方案，直接通过APP 把网盘的文件夹映射自动挂载到本地，不需要像 Linux 那样 mount，也不需像 window 一样新建磁盘映射：



我们看看以前要挂载一个盘有多麻烦:

```
# Debian/Ubuntu
sudo apt install cifs-utils
sudo mkdir /mnt/smb_share
sudo mount -t cifs //SERVER_IP_OR_NAME/SHARE_NAME /mnt/smb_share -o username=SMB_USER,password=SMB_PASSWORD,domain=WORKGROUP

```

如果需要开机自动挂载，还得改/etc/fstab里面的条目。但是，懒猫网盘可以开箱即用，不管你是用浏览器，APP，还是用访达挂载SMB都访问都可以。属实是解放了Mac党的电脑空间。

![image-20250514104946937](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514104946937.png)



在网盘中点击自己的头像，然后**设置** - **网络服务**这里，可以看到设置。甚至点击起开内网服务，还会给一个 IP 地址的SMB地址：

`smb://ip/user-name`，电视盒子不能安装懒猫app，但是有了IP地址之后就可以连接SMB了～



![](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514105241675.png)

然后就是当贝盒子这里啦，如果你是小米盒子或者其他的盒子，只要文件管理器支持SMB就OK



![image-20250514113806260](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514113806260.png)



进入文件管理器，选择 **局域网共享连接**。



![image-20250514113737029](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514113737029.png)



然后输入懒猫微服的IP地址，用户名密码就是微服APP的， 这一套有点 AD 域的感觉了。

![image-20250514113708677](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514113708677.png)



如果你的文件管理器默认没有SMB也没有关系，还可以使用第三方应用进行 SMB 连接，比如这个 Github 项目，可以从 release 中下载 APK 进行安装。



![image-20250514113634937](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514113634937.png)

连接成功后，可对文件进行扫描和管理。



![图片](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514113612422.png)

通过以上配置，就可以在电视盒子上通过SMB连接NAS，开心的观看的4K电影了。



![image-20250514113307833](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250514113307833.png)