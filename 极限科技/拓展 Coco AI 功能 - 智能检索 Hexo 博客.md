---
title: 🚀 拓展 Coco AI 功能 - 智能检索 Hexo 博客
date: 2025-03-25 20:46:04
tags: []
categories: [极限科技]
---
# **🚀 拓展 Coco AI 功能 - 智能检索 Hexo 博客**

在之前的文章中，我们成功让 **Coco AI** 检索 **Hugo 博客**，这对于博客作者来说是一大福音。然而，从 **Hexo** 迁移到 **Hugo** 的成本不容小觑，毕竟大多数开发者对 **Node.js** 更熟悉，而 **Golang** 相对陌生。那么，既然 Coco AI 官方尚未支持 Hexo，是否有办法让它兼容 Hexo 呢？

当然可以！💡 既然 **Coco AI** 依赖的是 **Hugo 生成的 `index.json`** 进行检索，那我们干脆在 **Hexo** 中实现 **相同结构的 `index.json`**，这样就可以直接复用 Hugo 的数据结构，避免字段不兼容导致的潜在 Bug。

**接下来，我们将从 0 到 1 实现 Hexo 的智能检索功能！** 🚀

------

## **📌 1. 安装 Hexo 并切换到 Next 主题**

首先，我们需要安装 **Hexo** 并设置 **Next 主题**。

### **安装 Hexo**

```bash
pnpm install -g hexo-cli
hexo init my-blog
cd my-blog
pnpm install
```

启动本地服务器：

```bash
pnpm hexo s
```

访问 `http://localhost:4000/`，确保 Hexo 站点运行正常。

------

### **安装 Next 主题**

```bash
pnpm add hexo-theme-next
```

修改 `_config.yml`：

```yaml
theme: next
```

然后运行：

```bash
pnpm hexo clean && pnpm hexo s
```

访问 `http://localhost:4000/`，确认 Next 主题已生效。

------

## **📌 2. 安装 `hexo-generator-json-content`**

我们需要安装 **JSON 生成插件**，用于输出博客文章数据：

```bash
pnpm add hexo-generator-json-content
```

这些添加到 `_config.yml`，确保 Hexo 生成完整的 JSON 数据：

```yaml
jsonContent:
  meta: false
  pages: false
  posts:
    title: true
    date: true
    path: false
    permalink: true
    excerpt: true
    content: true
    categories: true
    tags: true
```

运行：

```bash
pnpm hexo clean && pnpm hexo generate
```

然后检查 `public/index.json`：

```bash
cat public/index.json
```

此时 JSON 已经生成，但 `url` 不是 **Hugo** 风格的，我们需要进一步优化。

------

## **📌 3. 自定义 `index.json` **

默认情况下，**Hexo 不会生成 `/YYYY/MM/DD/slug/` 格式的 URL**，因此我们需要手动调整。

### **📌 创建 `scripts/generate_index_json.js`**

在 **Hexo 站点目录** 下，创建 `scripts/generate_index_json.js`：

```js
hexo.extend.generator.register("index_json", function (locals) {
  let posts = locals.posts.sort("-date").map(post => {
    let category = post.categories && post.categories.length > 0 ? post.categories.data[0].name : null;
    let subcategory = post.categories && post.categories.length > 1 ? post.categories.data[1].name : null;
    let tags = post.tags ? post.tags.map(tag => tag.name) : null;

    // 解析发布日期
    let date = post.date;
    let formattedDate = `${date.year()}/${String(date.month() + 1).padStart(2, "0")}/${String(date.date()).padStart(2, "0")}`;
    
    // 生成 Hugo 风格 URL: `/YYYY/MM/DD/slug/`
    let postUrl = `/${formattedDate}/${post.slug || post.title.replace(/\s+/g, "-").toLowerCase()}/`;

    return {
      category: category,
      subcategory: subcategory,
      content: post.content.replace(/(<([^>]+)>)/gi, ""), // 去除 HTML 标签
      created: post.date.toISOString(),
      updated: post.updated ? post.updated.toISOString() : post.date.toISOString(),
      lang: "en", // 你可以修改为动态语言检测
      summary: post.excerpt || post.content.substring(0, 150) + "...",
      tags: tags,
      title: post.title,
      url: postUrl // 确保符合 Hugo 格式
    };
  });

  return {
    path: "index.json",
    data: JSON.stringify(posts, null, 2)
  };
});

```

------

## **📌 4. 重新生成 `index.json`**

运行：

```bash
pnpm hexo clean && pnpm hexo generate
```

然后检查 `public/index.json`：

```bash
cat public/index.json
```

你应该会看到 JSON 变成：

```json
[
  {
    "category": "Technology",
    "subcategory": "Web Development",
    "content": "This is a test post.",
    "created": "2025-03-20T12:00:00+08:00",
    "updated": "2025-03-20T12:00:00+08:00",
    "lang": "en",
    "summary": "This is a test post.",
    "tags": ["Hexo", "Static Site"],
    "title": "Hello World",
    "url": "/2025/03/20/hello-world/"
  }
]
```

✅ **成功让 URL 变成 `/YYYY/MM/DD/slug/` 格式！**

![image-20250320213141804](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250320213141804.png)

------

## **📌 5. 让 Coco AI 识别 Hexo 博客**

既然 `index.json` 已经生成，我们可以像 **Hugo** 那样，在 **Coco AI** 里添加 Hexo 博客的检索。

在 **Coco AI** 里，点击 **添加 Hugo Site**，然后输入：

```
http://host.docker.internal:4000/index.json
```

如果想测试数据同步，我们可以修改同步时间为 **1 秒**，以便实时观察更新情况。

![image-20250320213908270](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250320213908270.png)

------

## **📌 6. 观察数据同步情况**

过了一会，我们可以在 **Coco AI** 界面看到博客数据已经同步，**但前提是需要先添加模型！** ✅

Coco AI 的 **KNN（近邻搜索）** 会按照相关性对内容进行智能排序，使检索更高效！

![image-20250320214256274](https://raw.githubusercontent.com/Xu-Hardy/picgo-imh/master/image-20250320214256274.png)

------

## **🎯 总结**

| **步骤**                                  | **命令**                                           |
| ----------------------------------------- | -------------------------------------------------- |
| **安装 Hexo 并切换到 Next 主题**          | `pnpm install -g hexo-cli && hexo init my-blog`    |
| **安装 `hexo-generator-json-content`**    | `pnpm add hexo-generator-json-content`             |
| **修改 `_config.yml`**                    | 让 Hexo 生成 `index.json`                          |
| **创建 `scripts/generate_index_json.js`** | 确保 URL 变成 Hugo 风格                            |
| **生成 JSON**                             | `pnpm hexo clean && pnpm hexo generate`            |
| **在 Coco AI 里添加 Hexo 站点**           | 输入 `http://host.docker.internal:4000/index.json` |

------

## **🚀 结论**

🎉 通过本教程，你已经成功： 

✅ **让 Coco AI 兼容 Hexo 博客，实现智能检索**
✅ **复用 Hugo 的 `index.json` 结构，避免迁移成本**
✅ **让 URL 变成 `/YYYY/MM/DD/slug/` 以适配 Hugo Connector**
✅ **在 Coco AI 里成功同步 Hexo 博客数据，并进行智能查询**

💡 现在，你可以愉快地使用 **Hexo + Coco AI** 进行智能检索了！如果有 **更多定制需求**（如 `author`、`word count`），可以继续优化 `generate_index_json.js`！🔥🚀

