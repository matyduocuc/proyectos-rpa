import mysql.connector
import bcrypt

# Configura tus datos de conexión a MariaDB/MySQL
db_config = {
    'host': 'localhost',  # O la IP de tu servidor MySQL
    'user': 'root',
    'password': '',
    'database': 'rpa_db'  # Asegúrate de colocar el nombre de tu base de datos
}

# Generar hash seguro para la clave inicial "admin123"
password_plana = "admin123"
salt = bcrypt.gensalt()
hashed_password = bcrypt.hashpw(password_plana.encode('utf-8'), salt).decode('utf-8')

try:
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Insertar o actualizar el usuario admin con su clave encriptada
    query = """
        INSERT INTO usuarios (username, password_hash, rol) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE password_hash = VALUES(password_hash)
    """
    cursor.execute(query, ('admin', hashed_password, 'admin'))
    conn.commit()

    print(" Usuario 'admin' (clave: admin123) configurado y encriptado exitosamente.")

except mysql.connector.Error as err:
    print(f" Error al conectar o insertar en la base de datos: {err}")

finally:
    if 'conn' in locals() and conn.is_connected():
        cursor.close()
        conn.close()