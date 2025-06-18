@echo off
chcp 65001 >nul
echo 正在更新笔记索引...
echo.

python update_readme.py

if %errorlevel% equ 0 (
    echo.
    echo ✅ 更新完成！
    echo.
    echo 现在您可以：
    echo 1. 查看更新后的 README.md
    echo 2. 使用 git add . 和 git commit 提交更改
    echo 3. 使用 git push 推送到 GitHub
) else (
    echo.
    echo ❌ 更新失败，请检查错误信息
)

echo.
pause 