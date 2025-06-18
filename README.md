# 📚 个人笔记系统

> 🌐 **在线浏览**: [https://jingya221.github.io/MyNotes/](https://jingya221.github.io/MyNotes/)

欢迎来到我的个人笔记管理系统！这里收录了各种学习笔记和技术文档。

## 📋 笔记目录

### R shiny开发教程
- [00-使用{Golem}搭建Rshiny project指南 <!-- omit in toc -->](docs/notes/R shiny开发教程/00-使用{Golem}搭建Rshiny project指南) - >作者：王靖雅 <br>
- [01-数据读入&数据处理模块开发指南 <!-- omit in toc -->](docs/notes/R shiny开发教程/01-数据读入&数据处理模块开发指南) - >作者：王靖雅 <br>
- [02-分析图表相关模块开发指南 <!-- omit in toc -->](docs/notes/R shiny开发教程/02-分析图表相关模块开发指南) - >作者：王靖雅 <br>
- [03-基于MediSum模块开发项目的ShinyApp整合指南 <!-- omit in toc -->](docs/notes/R shiny开发教程/03-基于MediSum模块开发项目的ShinyApp整合指南) - >作者：王靖雅 <br>

### R shiny部署教程
- [R Shiny Server Deployment in Hengrui Server](docs/notes/R shiny部署教程/0-R Shiny Server Deployment in Hengrui Server) - shnvlshiny01	10.10.5.114	 root/Hr@shiny0821

### R语言相关
- [XPT文件导出与读取](docs/notes/R语言相关/xpt-export-import) - 这个笔记来源于R taskforce出现的导出xpt无法打开的问题。
## 🔧 使用指南

- [基础使用指南](docs/guide/usage.md) - 了解如何使用这个笔记系统
- [添加新笔记](docs/guide/add-notes.md) - 学习如何创建和组织新的笔记文件  
- [更新索引](docs/guide/update-index.md) - 如何自动更新和维护笔记索引

## 📊 统计信息

- **笔记分类**: 3个
- **总笔记数**: 6篇
- **最近更新**: XPT文件导出与读取

---

> 💡 **提示**: 点击左侧导航栏可以快速浏览所有笔记分类，使用顶部搜索功能可以快速查找内容。

---

## 🚀 如何使用

1. **在线浏览**: 访问 [GitHub Pages](https://jingya221.github.io/MyNotes/) 获得最佳阅读体验
2. **本地运行**: 
   ```bash
   pip install mkdocs mkdocs-material
   mkdocs serve
   ```
3. **添加笔记**: 在 `docs/notes/` 文件夹中创建新的markdown文件
4. **自动更新**: 运行 `python update_readme.py` 或 `update_notes.bat` 自动更新索引

## 📁 项目结构

```
NotesGit/
├── docs/                    # MkDocs文档目录
│   ├── index.md            # 首页
│   ├── notes/              # 笔记文件夹
│   └── guide/              # 使用指南
├── mkdocs.yml              # MkDocs配置文件
├── update_readme.py        # 自动更新脚本
├── update_notes.bat        # Windows批处理文件
└── README.md               # 项目说明（本文件）
```

---

*📅 最后更新: 2025-06-18 17:15:39*
