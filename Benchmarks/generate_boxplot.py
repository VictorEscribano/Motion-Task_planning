import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Directorios de entrada y salida
input_folder = r"Benchmarks\Results_Benchmarks_MOVEs\DBs"  # Ruta de archivos .db
output_folder = r"Benchmarks\Results_Benchmarks_MOVEs\plots"  # Carpeta para guardar imágenes

# Asegurarse de que el directorio de salida existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Función para procesar un archivo .db y generar gráficos
def process_db_file(db_path, output_folder):
    try:
        conn = sqlite3.connect(db_path)
        
        # Obtener datos relevantes de las tablas
        planner_query = "SELECT id, name FROM plannerConfigs"
        runs_query = "SELECT plannerid, time, solved, solution_length FROM runs"
        
        planners_df = pd.read_sql_query(planner_query, conn)
        runs_df = pd.read_sql_query(runs_query, conn)
        
        # Combinar datos con nombres de planners
        merged_df = runs_df.merge(planners_df, left_on="plannerid", right_on="id")
        merged_df = merged_df.rename(columns={"name": "planner"})
        
        conn.close()
        
        # Nombre base del archivo
        db_name = os.path.basename(db_path).replace('.db', '')

        # Gráfico 1: Box Plot de "time"
        plt.figure(figsize=(20, 8))
        merged_df.boxplot(column='time', by='planner', patch_artist=True)
        for box in plt.gca().artists:
            box.set_facecolor('#d4f8e8')  # Verde clarito
        plt.title(f"Time Results for {db_name}")
        plt.suptitle("")
        plt.xlabel("Planner")
        plt.ylabel("Time")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{db_name}_time.png"))
        plt.close()

        # Gráfico 2: Box Plot de "solved"
        plt.figure(figsize=(20, 8))
        merged_df.boxplot(column='solved', by='planner', patch_artist=True)
        for box in plt.gca().artists:
            box.set_facecolor('#d4f8e8')  # Verde clarito
        plt.title(f"Solved Results for {db_name}")
        plt.suptitle("")
        plt.xlabel("Planner")
        plt.ylabel("Solved")
        plt.yticks([0, 1], ["Not Solved", "Solved"])
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{db_name}_solved.png"))
        plt.close()

        # Gráfico 3: Box Plot de "solution_length"
        plt.figure(figsize=(20, 8))
        merged_df.boxplot(column='solution_length', by='planner', patch_artist=True)
        for box in plt.gca().artists:
            box.set_facecolor('#add8e6')  # Azul claro
        plt.title(f"Solution Length Results for {db_name}")
        plt.suptitle("")
        plt.xlabel("Planner")
        plt.ylabel("Solution Length")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, f"{db_name}_solution_length.png"))
        plt.close()

        print(f"Gráficos guardados para {db_name}")
    
    except Exception as e:
        print(f"Error procesando {db_path}: {e}")

# Recorrer todos los archivos .db en la carpeta
for file in os.listdir(input_folder):
    if file.endswith(".db"):
        db_path = os.path.join(input_folder, file)
        process_db_file(db_path, output_folder)

print("Procesamiento completado.")
