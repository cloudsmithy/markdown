

之前写好应用做好镜像想扔到懒猫微服上打包，都是先使用 buildx 打包双架构镜像，push 到 dockerhub 上，然后再用微服的copy image转成国内的镜像地址，这过程很麻烦。

因为在 Apple Silicon（如 M1/M2 芯片）设备上，默认运行的是 ARM 架构镜像（`linux/arm64`）。但有些镜像或依赖只支持 X86（`linux/amd64`）架构。

本文将介绍如何在 ARM 设备上拉取并运行 X86 镜像，以及如何保存和加载镜像。


### 🐳 拉取 X86 架构的 Docker 镜像

使用 `--platform=amd64` 参数即可拉取 X86 架构镜像：

```bash
docker pull --platform=amd64 nginx:latest
```

* `docker pull`：从远程仓库拉取镜像
* `--platform=amd64`：显式指定拉取 `x86_64` 架构的镜像
* `nginx:latest`：镜像名与标签

> 适用于在 M 系列 Mac 上使用 X86 镜像进行兼容性测试或运行仅支持 x86 的应用。

---

### 🔍 验证镜像的架构信息

拉取完成后，可通过以下命令确认镜像架构：

```bash
docker image inspect nginx:latest --format '{{.Os}}/{{.Architecture}}'
```

示例输出（成功拉取 X86 架构）：

```
linux/amd64
```

---

### ⚠️ 遇到的运行报错分析

执行以下命令尝试运行时：

```bash
docker run --rm -it --platform=amd64 nginx:latest
```

可能会出现如下错误：

```
docker: Error response from daemon: image with reference nginx:latest was found but its platform (linux/amd64) does not match the specified platform (darwin/amd64)
```

#### 📌 错误原因解析：

Docker 镜像是 **基于 Linux 内核** 的容器运行时，不支持 `darwin/amd64` 平台。你应显式指定目标平台为：

```bash
--platform=linux/amd64
```

####  ✅ 正确命令：

```bash
docker run --rm -it --platform=linux/amd64 nginx:latest
```

此时 Docker Desktop 会自动调用 `qemu` 进行跨架构模拟（无需额外配置），即在 ARM Mac 上模拟运行 X86 容器。

---

### 📦 Docker 镜像的保存与加载

Docker 提供 `save` 和 `load` 命令，支持将镜像打包导出为文件，便于备份或跨设备迁移。

####  ✅ 1. 保存镜像为 `.tar` 文件

```bash
 docker save -o nginx-amd64.tar nginx:latest
```

* `-o nginx-amd64.tar`：导出的文件名
* `nginx:latest`：指定要导出的镜像标签

也可以一次保存多个镜像：

```bash
docker save -o images.tar nginx:latest redis:alpine
```

---

#### ✅ 2. 加载 `.tar` 镜像文件

使用 SCP 或者 FTP 传到懒猫微服上，使用以下命令导入：

```bash
docker load -i nginx-amd64.tar
```

导入成功后镜像将出现在 `docker images` 列表中。

---

#### ✅ 3. 跨架构导入运行示例

如果你从懒猫微服上保存了镜像（如 `linux/amd64` 的 nginx），在 ARM Mac 上可通过以下方式运行：

```bash
docker run --rm -it --platform=linux/amd64 nginx:latest
```

---

#### ✅ 4. 导出为压缩文件（可选）

压缩后更便于传输：

```bash
docker save nginx:latest | gzip > nginx.tar.gz
```

解压并导入：

```bash
gunzip -c nginx.tar.gz | docker load
```

---


### 📝 小结

| 操作        | 命令                                                        |
| --------- | --------------------------------------------------------- |
| 拉取 X86 镜像 | `docker pull --platform=amd64 nginx:latest`               |
| 运行 X86 镜像 | `docker run --rm -it --platform=linux/amd64 nginx:latest` |
| 保存镜像      | `docker save -o nginx.tar nginx:latest`                   |
| 加载镜像      | `docker load -i nginx.tar`                                |



如果是在 懒猫微服 运行 ARM 镜像呢？

### ✅ 拉取 ARM 架构镜像（在 X86 主机上）

```bash
docker pull --platform=linux/arm64 nginx:latest
```

或简写为：

```bash
docker pull --platform=arm64 nginx:latest
```

这会拉取适用于 `linux/arm64` 的 nginx 镜像（即 ARM 设备如 Raspberry Pi 或 Apple Silicon 可运行的版本）。

---

### ✅ 运行 ARM 镜像（在 X86 上）

```bash
docker run --rm -it --platform=linux/arm64 nginx:latest
```

Docker Desktop 会通过内置的 QEMU 模拟 ARM 架构运行该容器。

> ⚠️ 前提是你的 Docker 环境启用了 QEMU 多平台支持（默认大多数 Docker Desktop 安装都已经启用）。

---

### ✅ 验证运行中的容器架构

方案一：确认 QEMU 是否已配置（X86 主机想运行 ARM 镜像）
如果你在 Intel / X86 主机上运行 --platform=linux/arm64，需要先启用跨架构支持：

```bash
docker run --rm --privileged multiarch/qemu-user-static --reset -p yes
```

![image-20250616232147019](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250616232147019.png)

进入容器执行：

```bash
uname -m
```

输出应为：

```
aarch64
```

说明该容器运行在 ARM 架构上。

![image-20250616232100579](https://raw.githubusercontent.com/cloudsmithy/picgo-imh/master/image-20250616232100579.png)


如果遇到：
exec /docker-entrypoint.sh: exec format error
意味着：你尝试在一个 与镜像架构不匹配的主机或模拟环境中运行该镜像，导致容器入口脚本无法被执行。

| 目标架构                       | `--platform` 参数          | 常见用途                      |
| -------------------------- | ------------------------ | ------------------------- |
| X86 (Intel/AMD)            | `linux/amd64`            | 默认平台，大多数镜像的标准版本           |
| ARM (如 M1/M2/Raspberry Pi) | `linux/arm64`            | 在 Apple Silicon 上或嵌入式设备运行 |
| 在 X86 上模拟 ARM              | `--platform=linux/arm64` | 跨架构测试、兼容性验证               |
