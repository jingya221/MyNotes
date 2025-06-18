# 欢迎使用Markdown笔记系统

!!! tip "系统简介"
    这是一个基于 MkDocs Material 主题的个人笔记管理系统，提供了美观、实用的文档展示功能。

## 🌟 系统特色

### Material Design 风格

采用 Google Material Design 设计语言：

- **现代化界面** - 简洁美观的视觉设计
- **响应式布局** - 完美支持各种设备
- **深色模式** - 支持明暗主题切换
- **丰富组件** - 提示框、标签页、代码高亮等

### 强大功能

!!! info "核心功能"
    - 🔍 **全文搜索** - 快速查找任何内容
    - 📱 **移动优先** - 手机端体验优秀
    - ⚡ **快速导航** - 左侧导航栏和面包屑
    - 🎯 **目录生成** - 自动生成页面目录

## 📚 内容组织

### 分类结构

笔记按以下方式组织：

```
docs/
├── index.md          # 首页
├── guide/            # 使用指南
│   ├── usage.md      # 基础使用
│   ├── add-notes.md  # 添加笔记
│   └── update-index.md # 更新索引
└── notes/            # 笔记内容
    ├── welcome.md    # 欢迎页面
    └── r-lang/       # R语言专题
        └── xpt-export-import.md
```

### Markdown 增强

支持丰富的 Markdown 扩展语法：

#### 提示框

!!! note "笔记"
    这是一个普通的笔记提示框

!!! tip "小贴士"
    这里是有用的小贴士

!!! warning "注意"
    这是需要注意的内容

!!! danger "重要"
    这是非常重要的信息

#### 代码高亮

支持多种编程语言的语法高亮：

```python title="Python 示例"
def fibonacci(n):
    """计算斐波那契数列"""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 测试
print(fibonacci(10))
```

```javascript title="JavaScript 示例"
const greet = (name) => {
    console.log(`Hello, ${name}!`);
};

greet('World');
```

#### 标签页

使用标签页组织相关内容：

=== "基础语法"
    ```markdown
    # 标题
    **粗体** *斜体*
    [链接](url)
    ```

=== "高级功能"
    ```markdown
    !!! tip "提示"
        这是提示内容
    
    === "标签页"
        标签页内容
    ```

=== "数学公式"
    ```markdown
    行内公式：$E = mc^2$
    
    块级公式：
    $$\sum_{i=1}^{n} x_i$$
    ```

#### 数学公式

支持 LaTeX 数学公式：

行内公式：$f(x) = ax^2 + bx + c$

块级公式：
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

#### 表格

| 功能 | 状态 | 说明 |
|------|------|------|
| 搜索 | ✅ | 全文搜索功能 |
| 深色模式 | ✅ | 主题切换 |
| 移动端 | ✅ | 响应式设计 |
| 目录 | ✅ | 自动生成 |

## 🎨 定制化

### 主题配置

在 `mkdocs.yml` 中可以自定义：

- **颜色方案** - primary 和 accent 颜色
- **字体选择** - 支持 Google Fonts
- **功能开关** - 启用/禁用特定功能
- **插件扩展** - 添加额外功能

### 个性化内容

可以添加：

- **自定义 CSS** - 个性化样式
- **JavaScript** - 交互功能
- **图标** - 丰富的图标库
- **社交链接** - GitHub、邮箱等

## 🚀 快速上手

### 第一步：熟悉界面

1. **顶部导航** - 网站标题和搜索框
2. **左侧导航** - 页面分类和目录
3. **主内容区** - 笔记正文
4. **右侧目录** - 当前页面的章节导航

### 第二步：创建笔记

1. 在 `docs/notes/` 目录下创建新文件
2. 使用 Markdown 语法编写内容
3. 更新 `mkdocs.yml` 中的导航配置
4. 推送到 GitHub 自动部署

### 第三步：享受写作

专注于内容创作，让系统处理其他一切！

!!! success "开始写作吧！"
    现在你已经了解了系统的基本功能，可以开始创建自己的笔记了。

## 📖 延伸阅读

- [Material for MkDocs 官方文档](https://squidfunk.github.io/mkdocs-material/)
- [Markdown 语法指南](https://www.markdownguide.org/)
- [GitHub Pages 文档](https://docs.github.com/en/pages)

---

> 💡 **提示**: 这个系统的灵感来源于 [CS自学指南](https://csdiy.wiki/)，感谢他们提供的优秀范例！ 