@echo off
chcp 65001 >nul
echo ==========================================
echo      📝 Markdown笔记系统更新工具
echo ==========================================
echo.

echo 🔄 正在更新笔记索引...
python update_readme.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 更新失败，请检查错误信息
    pause
    exit /b 1
)

echo.
echo ✅ README.md 更新完成！
echo.

REM 检查是否有未提交的更改
git status --porcelain > temp_status.txt 2>nul
if exist temp_status.txt (
    set /p git_changes=<temp_status.txt
    del temp_status.txt
) else (
    set git_changes=
)

if "%git_changes%"=="" (
    echo ℹ️  没有检测到文件更改，无需提交。
    echo.
    pause
    exit /b 0
)

echo 📋 检测到以下文件有更改：
git status --short
echo.

REM 询问是否提交到Git
set /p commit_choice="🤔 是否要提交这些更改到Git？[Y/n]: "
if /i "%commit_choice%"=="n" (
    echo.
    echo ⏩ 跳过Git提交
    pause
    exit /b 0
)

echo.
echo 📦 添加文件到暂存区...
git add .

REM 询问提交信息
set /p commit_msg="💬 请输入提交信息（直接回车使用默认信息）: "
if "%commit_msg%"=="" (
    set commit_msg=更新笔记索引 - %date% %time:~0,8%
)

echo.
echo 💾 提交更改...
git commit -m "%commit_msg%"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Git提交失败
    pause
    exit /b 1
)

echo.
echo ✅ Git提交成功！
echo.

REM 询问是否推送到远程仓库
set /p push_choice="🚀 是否要推送到GitHub？[Y/n]: "
if /i "%push_choice%"=="n" (
    echo.
    echo ⏩ 跳过推送到远程仓库
    echo 💡 您可以稍后手动运行: git push
    pause
    exit /b 0
)

echo.
echo 🌐 正在推送到GitHub...
git push

if %errorlevel% equ 0 (
    echo.
    echo 🎉 推送成功！
    echo.
    echo 📱 您的更改将在几分钟内反映到GitHub Pages:
    echo    https://jingya221.github.io/MyNotes/
    echo.
    echo 💡 如果网页没有立即更新，请：
    echo    1. 等待2-5分钟让GitHub Pages构建
    echo    2. 刷新浏览器缓存 (Ctrl+F5)
    echo    3. 检查GitHub Actions状态
) else (
    echo.
    echo ❌ 推送失败，请检查：
    echo    1. 网络连接是否正常
    echo    2. GitHub认证是否有效
    echo    3. 是否有权限推送到仓库
    echo.
    echo 🔧 您可以手动推送: git push
)

echo.
echo ==========================================
echo           操作完成！
echo ==========================================
pause 