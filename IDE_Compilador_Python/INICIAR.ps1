# IDE Compilador Interactivo de Python
# Script para iniciar el IDE en PowerShell

Write-Host ""
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "  IDE COMPILADOR INTERACTIVO DE PYTHON" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Iniciando IDE..." -ForegroundColor Green
python python_ide_complete.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: No se pudo iniciar el IDE" -ForegroundColor Red
    Write-Host "Verifica que Python 3.10+ esté instalado" -ForegroundColor Yellow
    Write-Host "y que todos los archivos están en la misma carpeta" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Presiona Enter para salir"
}
