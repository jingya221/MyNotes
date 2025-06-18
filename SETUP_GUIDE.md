# 📋 设置指南

这个指南将帮助您完整设置您的Markdown笔记系统并连接到GitHub。

## 🚀 初始设置步骤

### 1. 创建GitHub仓库

1. 登录到 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 仓库名称建议使用：`my-notes` 或 `markdown-notes`
4. 设置为 Public（这样可以使用GitHub Pages）
5. 不要初始化README（因为我们已经有了）
6. 点击 "Create repository"

### 2. 配置本地Git

在命令行中运行以下命令（替换为您的信息）：

```bash
# 设置用户信息
git config --global user.name "您的姓名"
git config --global user.email "您的邮箱@example.com"

# 添加所有文件到暂存区
git add .

# 进行首次提交
git commit -m "初始化Markdown笔记系统"

# 添加远程仓库（替换为您的GitHub用户名和仓库名）
git remote add origin https://github.com/您的用户名/您的仓库名.git

# 推送到GitHub
git push -u origin main
```

### 3. 启用GitHub Pages

1. 在GitHub仓库页面，点击 "Settings" 标签
2. 滚动到左侧菜单的 "Pages" 部分
3. 在 "Source" 下，选择 "Deploy from a branch"
4. 选择 "main" 分支和 "/ (root)" 文件夹
5. 点击 "Save"
6. 几分钟后，您的笔记网站将在以下地址可访问：
   `https://您的用户名.github.io/您的仓库名/`

## 📝 日常使用流程

### 创建新笔记

1. 在 `notes/` 文件夹中创建新的 `.md` 文件
2. 确保文件开头有一级标题（以 `#` 开始）
3. 编写您的笔记内容

### 更新索引并发布

```bash
# 方法1：使用Python脚本
python update_readme.py

# 方法2：使用批处理文件（Windows）
update_notes.bat

# 提交更改
git add .
git commit -m "添加新笔记: 笔记标题"
git push
```

## 🛠️ 高级配置

### 自动化工作流（可选）

您可以设置GitHub Actions来自动更新README：

1. 创建 `.github/workflows/` 文件夹
2. 添加自动化工作流文件

### 自定义样式（可选）

为了让GitHub Pages看起来更美观，您可以：

1. 在仓库设置中选择一个主题
2. 或者创建自定义CSS文件

## 🔧 故障排除

### 常见问题

1. **Python脚本运行错误**
   - 确保安装了Python 3.6+
   - 检查文件路径是否正确

2. **Git推送失败**
   - 检查网络连接
   - 验证GitHub用户名和密码/令牌

3. **GitHub Pages不显示**
   - 确保仓库是Public
   - 检查Pages设置是否正确
   - 等待几分钟让更改生效

## 📞 获取帮助

如果遇到问题，您可以：

- 查看GitHub官方文档
- 检查错误信息并搜索解决方案
- 在GitHub Issues中提问

---

*祝您使用愉快！ 📚✨* 