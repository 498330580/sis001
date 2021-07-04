@echo off
@echo Django启动程序
@cd  %~dp0
@start /min "Django" .\venv\Scripts\python.exe .\manage.py runserver 0.0.0.0:8000


@start /min "获取sis小说" .\venv\Scripts\python.exe .\tools\get_script\get_xiaosuo.py