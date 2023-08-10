@echo off
setlocal

python -m venv  %~dp0\env
%~dp0\env\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple some-package