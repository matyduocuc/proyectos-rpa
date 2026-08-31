import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Ocultar advertencia de conexión DBAPI2 en pandas
warnings.filterwarnings('ignore', category=UserWarning)

# Configuración de conexión a la BD
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'rpa_db'
}

def obtener_datos_logs():
    try:
        conn = mysql.connector.connect(**db_config)
        query = "SELECT id, estado, tipo_error, fecha_registro FROM logs_accesos ORDER BY id ASC"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except mysql.connector.Error as err:
        print(f"❌ Error de conexión: {err}")
        return None

def generar_reporte_visual():
    df = obtener_datos_logs()
    
    if df is None or df.empty:
        print("⚠️ No hay suficientes datos cargados en 'logs_accesos'.")
        return

    # 1. CÁLCULO DE COLUMNAS (Siempre sobre el DataFrame 'df' completo primero)
    total_intentos = len(df)
    exitos = len(df[df['estado'] == 'Exitoso'])
    errores = total_intentos - exitos
    tasa_exito = (exitos / total_intentos) * 100 if total_intentos > 0 else 0

    df['num_intento'] = range(1, len(df) + 1)
    df['es_error'] = df['estado'].apply(lambda x: 1 if x != 'Exitoso' else 0)
    df['errores_acumulados'] = df['es_error'].cumsum()

    # 2. FILTRAR DESPUÉS DE CREAR LAS COLUMNAS
    df_exitos = df[df['estado'] == 'Exitoso']
    df_fallos = df[df['estado'] != 'Exitoso']

    # 3. FIGURA Y GRÁFICOS
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Panel de Control: Rendimiento de Accesos y Auditoría', fontsize=15, fontweight='bold')

    # Gráfico de Dona: Tasa Global de Éxito
    etiquetas = ['Éxito', 'Error']
    valores = [exitos, errores]
    colores = ['#2ecc71', '#e74c3c']

    ax1.pie(valores, labels=etiquetas, autopct='%1.1f%%', startangle=90, 
            colors=colores, wedgeprops=dict(width=0.4, edgecolor='white'))
    ax1.set_title(f'Tasa de Éxito Global ({tasa_exito:.1f}%)', fontsize=12)

    # Gráfico de Línea de Tiempo / Secuencia de Errores
    ax2.plot(df['num_intento'], df['errores_acumulados'], color='#e74c3c', linestyle='--', label='Errores Acumulados', zorder=1)
    
    # Puntos verdes para accesos exitosos
    ax2.scatter(df_exitos['num_intento'], df_exitos['errores_acumulados'], color='#2ecc71', s=80, label='Acceso Correcto', zorder=2)

    # Puntos rojos y anotaciones para cada tipo de error
    for idx, row in df_fallos.iterrows():
        etiqueta_error = row['tipo_error'] if pd.notnull(row['tipo_error']) else 'Fallo'
        ax2.scatter(row['num_intento'], row['errores_acumulados'], color='#c0392b', s=100, zorder=3)
        ax2.annotate(f"{etiqueta_error}", 
                     (row['num_intento'], row['errores_acumulados']),
                     textcoords="offset points", xytext=(0, 10), ha='center',
                     fontsize=8, fontweight='bold', color='#7f8c8d')

    ax2.set_title('Evolución de Fallos por Secuencia de Intentos', fontsize=12)
    ax2.set_xlabel('Número de Intento (Secuencia de Ejecución)', fontsize=10)
    ax2.set_ylabel('Cantidad de Errores Acumulados', fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='upper left')

    ax2.xaxis.get_major_locator().set_params(integer=True)
    ax2.yaxis.get_major_locator().set_params(integer=True)

    plt.tight_layout()
    plt.savefig('reporte_rendimiento.png', dpi=300)
    plt.show()

if __name__ == "__main__":
    generar_reporte_visual()