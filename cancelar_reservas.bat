@echo off
cd /d "C:\Projetos\Biblioteca Antares\BibliotecaAntares"

"C:\Users\TI Antares\AppData\Local\Python\pythoncore-3.14-64\python.exe" manage.py cancelar_reservas_expiradas >> cancelar_reservas.log 2>&1
