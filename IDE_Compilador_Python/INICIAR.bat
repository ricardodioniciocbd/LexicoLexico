@echo off
REM IDE Compilador Interactivo de Python
REM Script para iniciar el IDE

echo.
echo ====================================================
echo   IDE COMPILADOR INTERACTIVO DE PYTHON
echo ====================================================
echo.

python python_ide_complete.py

if errorlevel 1 (
    echo.
    echo ERROR: No se pudo iniciar el IDE
    echo Verifica que Python 3.10+ esté instalado
    echo y que todos los archivos están en la misma carpeta
    echo.
    pause
)
