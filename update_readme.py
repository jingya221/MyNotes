#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MkDocs笔记自动索引生成器
自动扫描docs/notes目录下的markdown文件，生成首页索引和导航配置
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def extract_title_from_markdown(file_path):
    """从markdown文件中提取标题"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
        # 查找第一个# 标题
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
        
        # 如果没有找到标题，使用文件名
        return Path(file_path).stem
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return Path(file_path).stem

def extract_description_from_markdown(file_path):
    """从markdown文件中提取描述（第一段文字）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # 去掉标题后的第一段非空文字
        lines = content.split('\n')
        description = ""
        found_title = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                found_title = True
                continue
            if found_title and line and not line.startswith('#') and not line.startswith('```') and not line.startswith('!!!'):
                # 取前50个字符作为描述，避免代码块
                description = line[:50] + ("..." if len(line) > 50 else "")
                break
        
        return description
    except Exception as e:
        return ""

def get_file_info(file_path):
    """获取文件信息"""
    stat = os.stat(file_path)
    modified_time = datetime.fromtimestamp(stat.st_mtime)
    
    # 获取相对于docs/notes文件夹的路径来确定分类
    relative_path = Path(file_path).relative_to(Path('./docs/notes'))
    category = str(relative_path.parent) if relative_path.parent != Path('.') else "根目录"
    
    return {
        'path': file_path,
        'title': extract_title_from_markdown(file_path),
        'description': extract_description_from_markdown(file_path),
        'category': category,
        'modified': modified_time,
        'size': stat.st_size,
        'relative_path': str(relative_path)
    }

def scan_notes_folder():
    """扫描docs/notes文件夹中的所有markdown文件"""
    notes_folder = Path('./docs/notes')
    if not notes_folder.exists():
        return []
    
    markdown_files = []
    for file_path in notes_folder.glob('**/*.md'):
        if file_path.is_file():
            file_info = get_file_info(file_path)
            markdown_files.append(file_info)
    
    # 按修改时间排序（最新的在前）
    markdown_files.sort(key=lambda x: x['modified'], reverse=True)
    return markdown_files

def generate_statistics(markdown_files):
    """生成统计信息"""
    if not markdown_files:
        return ""
    
    total_files = len(markdown_files)
    categories = set(file_info['category'] for file_info in markdown_files)
    total_categories = len(categories)
    
    # 最近更新统计
    today = datetime.now().date()
    recent_count = sum(1 for f in markdown_files if (today - f['modified'].date()).days <= 7)
    
    stats = [
        f"📝 **总笔记数：{total_files} 个**  ",
        f"📁 **分类数：{total_categories} 个**  ",
        f"🔥 **最近7天更新：{recent_count} 个**  ",
        f"📅 **最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**",
        ""
    ]
    
    return '\n'.join(stats)

def generate_recent_updates(markdown_files):
    """生成最近更新列表"""
    if not markdown_files:
        return ""
    
    content = []
    today = datetime.now().date()
    recent_files = [f for f in markdown_files if (today - f['modified'].date()).days <= 7]
    
    if recent_files:
        for file_info in recent_files[:5]:  # 只显示最近5个
            # MkDocs相对路径
            page_path = file_info['relative_path'].replace('\\', '/').replace('.md', '')
            modified_str = file_info['modified'].strftime('%Y-%m-%d')
            category_badge = f"`{file_info['category']}`" if file_info['category'] != "根目录" else ""
            description = f" - {file_info['description']}" if file_info['description'] else ""
            content.append(f"- [**{file_info['title']}**](notes/{page_path}) {category_badge} *({modified_str})*{description}")
    
    return '\n'.join(content)

