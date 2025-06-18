# GitHub Pages 设置指南

## 问题诊断

从构建失败的情况看，很可能是GitHub Pages的源设置不正确。

## 解决步骤

### 1. 进入仓库设置
1. 打开你的GitHub仓库: https://github.com/jingya221/MyNotes
2. 点击仓库顶部的 **Settings** 选项卡
3. 在左侧菜单中找到 **Pages** 选项

### 2. 配置GitHub Pages源
在Pages设置页面中：

**重要：选择正确的源**
- **Source**: 选择 `GitHub Actions` 
- **不要**选择 `Deploy from a branch`

### 3. 确保Actions权限正确
1. 在Settings页面，点击左侧的 **Actions** → **General**
2. 在 "Workflow permissions" 部分：
   - 选择 `Read and write permissions`
   - 勾选 `Allow GitHub Actions to create and approve pull requests`

### 4. 手动触发构建
1. 去到 **Actions** 选项卡
2. 点击 **Deploy MkDocs** workflow
3. 点击 **Run workflow** 按钮
4. 确认运行

## 常见问题解决

### 如果仍然失败：

#### 问题1：权限不足
- 确保你是仓库的管理员
- 检查Actions是否被启用

#### 问题2：文件缺失
确保以下文件存在：
- `mkdocs.yml`
- `.github/workflows/docs.yml`
- `docs/index.md`

#### 问题3：依赖问题
检查workflow中的Python依赖是否正确安装。

## 验证成功

构建成功后，你的网站将在以下地址可用：
- https://jingya221.github.io/MyNotes/

## 备选方案：Wiki站点

**只有在上述方法完全无效时才考虑**

如果GitHub Pages确实无法工作，可以考虑：
1. 使用GitHub Wiki功能
2. 部署到Netlify或Vercel
3. 使用Gitee Pages（国内访问更快）

但建议先尝试修复当前的GitHub Pages设置，因为MkDocs Material主题提供了最佳的用户体验。 