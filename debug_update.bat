@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ==========================================
echo      🔧 笔记系统调试工具
echo ==========================================
echo.

echo 🔍 系统环境检查...
echo 💻 当前工作目录: %CD%
echo 📅 当前时间: %date% %time%
echo 🖥️  计算机名: %COMPUTERNAME%
echo 👤 用户名: %USERNAME%
echo.

echo 📁 文件结构检查...
if exist "update_readme.py" (
    echo ✅ update_readme.py 存在
) else (
    echo ❌ update_readme.py 不存在
)

if exist "mkdocs.yml" (
    echo ✅ mkdocs.yml 存在
) else (
    echo ❌ mkdocs.yml 不存在
)

if exist "docs" (
    echo ✅ docs 目录存在
    if exist "docs\index.md" (
        echo ✅ docs\index.md 存在
    ) else (
        echo ❌ docs\index.md 不存在
    )
    if exist "docs\notes" (
        echo ✅ docs\notes 目录存在
        for /f %%i in ('dir /s /b "docs\notes\*.md" 2^>nul ^| find /c /v ""') do set MD_COUNT=%%i
        echo 📄 找到 !MD_COUNT! 个markdown文件
    ) else (
        echo ❌ docs\notes 目录不存在
    )
) else (
    echo ❌ docs 目录不存在
)
echo.

echo 🐍 Python环境检查...
where python >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ 系统PATH中找到Python
    python --version
    echo.
    echo 📦 检查Python包...
    python -c "import yaml; print('✅ pyyaml已安装')" 2>nul || echo "❌ pyyaml未安装"
    python -c "import pathlib; print('✅ pathlib可用')" 2>nul || echo "❌ pathlib不可用"
    python -c "import os; print('✅ os模块可用')" 2>nul || echo "❌ os模块不可用"
    python -c "import re; print('✅ re模块可用')" 2>nul || echo "❌ re模块不可用"
    python -c "import datetime; print('✅ datetime模块可用')" 2>nul || echo "❌ datetime模块不可用"
    python -c "import collections; print('✅ collections模块可用')" 2>nul || echo "❌ collections模块不可用"
) else (
    echo ❌ 系统PATH中未找到Python
    echo 🔍 查找常见Python安装路径...
    
    set FOUND_PYTHON=0
    for %%p in (C:\Python312 C:\Python311 C:\Python310 C:\Python39 C:\Python_396) do (
        if exist "%%p\python.exe" (
            echo ✅ 找到Python: %%p\python.exe
            "%%p\python.exe" --version
            set FOUND_PYTHON=1
        )
    )
    
    if !FOUND_PYTHON! equ 0 (
        echo ❌ 未找到任何Python安装
    )
)
echo.

echo 🧪 测试Python脚本...
if exist "update_readme.py" (
    echo 🔍 检查Python脚本语法...
    python -m py_compile update_readme.py 2>nul
    if !errorlevel! equ 0 (
        echo ✅ Python脚本语法正确
        echo.
        echo 🚀 尝试运行Python脚本（详细输出）...
        echo ==========================================
        python update_readme.py
        set SCRIPT_EXIT_CODE=!errorlevel!
        echo ==========================================
        echo 📋 脚本执行完成，退出代码: !SCRIPT_EXIT_CODE!
    ) else (
        echo ❌ Python脚本语法错误
    )
) else (
    echo ❌ update_readme.py 文件不存在，无法测试
)
echo.

echo 🔧 Git状态检查...
git --version >nul 2>&1
if !errorlevel! equ 0 (
    echo ✅ Git已安装
    git status --porcelain > temp_status.txt 2>nul
    if exist temp_status.txt (
        set /p git_changes=<temp_status.txt
        del temp_status.txt
        if "!git_changes!"=="" (
            echo ℹ️  Git状态：无更改
        ) else (
            echo 📋 Git状态：有未提交的更改
        )
    ) else (
        echo ⚠️  无法获取Git状态（可能不是Git仓库）
    )
) else (
    echo ❌ Git未安装或不在PATH中
)
echo.

echo ==========================================
echo          🎯 诊断完成
echo ==========================================
echo.
echo 💡 如果发现问题，请根据上述检查结果进行修复
echo.
pause 