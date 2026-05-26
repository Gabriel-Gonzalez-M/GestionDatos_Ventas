import pandas as pd
import os
import logging
from datetime import datetime
import shutil

# 1. CONFIGURACIÓN DE RUTAS
LOG_DIR = 'logs'
LOG_OLD_DIR = 'logs_old'
DATA_RAW_DIR = os.path.join('data', 'raw')
DATA_PROCESSED_DIR = os.path.join('data', 'processed')

def run_pipeline():
    # --- A. GESTIÓN DE LOGS ANTIGUOS (Log Rotation) ---
    # Lo hacemos antes de iniciar el logging para que no haya archivos bloqueados
    if os.path.exists(LOG_DIR):
        if not os.path.exists(LOG_OLD_DIR): 
            os.makedirs(LOG_OLD_DIR)
            
        for archivo in os.listdir(LOG_DIR):
            if archivo.endswith(".log"):
                ruta_origen = os.path.join(LOG_DIR, archivo)
                ruta_destino = os.path.join(LOG_OLD_DIR, archivo)
                try:
                    shutil.move(ruta_origen, ruta_destino)
                except Exception as e:
                    print(f"No se pudo mover el log antiguo {archivo}: {e}")

    # --- B. CONFIGURACIÓN DEL NUEVO LOG ---
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    log_filename = os.path.join(LOG_DIR, f"ejecucion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    # Reiniciamos la configuración del logger para cada ejecución
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        encoding='utf-8'
    )

    logging.info("Iniciando Pipeline de Datos de Ventas...")
    print("Ejecutando pipeline...")
    
    try:
        # 2. INGESTA
        path_raw = os.path.join(DATA_RAW_DIR, 'ventas.csv')
        df = pd.read_csv(path_raw)
        logging.info(f"Ingesta exitosa: {len(df)} registros cargados.")

        # 3. LIMPIEZA INICIAL
        df['precio_limpio'] = df['precio'].replace(r'[\$,]', '', regex=True)
        df['precio_limpio'] = pd.to_numeric(df['precio_limpio'], errors='coerce')
        df['ciudad_limpia'] = df['ciudad'].str.upper().str.strip()

        # LIMPIEZA DE FECHAS
        df['fecha'] = df['fecha'].astype(str).str.strip().str.replace(r'^/', '', regex=True)
        df['fecha_dt'] = pd.to_datetime(df['fecha'], errors='coerce', dayfirst=True)
        
        logging.info("Limpieza estructural y de fechas completada.")

        # 4. VALIDACIÓN ÚNICA (Anomalías Críticas)
        df_validado = df[
            (df['precio_limpio'] > 0) & 
            (df['productos'] > 0) & 
            (df['fecha_dt'].notna())
        ].copy()

        df_validado['fecha_limpia'] = df_validado['fecha_dt'].dt.strftime('%Y-%m-%d')
        
        filas_descartadas = len(df) - len(df_validado)
        logging.warning(f"Validación: se descartaron {filas_descartadas} registros por anomalías.")

        # 5. SEGURIDAD (Anonimización)
        df_validado['email'] = df_validado['email'].apply(lambda x: str(x)[:3] + "***@dominio.com")
        logging.info("Seguridad: datos sensibles anonimizados.")

        # 6. CARGA
        path_processed = os.path.join(DATA_PROCESSED_DIR, 'ventas_final.csv')
        df_validado.to_csv(path_processed, index=False)
        
        logging.info(f"Carga exitosa: Archivo guardado en {path_processed}")
        print(f"¡Éxito! Pipeline terminado. Filas procesadas: {len(df_validado)}")
        print(f"Nuevo log generado: {log_filename}")

    except Exception as e:
        logging.error(f"Error crítico en el pipeline: {str(e)}")
        print(f"Error: {e}")

if __name__ == "__main__":
    run_pipeline()