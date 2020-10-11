@echo off

# このバッチファイルが格納されているディレクトリをカレントディレクトリとする.
pushd %~dp0 

setlocal

# pythonファイルの実行.
python perse_git_log.py

endlocal