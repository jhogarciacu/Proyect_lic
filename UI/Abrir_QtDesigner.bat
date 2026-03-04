@echo off
REM Activar entorno virtual
call C:\Proyects\Proyect_lic\venv_ui\Scripts\activate

REM Ir a la carpeta del proyecto UI
cd /d C:\Proyects\Proyect_lic\UI

REM Abrir Qt Designer con el archivo .ui
pyside6-designer Qt_designer.ui