import mysql.connector
import bcrypt

# Configuración de conexión a la base de datos
db_config = {
    'host': 'localhost',      # Cambia por la IP del servidor (ej. 10.220.2.99) en producción
    'user': 'root',
    'password': '',
    'database': 'rpa_db'
}

def registrar_log(cursor, conn, usuario_id, username, estado, tipo_error=None):
    """Guarda cada intento en la tabla logs_accesos para alimentar los gráficos."""
    query = """
        INSERT INTO logs_accesos (usuario_id, username_intentado, estado, tipo_error)
        VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (usuario_id, username, estado, tipo_error))
    conn.commit()

def iniciar_sesion(username, password_ingresada):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # 1. Buscar usuario en la base de datos
        query_usuario = "SELECT id, username, password_hash, rol FROM usuarios WHERE username = %s"
        cursor.execute(query_usuario, (username,))
        usuario = cursor.fetchone()

        # Error 1: El usuario no existe
        if not usuario:
            print(" Acceso denegado: Usuario no encontrado.")
            registrar_log(cursor, conn, None, username, 'Error_Password', 'Usuario no registrado')
            return False

        # 2. Verificar contraseña hash
        password_bytes = password_ingresada.encode('utf-8')
        hash_almacenado = usuario['password_hash'].encode('utf-8')

        if bcrypt.checkpw(password_bytes, hash_almacenado):
            # Éxito
            print(f" ¡Bienvenido {usuario['username']}! Rol: [{usuario['rol'].upper()}]")
            registrar_log(cursor, conn, usuario['id'], username, 'Exitoso', None)
            return True
        else:
            # Error 2: Contraseña incorrecta
            print(" Acceso denegado: Contraseña incorrecta.")
            registrar_log(cursor, conn, usuario['id'], username, 'Error_Password', 'Clave errónea')
            return False

    except mysql.connector.Error as err:
        # Error 3: Fallo de conexión/infraestructura
        print(f" Error de base de datos: {err}")
        return False
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# --- SCRIPT DE PRUEBA ---
if __name__ == "__main__":
    print("--- INICIO DE SESIÓN ---")
    usr = input("Usuario: ")
    pwd = input("Contraseña: ")
    iniciar_sesion(usr, pwd)