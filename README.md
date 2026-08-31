1. Configuración del Entorno y Sistema

Comandos de consola para verificar herramientas y configurar el sistema Windows:

Abrir Variables de Entorno del Sistema:

PowerShell
sysdm.cpl
(Abre la ventana desplegable para agregar rutas al PATH sin navegar por la configuración de Windows).

Verificar versión de GeckoDriver (Firefox):

PowerShell
geckodriver --version
Agregar ruta al PATH desde la terminal (PowerShell):

PowerShell
[System.Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Ruta\Geckodriver", "User")
2. Instalación de Librerías (Por Separado)

Comandos individuales para la instalación de cada paquete según su función en el bot:

Librería de Automatización Web (Selenium):

PowerShell
python -m pip install selenium
Librería de Procesamiento de Datos (Pandas):

PowerShell
python -m pip install pandas
(Se usa para la manipulación estructurada de tablas, exportación/lectura de CSVs y reporte de auditoría).

Librería del Conector de Base de Datos (MySQL):

PowerShell
python -m pip install mysql-connector-python
(Permite la conexión directa desde Python hacia XAMPP / MariaDB).

3. Control de Dependencias del Proyecto

Comandos para registrar y desplegar librerías entre laptops o entornos:

Exportar las librerías instaladas a un archivo:

PowerShell
python -m pip freeze > requirements.txt
Instalar todas las librerías registradas en una laptop nueva:

PowerShell
python -m pip install -r requirements.txt
4. Ejecución de Scripts Python

Ejecutar el bot principal (Trazabilidad en tiempo real):

PowerShell
python hola123.py
Ejecutar el script de migración (Cargar CSV a XAMPP):

PowerShell
python migrar.py
Ejecutar si la palabra python no está en el PATH:

PowerShell
py hola123.py

Comando de atajo para abrir directamente la ventana del sistema donde están las Variables de entorno en Windows.



https://github.com/mozilla/geckodriver/releases
