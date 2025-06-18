@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
echo ==========================================
echo      📝 笔记索引更新工具（仅更新索引）
echo ==========================================
echo.

echo 🔄 正在更新笔记索引...
echo 💻 当前工作目录: %CD%
echo.

REM 检查必要文件是否存在
if not exist "update_readme.py" (
    echo ❌ 错误：未找到 update_readme.py 文件
    echo 💡 请确保在正确的目录下运行此脚本
    echo.
    pause
    exit /b 1
)

if not exist "docs" (
    echo ❌ 错误：未找到 docs 目录
    echo 💡 请确保在项目根目录下运行此脚本
    echo.
    pause
    exit /b 1
)

REM 尝试查找Python
set PYTHON_CMD=
echo 🔍 正在查找Python...

where python >nul 2>&1
if !errorlevel! equ 0 (
    set PYTHON_CMD=python
    echo ✅ 在系统PATH中找到Python
) else (
    echo ⚠️  系统PATH中未找到Python，尝试常见安装路径...
    
    if exist "C:\Python312\python.exe" (
        set PYTHON_CMD=C:\Python312\python.exe
        echo ✅ 找到Python: C:\Python312\python.exe
    ) else if exist "C:\Python311\python.exe" (
        set PYTHON_CMD=C:\Python311\python.exe
        echo ✅ 找到Python: C:\Python311\python.exe
    ) else if exist "C:\Python310\python.exe" (
        set PYTHON_CMD=C:\Python310\python.exe
        echo ✅ 找到Python: C:\Python310\python.exe
    ) else if exist "C:\Python39\python.exe" (
        set PYTHON_CMD=C:\Python39\python.exe
        echo ✅ 找到Python: C:\Python39\python.exe
    ) else if exist "C:\Python_396\python.exe" (
        set PYTHON_CMD=C:\Python_396\python.exe
        echo ✅ 找到Python: C:\Python_396\python.exe
    ) else (
        echo ❌ 未找到Python安装
        echo 💡 请确保Python已安装并在系统PATH中
        pause
        exit /b 1
    )
)

echo 📍 使用Python: %PYTHON_CMD%
echo.

REM 检查Python是否能正常运行
echo 🧪 测试Python环境...
%PYTHON_CMD% --version
if %errorlevel% neq 0 (
    echo ❌ Python无法正常运行
    pause
    exit /b 1
)

echo.
echo 🚀 开始执行Python脚本...
echo.

REM 执行Python脚本
%PYTHON_CMD% update_readme.py
set PYTHON_EXIT_CODE=%errorlevel%

echo.
echo 📋 Python脚本执行完成，退出代码: %PYTHON_EXIT_CODE%

if %PYTHON_EXIT_CODE% neq 0 (
    echo.
    echo ❌ 更新失败，Python脚本执行出错（退出代码: %PYTHON_EXIT_CODE%）
    echo.
    echo 🔧 可能的解决方案：
    echo    1. 检查Python依赖是否已安装（如 pyyaml）
    echo    2. 检查文件路径和权限
    echo    3. 检查markdown文件格式是否正确
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 笔记索引更新完成！
echo.
echo 💡 如需提交到Git，请：
echo    1. 运行 update_notes.bat 进行完整操作
echo    2. 或手动执行 git add . && git commit && git push
echo.

echo ==========================================
echo           ✅ 操作完成！
echo ==========================================
pause 