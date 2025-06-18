# 添加笔记

!!! info "前置条件"
    确保你已经熟悉基本的 [使用方法](usage.md)。

## 📝 创建新笔记

### 方法一：直接在 GitHub 上创建

1. 访问 [GitHub 仓库](https://github.com/jingya221/MyNotes)
2. 进入 `docs/notes/` 目录
3. 点击 "Create new file" 按钮
4. 输入文件名，如 `new-note.md`
5. 编写内容并提交

### 方法二：本地创建并推送

```bash
# 克隆仓库
git clone https://github.com/jingya221/MyNotes.git
cd MyNotes

# 创建新笔记
touch docs/notes/my-new-note.md

# 编辑内容
# 使用你喜欢的编辑器编写内容

# 提交更改
git add .
git commit -m "添加新笔记: my-new-note"
git push
```

## 📂 文件组织

### 目录结构

```
docs/
├── index.md           # 首页
├── guide/            # 使用指南
│   ├── usage.md
│   ├── add-notes.md
│   └── update-index.md
└── notes/            # 笔记内容
    ├── welcome.md    # 根目录笔记
    └── r-lang/       # R语言分类
        └── xpt-export-import.md
```

### 分类建议

!!! tip "分类原则"
    - 按**学科领域**分类：如 `python/`, `r-lang/`, `statistics/`
    - 按**项目类型**分类：如 `projects/`, `tutorials/`, `references/`
    - 按**难度级别**分类：如 `beginner/`, `intermediate/`, `advanced/`

## ✍️ 编写规范

### Markdown 语法

使用标准 Markdown 语法，支持 Material for MkDocs 扩展：

```markdown
# 一级标题

## 二级标题

### 三级标题

**粗体文本**

*斜体文本*

- 无序列表
- 项目二

1. 有序列表
2. 项目二

[链接文本](http://example.com)

![图片描述](image.png)
```

### 代码块

支持语法高亮和标题：

````markdown
```python title="示例代码"
def hello():
    print("Hello, World!")
```
````

### 提示框

使用各种提示框来突出重要信息：

```markdown
!!! note "笔记"
    这是一个笔记提示框

!!! tip "小贴士"
    这是一个小贴士

!!! warning "注意"
    这需要特别注意

!!! danger "重要"
    这是重要信息
```

### 数学公式

支持 LaTeX 数学公式：

```markdown
行内公式：$E = mc^2$

块级公式：
$$
\frac{d}{dx}\left( \int_{0}^{x} f(u)\,du\right)=f(x)
$$
```

## 🏷️ 元数据设置

### Front Matter

虽然 MkDocs 不需要 Front Matter，但可以通过文件名和目录结构来组织：

```markdown
# 文件：docs/notes/python/data-analysis.md
# 会在导航中显示为：笔记分类 > Python > 数据分析

# 数据分析入门

内容开始...
```

### 更新导航

编辑 `mkdocs.yml` 添加新页面：

```yaml
nav:
  - 首页: index.md
  - 使用指南:
    - 如何使用: guide/usage.md
    - 添加笔记: guide/add-notes.md
    - 更新索引: guide/update-index.md
  - 笔记分类:
    - 根目录:
      - 欢迎使用Markdown笔记系统: notes/welcome.md
    - Python:
      - 数据分析: notes/python/data-analysis.md
    - R语言相关:
      - xpt导出&读取: notes/r-lang/xpt-export-import.md
```

## 🖼️ 添加图片

### 图片存储

建议在 `docs/` 下创建 `images/` 目录：

```
docs/
├── images/
│   ├── logo.png
│   └── screenshots/
│       └── example.png
└── notes/
    └── my-note.md
```

### 引用图片

```markdown
# 相对路径引用
![示例图片](../images/example.png)

# 或者使用在线图片
![GitHub Logo](https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png)
```

## 📊 表格制作

支持标准 Markdown 表格：

```markdown
| 功能 | 描述 | 状态 |
|------|------|------|
| 搜索 | 全文搜索功能 | ✅ |
| 深色模式 | 主题切换 | ✅ |
| 移动端 | 响应式设计 | ✅ |
```

## 🔗 内部链接

### 页面间链接

```markdown
# 链接到其他笔记
参考 [使用指南](../guide/usage.md) 获取更多信息。

# 链接到同一页面的章节
查看上面的 [文件组织](#文件组织) 章节。
```

### 自动链接

MkDocs 会自动处理相对路径链接，确保在网站中正确工作。

## ✅ 检查清单

添加新笔记时的检查清单：

- [ ] 文件名使用小写和连字符
- [ ] 内容结构清晰，有适当的标题层级
- [ ] 代码块有正确的语言标识
- [ ] 图片路径正确
- [ ] 内部链接可以正常工作
- [ ] 更新了 `mkdocs.yml` 中的导航
- [ ] 提交了更改并推送到 GitHub

!!! success "完成"
    当你完成以上步骤后，GitHub Actions 会自动构建和部署你的网站！ 