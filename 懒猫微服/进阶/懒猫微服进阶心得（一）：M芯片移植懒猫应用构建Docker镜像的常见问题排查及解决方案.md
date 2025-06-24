> 本文是使用 Apple silicon 的 MacOS 移植到懒猫商店的踩坑记录，希望能够给大家带来帮助

Apple silicon 很好，在这年几乎带起来 ARM 的生态。但这也拉开了 ARM 和 X86 之战，用户在两大生态中穿梭，只能增加自己应用的兼容性。就比如说用来打包的Docker image，尽管编程语言和操作系统都在底层屏蔽了硬件架构，但是容器还得用相同架构的。

这是之前移植开源项目时候忘记打包不同架构的 image 而直接推送到懒猫镜像仓库导致的问题。MacOS 默认打包了 ARMv8 架构的镜像，在 X86上也无法运行。

```bash
pg-docker run -p 5000:5500 registry.lazycat.cloud/u04123229/you/doudizhu-scorer:d1d9085174c0bf8c
WARNING: The requested image's platform (linux/arm64/v8) does not match the detected host platform (linux/amd64/v4) and no specific platform was requested
```



由于打包的时候容器一直在反复重启，所以在dozzle 上也没有什么明显的报错，所以有个办法就是ssh 进去用终端**pg-docker run**，这样所见即所得。dozzle 地址：https://dev.<name>.heiyu.space/dozzle/



于是重新打包，跨架构打包时候需要使用 buildx，当然前提是需要里面的运行时和代码也是跨平台的。

我们先来看概念和原理：



`buildx` 是 Docker 提供的一种扩展功能，它基于 **BuildKit** 引擎，目的是为 Docker 提供更强大的构建功能，包括：

- **跨平台构建**：支持在一种平台上构建适用于多种平台的 Docker 镜像。
- **缓存管理**：支持高效的缓存管理机制，能够减少重复构建的时间。
- **多阶段构建**：支持复杂的多阶段构建流程。

`buildx` 使 Docker 能够生成多平台的镜像，这意味着你可以在一个平台上（例如 ARM 或 x86）构建适用于其他平台（如 `x86_64`、`arm64`、`armv7` 等）的 Docker 镜像。



 `docker buildx build` 通过指定 `--platform` 参数来告诉 Docker 在构建时要生成哪些平台的镜像。例如，`linux/amd64` 和 `linux/arm64` 就分别对应 x86 和 ARM 架构。



 在 `buildx` 构建完成后，你得到的不是一个单独的镜像，而是一个支持多平台的 **manifest list**，这个列表包含了不同架构的镜像。这个列表可以推送到 Docker Hub 等镜像仓库，客户端在拉取时，会根据自己的硬件架构自动选择合适的镜像。

这意味着，我们可以通过同一个镜像标签（如 `your_image_name`）来支持多个平台的 Docker 镜像，而用户在拉取时会自动选择适合自己平台的镜像。

1. **准备构建环境**：
    Docker Buildx 会首先准备并选择一个构建器（builder）。这个构建器负责在指定的平台上执行构建任务。
2. **选择平台**：
    使用 `--platform` 参数来选择目标平台，Docker 会通过 QEMU 模拟器或者本地平台来执行构建。
3. **构建镜像**：
    在选择平台后，Buildx 会根据 Dockerfile 和其他构建上下文开始构建镜像。它会处理平台特定的依赖和构建步骤。
4. **生成适配镜像**：
    对于每个平台，Docker Buildx 会生成一个特定的镜像。例如，对于 `linux/amd64` 和 `linux/arm64`，它会分别为这两个平台构建独立的镜像，并将它们绑定在一个 **manifest list** 中。
5. **推送镜像**：
    完成构建后，你可以使用 `--push` 参数将包含多个架构镜像的 **manifest list** 推送到 Docker Hub 或其他镜像仓库。这个清单包含了多个平台的镜像，当用户从仓库拉取时，Docker 会自动选择与用户当前平台兼容的镜像



#### 然后来实操

1. 确保 Docker 版本支持 Buildx,用`docker buildx version` 来验证/
2. 创建并使用新的 Builder
3. 打包的时候加上平台参数：`--platform linux/amd64,linux/arm64`

具体命令如下：

```
docker buildx version
docker buildx create --use --name multiarch-builder
docker buildx build --platform linux/amd64 -t your_image_name . 
docker buildx build --platform linux/amd64 -t your_dockerhub_username/your_image_name --push .
```



在这过程中，我们可能还会使用`docker tag` ，这个命令可以将一个现有的镜像打上新的标签（tag），通常用于将镜像标记为自己的名字或指定版本。这对于推送镜像到 Docker Hub 或其他镜像仓库时非常有用。

```bash
docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
```

- **`SOURCE_IMAGE[:TAG]`**：要打标签的源镜像。`TAG` 是可选的，如果不指定，默认是 `latest`。
- **`TARGET_IMAGE[:TAG]`**：新的目标标签，通常你可以为镜像指定一个新的名字或版本号。

假设你有一个名为 `my_image:latest` 的镜像，并且你希望将它标记为属于你自己（例如，`your_dockerhub_username/my_image:latest`）：

   ```bash
   docker tag my_image:latest your_dockerhub_username/my_image:latest
   ```

 这条命令会将 `my_image:latest` 镜像打上 `your_dockerhub_username/my_image:latest` 的标签。




推送到 dockerhub 之后，然后就可以像往常一样使用 Docker 了。

```
docker pull your_dockerhub_username/your_image_name
docker run your_dockerhub_username/your_image_name
```



如果想走 Github action 一键打包 image 的话，是这样：

