@echo off
@echo sis001��������
@cd  %~dp0
@echo ����API
@start /min "API" .\api\api_run.bat
@echo ������ȡ�ű�
@start /min "API" .\get_xiaosuo_save\get_run.bat