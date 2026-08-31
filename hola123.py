import os
import csv
import time
import getpass
from datetime import datetime
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By

URL_LOGIN = "https://fundacion-instituto-profesional-duoc-uc.github.io/ATY1102-MantenedorUsuarios/index.html"
ARCHIVO_CSV = "trazabilidad_rpa.csv"

# Usuarios a ingresar en el mantenedor
USUARIOS_A_REGISTRAR = [
    {"nombre": "Matias Gaete", "email": "matias@duocuc.cl", "ciudad": "Santiago"},
    {"nombre": "Ana Lopez", "email": "ana.lopez@duocuc.cl", "ciudad": "Concepcion"},
    {"nombre": "Carlos Perez", "email": "carlos.perez@duocuc.cl", "ciudad": "Valparaiso"}
]

def guardar_trazabilidad_csv(fec_inicio, fec_fin, intento, status, mensaje, pc_name, usuario):
    """Guarda el historial acumulativo en un archivo CSV"""
    tiempo_total = str(fec_fin - fec_inicio)
    existe_archivo = os.path.exists(ARCHIVO_CSV)

    try:
        with open(ARCHIVO_CSV, mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo, delimiter=';')
            
            # Si el archivo es nuevo, escribe la cabecera
            if not existe_archivo:
                escritor.writerow(["ID_EJECUCION", "FEC_INICIO", "FEC_FIN", "TIEMPO_TOTAL", "INTENTO", "STATUS", "MENSAJE", "PC", "USUARIO_SISTEMA"])
            
            # Genera un ID basado en la fecha/hora
            id_ejecucion = fec_inicio.strftime('%Y%m%d%H%M%S')
            
            escritor.writerow([
                id_ejecucion,
                fec_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                fec_fin.strftime('%Y-%m-%d %H:%M:%S'),
                tiempo_total,
                intento,
                status,
                mensaje,
                pc_name,
                usuario
            ])
        print(f" [CSV] Historial actualizado en {ARCHIVO_CSV}")
    except Exception as err:
        print(f" [CSV ERROR] No se pudo escribir en el CSV: {err}")

def guardar_trazabilidad_mysql(fec_inicio, fec_fin, status, mensaje, pc_name, usuario):
    """Inserción directa en MySQL (XAMPP) en la tabla trazabilidad_rpa"""
    tiempo_total = str(fec_fin - fec_inicio)

    try:
        conexion = mysql.connector.connect(
            host="127.0.0.1",  # <- Reemplaza "localhost" por la IP o ID exacto aquí
            user="root",
            password="",
            database="rpa_db"
        )
        cursor = conexion.cursor()

        sql = """INSERT INTO trazabilidad_rpa
                (fec_inicio, fec_fin, tiempo, status, mensaje, pc, cuenta_usuario)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        valores = (
            fec_inicio, fec_fin, tiempo_total, status, mensaje, pc_name, usuario
        )
        cursor.execute(sql, valores)
        conexion.commit()
        
    except Exception as err:
        print(f" [CSV ERROR] No se pudo escribir en el CSV: {err}")

def ejecutar_flujo_rpa(intento_num):
    fec_inicio = datetime.now()
    pc_name = os.environ.get('COMPUTERNAME', 'LOCAL_PC')
    usuario_so = getpass.getuser()
    driver = webdriver.Firefox()
    
    try:
        # 1. INICIAR SESIÓN
        driver.get(URL_LOGIN)
        time.sleep(1)

        input_user = driver.find_element(By.ID, "username")
        input_pass = driver.find_element(By.ID, "password")
        form_login = driver.find_element(By.ID, "loginForm")

        input_user.clear()
        input_user.send_keys("duoc")
        
        input_pass.clear()
        input_pass.send_keys("duoc123")
        
        form_login.submit()
        time.sleep(2)

        # Validar redirección
        if "mantenedor.html" not in driver.current_url:
            raise Exception("No se logro redirigir a mantenedor.html (Login fallido)")

        # 2. REGISTRAR 3 USUARIOS EN EL MANTENEDOR
        input_nombre = driver.find_element(By.ID, "nombre")
        input_email = driver.find_element(By.ID, "email")
        input_ciudad = driver.find_element(By.ID, "ciudad")
        form_datos = driver.find_element(By.ID, "dataForm")

        for persona in USUARIOS_A_REGISTRAR:
            input_nombre.clear()
            input_nombre.send_keys(persona["nombre"])
            
            input_email.clear()
            input_email.send_keys(persona["email"])
            
            input_ciudad.clear()
            input_ciudad.send_keys(persona["ciudad"])
            
            form_datos.submit()
            time.sleep(1)

        driver.save_screenshot("captura_evidencia.png")
        fec_fin = datetime.now()
        
        mensaje_exito = f"Intento #{intento_num}: Login y 3 usuarios registrados con exito."
        
        # Guardar en ambos destinos
        guardar_trazabilidad_mysql(fec_inicio, fec_fin, "OK", mensaje_exito, pc_name, usuario_so)
        guardar_trazabilidad_csv(fec_inicio, fec_fin, intento_num, "OK", mensaje_exito, pc_name, usuario_so)
        return True

    except Exception as e:
        fec_fin = datetime.now()
        mensaje_error = f"Intento #{intento_num} Fallo: {str(e)[:150]}"
        print(f" [ERROR] {mensaje_error}")
        
        # Guardar en ambos destinos
        guardar_trazabilidad_mysql(fec_inicio, fec_fin, "ERROR", mensaje_error, pc_name, usuario_so)
        guardar_trazabilidad_csv(fec_inicio, fec_fin, intento_num, "ERROR", mensaje_error, pc_name, usuario_so)
        return False

    finally:
        driver.quit()

# --- CONTROL DE REINTENTOS ---
if __name__ == "__main__":
    max_reintentos = 3
    proceso_exitoso = False

    print("=== INICIANDO PROCESO RPA CON REINTENTOS, MYSQL Y CSV ===")

    for intento in range(1, max_reintentos + 1):
        print(f"\n--- Ejecutando Intento {intento} de {max_reintentos} ---")
        proceso_exitoso = ejecutar_flujo_rpa(intento)
        
        if proceso_exitoso:
            print(f"\n ¡Proceso completado exitosamente en el intento #{intento}!")
            break
        else:
            print(f"\n Intento #{intento} fallo. Reintentando...")
            time.sleep(2)

    if not proceso_exitoso:
        print("\n [ALERTA] Se agotaron los 3 reintentos sin exito.")