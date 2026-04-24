@echo off
chcp 65001 >nul
echo ========================================
echo   全自动折扣资讯聚合器 - 启动脚本
echo ========================================
echo.

cd /d "%~dp0"

echo [1/2] 激活虚拟环境...
call venv\Scripts\activate.bat

echo [2/2] 启动爬虫服务（后台运行）...
echo 按 Ctrl+C 可停止服务
echo.

python scraper.py

pause
