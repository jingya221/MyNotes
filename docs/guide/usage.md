# 如何使用

!!! abstract "指南简介"
    这份指南将帮助你快速上手个人笔记管理系统，学会如何添加、编辑和管理你的笔记。

## 🎯 快速开始

### 浏览笔记

使用左侧导航栏可以按分类浏览笔记：

- **根目录** - 系统介绍和基础内容
- **R语言相关** - R语言学习笔记
- 更多分类会随着内容增加自动出现

### 搜索功能

- 点击顶部的搜索框
- 输入关键词可以搜索笔记标题和内容
- 支持中文和英文搜索

!!! tip "搜索技巧"
    - 尝试使用关键词的不同组合
    - 可以搜索代码片段中的函数名
    - 支持模糊搜索

## 📝 添加新笔记

### 第一步：创建文件

在相应的分类目录下创建新的 Markdown 文件：

```bash
# 在 docs/notes/ 目录下创建新文件
touch docs/notes/new-note.md

# 或在子分类下创建
touch docs/notes/r-lang/new-r-note.md
```

### 第二步：编写内容

使用标准的 Markdown 语法编写笔记：

```markdown
# 笔记标题

## 主要内容

这里是笔记的主要内容...

### 代码示例

​```python
def hello_world():
    print("Hello, World!")
​```

!!! note "提示"
    这是一个提示框
```

### 第三步：更新导航

编辑 `mkdocs.yml` 文件中的 `nav` 部分，添加新页面：

```yaml
nav:
  - 首页: index.md
  - 笔记分类:
    - 根目录:
      - 新笔记: notes/new-note.md
```

## 🔄 更新索引

使用提供的脚本自动更新索引：

=== "Python脚本"
    ```bash
    python update_readme.py
    ```

=== "批处理文件"
    ```bash
    ./update_notes.bat
    ```

!!! warning "注意"
    更新脚本会自动扫描 `docs/notes/` 目录，更新首页的统计信息和最近更新列表。

## 🎨 格式化技巧

### 使用提示框

MkDocs Material 支持多种提示框：

!!! note "笔记"
    这是一个普通提示

!!! tip "技巧"
    这是一个小贴士

!!! warning "警告"
    这需要注意

!!! danger "危险"
    这很重要！

### 代码高亮

支持多种编程语言的语法高亮：

```python title="Python代码示例"
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

```r title="R代码示例"
# 生成随机数据
data <- rnorm(100, mean = 0, sd = 1)
summary(data)
```

### 标签页

使用标签页组织相关内容：

=== "基础用法"
    这是基础内容

=== "高级用法"
    这是高级内容

=== "专家级"
    这是专家级内容

## 🚀 部署说明

网站使用 GitHub Actions 自动部署：

1. 推送代码到 `master` 分支
2. GitHub Actions 自动构建 MkDocs 网站
3. 自动部署到 GitHub Pages

!!! success "自动化流程"
    - ✅ 代码推送触发构建
    - ✅ 自动安装依赖
    - ✅ 生成静态网站
    - ✅ 部署到 GitHub Pages

## 📱 移动端优化

网站完全响应式设计：

- **手机端** - 侧边栏可折叠
- **平板端** - 适配中等屏幕
- **桌面端** - 充分利用大屏空间

## 🎉 更多功能

- **深色模式** - 点击右上角切换主题
- **目录导航** - 长文章自动生成目录
- **返回顶部** - 长页面自动显示返回按钮
- **编辑链接** - 每页都有 GitHub 编辑链接

---

!!! question "需要帮助？"
    如果你在使用过程中遇到问题，可以：
    
    - 查看 [添加笔记](add-notes.md) 的详细说明
    - 阅读 [更新索引](update-index.md) 的自动化配置
    - 在 GitHub 仓库提交 Issue 