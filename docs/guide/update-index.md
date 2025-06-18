# 更新索引

!!! abstract "自动化管理"
    学习如何自动维护网站的索引和导航结构。

## 🔄 自动更新脚本

### Python 脚本

更新后的 `update_readme.py` 脚本现在支持 MkDocs 格式：

```python title="update_readme.py 核心功能"
def scan_mkdocs_notes():
    """扫描 docs/notes/ 目录下的所有笔记"""
    notes = []
    docs_dir = Path("docs/notes")
    
    for md_file in docs_dir.rglob("*.md"):
        # 提取笔记信息
        title = extract_title(md_file)
        category = get_category(md_file)
        mtime = get_modification_time(md_file)
        
        notes.append({
            'title': title,
            'category': category,
            'path': str(md_file.relative_to('docs')),
            'mtime': mtime
        })
    
    return notes

def update_mkdocs_config():
    """更新 mkdocs.yml 中的导航结构"""
    # 自动生成导航配置
    pass

def update_index_page():
    """更新首页的统计信息和最近更新列表"""
    # 更新 docs/index.md
    pass
```

### 批处理脚本

`update_notes.bat` 现在支持 MkDocs 工作流：

```batch title="update_notes.bat"
@echo off
echo 正在更新笔记索引...

python update_readme.py

echo 检查 Git 状态...
git status

set /p commit_msg="请输入提交消息 (或按回车使用默认消息): "
if "%commit_msg%"=="" set commit_msg=更新笔记索引

git add .
git commit -m "%commit_msg%"

set /p push_confirm="是否推送到 GitHub? (y/N): "
if /i "%push_confirm%"=="y" (
    git push
    echo 推送完成！GitHub Actions 将自动构建网站。
) else (
    echo 已提交到本地，未推送到远程仓库。
)

pause
```

## 📊 统计信息生成

### 笔记统计

脚本会自动计算：

- **总笔记数** - 统计所有 `.md` 文件
- **分类数** - 统计不同的目录分类
- **最近更新** - 按修改时间排序
- **最后更新时间** - 显示最新的修改时间

### 生成格式

更新后的首页格式：

```markdown
## 📊 笔记统计

<!-- 笔记索引开始 -->
📝 **总笔记数：X 个**  
📁 **分类数：Y 个**  
🔥 **最近7天更新：Z 个**  
📅 **最后更新：YYYY-MM-DD HH:MM:SS**
<!-- 笔记索引结束 -->

## 🔥 最近更新

- [**笔记标题**](notes/path/to/note.md) `分类名` *(YYYY-MM-DD)*
```

## 🗂️ 导航结构自动化

### 自动分类

脚本会根据目录结构自动生成导航：

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
    - R语言相关:
      - xpt导出&读取: notes/r-lang/xpt-export-import.md
    # 新分类会自动添加在这里
```

### 手动调整

如果需要手动调整导航顺序：

1. 编辑 `mkdocs.yml` 文件
2. 调整 `nav` 部分的顺序
3. 提交更改

!!! tip "最佳实践"
    - 让脚本自动生成基础结构
    - 手动调整重要页面的顺序
    - 使用清晰的文件夹层次结构

## 🚀 GitHub Actions 集成

### 触发条件

GitHub Actions 会在以下情况自动运行：

- **推送到 master 分支** - 自动构建和部署
- **Pull Request** - 预览构建（不部署）

### 构建过程

```yaml
# .github/workflows/docs.yml
jobs:
  build:
    steps:
      - name: 安装依赖
        run: |
          pip install mkdocs-material
          pip install mkdocs-minify-plugin
      
      - name: 构建网站
        run: mkdocs build
      
      - name: 部署到 GitHub Pages
        uses: actions/deploy-pages@v2
```

### 监控状态

可以在 GitHub 仓库的 Actions 标签页查看：

- **构建状态** - 成功/失败
- **构建日志** - 详细的执行信息
- **部署时间** - 从推送到生效的时间

## 📝 自定义脚本

### 扩展功能

可以根据需要扩展更新脚本：

```python title="自定义功能示例"
def generate_tags():
    """生成标签页面"""
    pass

def create_category_index():
    """为每个分类创建索引页面"""
    pass

def optimize_images():
    """压缩和优化图片"""
    pass

def check_links():
    """检查内部链接是否有效"""
    pass
```

### 配置选项

在脚本中添加配置选项：

```python
CONFIG = {
    'docs_dir': 'docs',
    'notes_dir': 'docs/notes',
    'exclude_files': ['.DS_Store', 'README.md'],
    'date_format': '%Y-%m-%d %H:%M:%S',
    'recent_days': 7,
    'auto_nav': True
}
```

## 🔧 故障排除

### 常见问题

!!! warning "构建失败"
    如果 GitHub Actions 构建失败：
    
    1. 检查 `mkdocs.yml` 语法是否正确
    2. 确保所有引用的文件都存在
    3. 查看 Actions 日志了解具体错误

!!! warning "链接失效"
    如果页面间链接不工作：
    
    1. 使用相对路径链接
    2. 确保文件路径大小写正确
    3. 避免使用特殊字符

### 调试模式

本地测试 MkDocs：

```bash
# 安装依赖
pip install mkdocs-material

# 本地预览
mkdocs serve

# 构建静态文件
mkdocs build
```

## ⚡ 性能优化

### 构建优化

- **启用缓存** - GitHub Actions 缓存依赖
- **并行构建** - 利用多核处理器
- **增量更新** - 只重建更改的页面

### 内容优化

- **图片压缩** - 使用合适的图片格式和大小
- **代码高亮** - 只加载需要的语言支持
- **搜索索引** - 优化搜索索引大小

!!! success "自动化收益"
    通过自动化更新脚本，你可以：
    
    - ⏰ 节省手动维护时间
    - 🔄 保持网站内容同步
    - 📈 提供准确的统计信息
    - 🎯 专注于内容创作而非维护 