def update_mkdocs_nav(markdown_files):
    """更新mkdocs.yml中的导航配置"""
    mkdocs_file = Path('./mkdocs.yml')
    if not mkdocs_file.exists():
        print("mkdocs.yml文件不存在！")
        return False
    
    with open(mkdocs_file, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file)
    
    # 按分类组织文件
    categories = defaultdict(list)
    for file_info in markdown_files:
        categories[file_info['category']].append(file_info)
    
    # 生成导航结构
    nav_notes = []
    for category, files in sorted(categories.items()):
        if category == "根目录":
            category_nav = []
            for file_info in sorted(files, key=lambda x: x['title']):
                page_path = file_info['relative_path'].replace('\\', '/')
                category_nav.append({file_info['title']: f"notes/{page_path}"})
            nav_notes.append({"根目录": category_nav})
        else:
            category_nav = []
            for file_info in sorted(files, key=lambda x: x['title']):
                page_path = file_info['relative_path'].replace('\\', '/')
                category_nav.append({file_info['title']: f"notes/{page_path}"})
            nav_notes.append({category: category_nav})
    
    # 更新导航配置
    if 'nav' in config:
        # 找到并更新笔记分类部分
        for i, item in enumerate(config['nav']):
            if isinstance(item, dict) and '笔记分类' in item:
                config['nav'][i]['笔记分类'] = nav_notes
                break
    
    # 写回文件
    with open(mkdocs_file, 'w', encoding='utf-8') as file:
        yaml.dump(config, file, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    return True

def update_index_page(markdown_files):
    """更新docs/index.md首页"""
    index_file = Path('./docs/index.md')
    if not index_file.exists():
        print("docs/index.md文件不存在！")
        return False
    
    # 按分类组织文件
    categories = defaultdict(list)
    for file_info in markdown_files:
        categories[file_info['category']].append(file_info)
    
    # 生成笔记目录内容
    notes_content = []
    for category in sorted(categories.keys()):
        notes_content.append(f"### {category}")
        files = categories[category]
        if files:
            for file_info in sorted(files, key=lambda x: x['title']):
                page_path = file_info['relative_path'].replace('\\', '/').replace('.md', '')
                description = f" - {file_info['description']}" if file_info['description'] else ""
                notes_content.append(f"- [{file_info['title']}](notes/{page_path}){description}")
        else:
            notes_content.append("*该分类暂无笔记*")
        notes_content.append("")
    
    # 生成统计信息
    total_files = len(markdown_files)
    total_categories = len(categories)
    latest_note = markdown_files[0]['title'] if markdown_files else "无"
    
    # 构建新的首页内容
    new_content = f"""# 📚 个人笔记系统

欢迎来到我的个人笔记管理系统！这里收录了各种学习笔记和技术文档。

## 📋 笔记目录

{chr(10).join(notes_content).rstrip()}
## 🔧 使用指南

- [基础使用指南](guide/usage.md) - 了解如何使用这个笔记系统
- [添加新笔记](guide/add-notes.md) - 学习如何创建和组织新的笔记文件  
- [更新索引](guide/update-index.md) - 如何自动更新和维护笔记索引

## 📊 统计信息

- **笔记分类**: {total_categories}个
- **总笔记数**: {total_files}篇
- **最近更新**: {latest_note}

---

> 💡 **提示**: 点击左侧导航栏可以快速浏览所有笔记分类，使用顶部搜索功能可以快速查找内容。"""
    
    # 写入文件
    with open(index_file, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    return True

def main():
    """主函数"""
    print("🔍 正在扫描docs/notes目录...")
    
    # 扫描笔记文件
    markdown_files = scan_notes_folder()
    
    if not markdown_files:
        print("❌ 未找到任何markdown文件！")
        return
    
    print(f"📝 找到 {len(markdown_files)} 个笔记文件")
    
    # 更新首页
    if update_index_page(markdown_files):
        print("✅ 已更新首页 (docs/index.md)")
    else:
        print("❌ 更新首页失败")
    
    # 更新导航配置
    if update_mkdocs_nav(markdown_files):
        print("✅ 已更新导航配置 (mkdocs.yml)")
    else:
        print("❌ 更新导航配置失败")
    
    print("\n📊 统计信息:")
    categories = set(f['category'] for f in markdown_files)
    for category in sorted(categories):
        count = len([f for f in markdown_files if f['category'] == category])
        print(f"  {category}: {count} 个文件")
    
    print(f"\n🎉 更新完成！请运行 'mkdocs serve' 预览效果")

if __name__ == "__main__":
    main() 