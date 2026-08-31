import mysql.connector

def crear_base_y_tabla():
    try:
        # Conexión inicial a MySQL en XAMPP
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        cursor = conexion.cursor()

        # Crear Base de Datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS rpa_db")
        cursor.execute("USE rpa_db")

        # Crear Tabla de Trazabilidad
        sql_tabla = """
        CREATE TABLE IF NOT EXISTS trazabilidad_rpa (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fec_inicio DATETIME NOT NULL,
            fec_fin DATETIME NOT NULL,
            tiempo VARCHAR(50) NOT NULL,
            status VARCHAR(20) NOT NULL,
            mensaje VARCHAR(255) NOT NULL,
            pc VARCHAR(100) NOT NULL,
            cuenta_usuario VARCHAR(100) NOT NULL
        )
        """
        cursor.execute(sql_tabla)
        conexion.commit()
        cursor.close()
        conexion.close()
        print(" [BD] Base de datos 'rpa_db' y tabla 'trazabilidad_rpa' listas.")
    except Exception as e:
        print(f" [BD ERROR] Error al crear la estructura en MySQL: {e}")

if __name__ == "__main__":
    crear_base_y_tabla()