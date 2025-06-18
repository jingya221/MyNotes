#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动更新README.md中的笔记索引
扫描notes文件夹中的所有markdown文件，并更新README.md中的目录
"""

import os
import re
from datetime import datetime
from pathlib import Path

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

def get_file_info(file_path):
    """获取文件信息"""
    stat = os.stat(file_path)
    modified_time = datetime.fromtimestamp(stat.st_mtime)
    return {
        'path': file_path,
        'title': extract_title_from_markdown(file_path),
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

def generate_index_content(markdown_files):
    """生成目录索引内容"""
    if not markdown_files:
        return "*目前还没有笔记，快去创建第一个笔记吧！*\n"
    
    content = []
    content.append(f"*共找到 {len(markdown_files)} 个笔记文件*\n")
    
    # 按修改时间分组
    today = datetime.now().date()
    recent_files = []
    older_files = []
    
    for file_info in markdown_files:
        if (today - file_info['modified'].date()).days <= 7:
            recent_files.append(file_info)
        else:
            older_files.append(file_info)
    
    # 最近的笔记
    if recent_files:
        content.append("### 🔥 最近更新\n")
        for file_info in recent_files:
            relative_path = str(file_info['path']).replace('\\', '/')
            modified_str = file_info['modified'].strftime('%Y-%m-%d')
            content.append(f"- [{file_info['title']}]({relative_path}) *({modified_str})*")
        content.append("")
    
    # 所有笔记
    content.append("### 📋 所有笔记\n")
    
    # 按字母顺序分组
    files_by_letter = {}
    for file_info in markdown_files:
        first_char = file_info['title'][0].upper()
        if first_char.isalpha():
            if first_char not in files_by_letter:
                files_by_letter[first_char] = []
            files_by_letter[first_char].append(file_info)
        else:
            if '#' not in files_by_letter:
                files_by_letter['#'] = []
            files_by_letter['#'].append(file_info)
    
    for letter in sorted(files_by_letter.keys()):
        if letter == '#':
            content.append("#### 其他")
        else:
            content.append(f"#### {letter}")
        
        for file_info in sorted(files_by_letter[letter], key=lambda x: x['title']):
            relative_path = str(file_info['path']).replace('\\', '/')
            modified_str = file_info['modified'].strftime('%Y-%m-%d')
            content.append(f"- [{file_info['title']}]({relative_path}) *({modified_str})*")
        content.append("")
    
    return '\n'.join(content)

def update_readme():
    """更新README.md文件"""
    readme_path = Path('./README.md')
    if not readme_path.exists():
        print("README.md文件不存在！")
        return False
    
    # 读取当前README内容
    with open(readme_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # 扫描笔记文件
    markdown_files = scan_notes_folder()
    
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
        print("未找到索引标记，请检查README.md格式！")
        return False
    
    # 更新最后更新时间
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    new_content = re.sub(
        r'\*最后更新:.*?\*',
        f'*最后更新: {current_time}*',
        new_content
    )
    
    # 写入文件
    with open(readme_path, 'w', encoding='utf-8') as file:
        file.write(new_content)
    
    print(f"✅ README.md 已更新！找到 {len(markdown_files)} 个笔记文件")
    return True

if __name__ == '__main__':
    update_readme() 