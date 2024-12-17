import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Directorios de entrada y salida
input_folder = r"Benchmarks\Results_Benchmarks_PICKs\DBs" 
output_folder = r"Benchmarks\Results_Benchmarks_PICKs\plots" 

# Asegurarse de que el directorio de salida existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para procesar un archivo .db y guardar el gráfico
def process_db_file(db_path, output_folder):
    try:
        conn = sqlite3.connect(db_path)
        
        # Obtener plannerid y nombres de planners
        planner_query = "SELECT id, name FROM plannerConfigs"
        runs_query = "SELECT plannerid, time FROM runs"
        
        planners_df = pd.read_sql_query(planner_query, conn)
        runs_df = pd.read_sql_query(runs_query, conn)
        
        # Combinar datos
        merged_df = runs_df.merge(planners_df, left_on="plannerid", right_on="id")
        merged_df = merged_df[['name', 'time']].rename(columns={"name": "planner"})
        
        conn.close()
        
        # Ajustar tamaño dinámicamente según el número de planners
        num_planners = merged_df['planner'].nunique()
        fig_width = max(15, num_planners * 2)  # Ajuste dinámico del ancho
        
        # Crear y guardar el box plot
        plt.figure(figsize=(fig_width, 8))  # Ancho dinámico, altura fija
        boxplot = merged_df.boxplot(column='time', by='planner', patch_artist=True)
        
        # Personalización del color verde clarito
        for box in boxplot.artists:
            box.set_facecolor('#d4f8e8')
        
        plt.title("")
        plt.suptitle("")
        plt.xlabel("planner")
        plt.ylabel("time")
        plt.xticks(rotation=45)  # Rotar labels para mejor visibilidad
        plt.grid(False)
        plt.tight_layout()
        
        # Guardar el gráfico
        db_name = os.path.basename(db_path).replace('.db', '')
        output_path = os.path.join(output_folder, f"{db_name}_boxplot.png")
        plt.savefig(output_path)
        plt.close()
        print(f"Gráfico guardado en: {output_path}")
    
    except Exception as e:
        print(f"Error procesando {db_path}: {e}")

# Recorrer todos los archivos .db en la carpeta
for file in os.listdir(input_folder):
    if file.endswith(".db"):
        db_path = os.path.join(input_folder, file)
        process_db_file(db_path, output_folder)

print("Procesamiento completado.")
