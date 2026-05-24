@echo off
echo Lancement du Cerveau IA...
start cmd /k "python FINAL_ACCOUNTING_OS/backend/core/main.py"
echo Lancement du Pont PC...
start cmd /k "python FINAL_ACCOUNTING_OS/backend/bridge/client_bridge.py"
echo Lancement de l'Interface...
start chrome "file:///%cd%/FINAL_ACCOUNTING_OS/index.html"
echo.
echo SYSTEME PRET !
pause
