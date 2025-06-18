#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新README.md中的笔记索引
扫描notes文件夹中的所有markdown文件，并更新README.md中的目录
支持分类显示和更好的目录结构
"""

import os
import re
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
            if found_title and line and not line.startswith('#') and not line.startswith('```'):
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
    
    # 获取相对于notes文件夹的路径来确定分类
    relative_path = Path(file_path).relative_to(Path('./notes'))
    category = str(relative_path.parent) if relative_path.parent != Path('.') else "根目录"
    
    return {
        'path': file_path,
        'title': extract_title_from_markdown(file_path),
        'description': extract_description_from_markdown(file_path),
        'category': category,
        'modified': modified_time,
        'size': stat.st_size
    }

def scan_notes_folder():
    """扫描notes文件夹中的所有markdown文件"""
    notes_folder = Path('./notes')
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
        f"## 📊 统计信息",
        "",
        f"- 📝 **总笔记数：{total_files} 个**",
        f"- 📁 **分类数：{total_categories} 个**", 
        f"- 🔥 **最近7天更新：{recent_count} 个**",
        f"- 📅 **最后更新：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**",
        "",
        "---",
        ""
    ]
    
    return '\n'.join(stats)

def generate_index_content(markdown_files):
    """生成目录索引内容 - 简化版，仅更新统计信息和最近更新"""
    if not markdown_files:
        return "*目前还没有笔记，快去创建第一个笔记吧！*\n"
    
    content = []
    
    # 添加统计信息
    content.append(generate_statistics(markdown_files))
    
    # 按修改时间分组 - 最近更新
    today = datetime.now().date()
    recent_files = [f for f in markdown_files if (today - f['modified'].date()).days <= 7]
    
    if recent_files:
        content.append("## 🔥 最近更新\n")
        for file_info in recent_files[:5]:  # 只显示最近5个
            # 使用Jekyll相对URL
            file_path = str(file_info['path']).replace('\\', '/')
            # 转换为Jekyll页面路径
            if file_path.startswith('notes/'):
                page_path = file_path.replace('.md', '/').replace('notes/', '')
                relative_path = f"{{{{ site.baseurl }}}}/notes/{page_path}"
            else:
                relative_path = f"{{{{ site.baseurl }}}}/{file_path.replace('.md', '/')}"
            
            modified_str = file_info['modified'].strftime('%Y-%m-%d')
            category_badge = f"`{file_info['category']}`" if file_info['category'] != "根目录" else ""
            description = f" - {file_info['description']}" if file_info['description'] else ""
            content.append(f"- [**{file_info['title']}**]({relative_path}) {category_badge} *({modified_str})*{description}")
        content.append("")
    
    return '\n'.join(content)

def update_file(file_path, markdown_files):
    """更新指定的markdown文件"""
    if not file_path.exists():
        print(f"{file_path.name}文件不存在！")
        return False
    
    # 读取当前文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 生成新的索引内容
    index_content = generate_index_content(markdown_files)
    
    # 替换索引部分
    start_marker = '<!-- 笔记索引开始 -->'
    end_marker = '<!-- 笔记索引结束 -->'
    
    pattern = f'{re.escape(start_marker)}.*?{re.escape(end_marker)}'
    new_section = f'{start_marker}\n{index_content}{end_marker}'
    
    if re.search(pattern, content, re.DOTALL):
        new_content = re.sub(pattern, new_section, content, flags=re.DOTALL)
    else:
        print(f"未找到索引标记，请检查{file_path.name}格式！")
        return False
    
    # 更新最后更新时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_content = re.sub(
        r'\*最后更新:.*?\*',
        f'*最后更新: {current_time}*',
        new_content
    )
    
    # 写入文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    return True

def update_readme():
    """更新README.md和index.md文件"""
    # 扫描笔记文件
    markdown_files = scan_notes_folder()
    
    success_count = 0
    files_to_update = [
        Path('./README.md'),
        Path('./index.md')
    ]
    
    for file_path in files_to_update:
        if file_path.exists():
            if update_file(file_path, markdown_files):
                print(f"✅ {file_path.name} 已更新！")
                success_count += 1
            else:
                print(f"❌ {file_path.name} 更新失败！")
        else:
            print(f"⚠️ {file_path.name} 文件不存在，跳过更新")
    
    if success_count > 0:
        print(f"📊 找到 {len(markdown_files)} 个笔记文件")
        
        # 显示分类统计
        if markdown_files:
            categories = set(f['category'] for f in markdown_files)
            print(f"📁 发现分类: {', '.join(sorted(categories))}")
    
    return success_count > 0

if __name__ == '__main__':
    update_readme() 