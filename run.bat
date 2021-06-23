@echo off
@echo sis001辅助程序
@cd  %~dp0
@echo 启动API
@start /min "API" .\api\api_run.bat
@echo 启动获取脚本
@start /min "API" .\get_xiaosuo_save\get_run.bat