```yml
name: Build and Push Docker Image

on:
  push:
    tags:
      - 'v*'  # 仅在 tag push（如 v1.0.0）时触发

jobs:
  build-and-push:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout source code
      uses: actions/checkout@v4

    - name: Check DockerHub secrets
      run: |
        if [ -z "${{ secrets.DOCKER_USERNAME }}" ] || [ -z "${{ secrets.DOCKER_PASSWORD }}" ]; then
          echo "❌ ERROR: DOCKER_USERNAME or DOCKER_PASSWORD is missing"
          exit 1
        fi

    - name: Set up QEMU
      uses: docker/setup-qemu-action@v3

    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v3
      with:
        install: true  # ✅ 自动创建默认 builder

    - name: Docker login
      uses: docker/login-action@v3
      with:
        username: ${{ secrets.DOCKER_USERNAME }}
        password: ${{ secrets.DOCKER_PASSWORD }}

    - name: Extract tag name
      id: vars
      run: echo "TAG=${GITHUB_REF#refs/tags/}" >> $GITHUB_ENV

    - name: Build and push Docker image (multi-arch + latest)
      uses: docker/build-push-action@v5
      with:
        context: .
        push: true
        platforms: linux/amd64,linux/arm64
        tags: |
          cloudsmithy/flask-demo:${{ env.TAG }}
          cloudsmithy/flask-demo:latest
```



没有把lzc-cli写进去的原因是目前只能从终端命令行查看到推送到懒猫仓库的镜像命令，目前还不能存到一个中间位置，所以做了一个通用的版本。



事情到这里本来应该结束的，但似乎有了新的故事。



#### 故事1：无法打包

某次在打包的过程种突然报错，期间一度以为 Orbstack 出现了问题，于是卸载重装，重启电脑，均无效，GPT 和 deepseek 也只是让我检查网络连接。期间重新 docker pull 也是没问题的。


```
characters ERROR: failed to dial qRPC: rpc error:code = Internal desc = rpc error: code = Internal desC = header key "x-docker-expoSe-session-name" contains value with non-printable ASCI #2793
```

无奈只能Google，在issue里有一个评论，打包目录不能出现中文。(我的OS默认中文) 参考链接：https://github.com/docker/buildx/issues/2793





#### 故事2：构建之后没有输出

`docker buildx build --platform linux/amd64 -t your_image_name .`

```
WARNING: No output specified with docker-container driver. Build result will only remain in the build cache. To push result image into registry use --push or to load image into docker use --load

```

这是使用 `docker buildx` 构建镜像时，指定了 `docker-container` 驱动，但是没有使用 `--push` 或 `--load` 参数。结果是，构建的镜像只会保留在构建缓存中，而不会被推送到镜像仓库或加载到本地 Docker 环境中。

我们可以通过两种方式之一来明确指定输出目标，避免出现此警告：

##### 1. **使用 `--push` 将镜像推送到远程仓库**：

如果你希望构建的镜像推送到 Docker Hub 或其他 Docker 镜像仓库，可以使用 `--push` 参数。例如：

```bash
docker buildx build --platform linux/amd64 -t your_image_name --push .
```

这将把镜像推送到 Docker 仓库，而不是仅保留在本地构建缓存中。

##### 2. **使用 `--load` 将镜像加载到本地 Docker 环境**：

如果你想将构建的镜像加载到本地 Docker 环境中以便后续使用（例如运行容器），可以使用 `--load` 参数：

```bash
docker buildx build --platform linux/amd64 -t your_image_name --load .
```

这会将构建的镜像加载到本地 Docker 环境，使你可以在本地运行、调试或进行其他操作。



#### 故事3：无法同时保存双平台Image到本地

```
docker buildx build --platform linux/amd64,linux/arm64 -t cloudsmithy/shuangpin:latest . --load
[+] Building 0.0s (0/0) docker-container:stoic_hellman
ERROR: docker exporter does not currently support exporting manifest lists
```



`--load` 只适用于单平台构建。如果你在跨平台构建（如 `linux/amd64,linux/arm64`）时使用 `--load`，则只会将构建的默认平台镜像加载到本地，不会加载所有平台的镜像。跨平台构建时，通常需要使用 `--push` 将所有平台的镜像推送到远程仓库

```
docker buildx build --platform linux/amd64 -t cloudsmithy/shuangpin:latest . --load
```



使用 `--load` 时，镜像会被加载到本地 Docker 守护进程中。对于大镜像，加载过程可能需要较长的时间和较多的本地存储空间。因此，如果镜像非常大，可能需要考虑是否使用 `--push` 直接推送到远程仓库，而不是将其加载到本地。

```bash
docker buildx build --platform linux/amd64,linux/arm64 -t cloudsmithy/shuangpin:latest . --push
```



#### 故事3：懒猫仓库黑魔法

对了，关于文档上提到的懒猫的registry不能在微服外面用，黑魔法的限制其实就是加了认证，直接返回401.

```bash
docker run -p 5000:5500 registry.lazycat.cloud/u04123229/you/doudizhu-scorer:d1d9085174c0bf8c
Unable to find image 'registry.lazycat.cloud/u04123229/you/doudizhu-scorer:d1d9085174c0bf8c' locally
docker: Error response from daemon: Head "https://registry.lazycat.cloud/v2/u04123229/you/doudizhu-scorer/manifests/d1d9085174c0bf8c": no basic auth credentials.
```

  
  #### 最后

希望这篇文章能够帮助大家在将开源项目移植到懒猫商店时，避免遇到一些常见的坑和问题。祝大家顺利解决跨平台构建和镜像推送中的挑战，提升开发效率！

  
  