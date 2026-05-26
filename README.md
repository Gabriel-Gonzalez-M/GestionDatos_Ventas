# RetailData Pro - Pipeline de Datos para IA

Proyecto de automatización de gestión de datos (DataOps) para el sector Retail.

## Estructura del Proyecto
- `data/raw`: Datos de origen inmutables.
- `data/processed`: Datos validados y anonimizados.
- `src/pipeline.py`: Script principal de automatización.
- `logs/` y `logs_old/`: Sistema de monitoreo y auditoría.

## Requisitos
- Python 3.12+
- Pandas

## Instrucciones de Ejecución
1. Clonar el repositorio.
2. Ejecutar `python src/pipeline.py`.
3. Revisar los resultados en `data/processed/` y las evidencias en `logs/`.