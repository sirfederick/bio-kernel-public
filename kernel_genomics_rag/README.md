# kernel_genomics_rag

`kernel_genomics_rag` es un prototipo minimalista de **Retrieval Augmented Generation (RAG)** orientado a datos genómicos. Incluye un pipeline ETL para obtener datos de Ensembl, construcción de un índice FAISS con embeddings y agentes basados en GPT-4 para generar y validar hipótesis.

## Requisitos

- Python ≥ 3.10  
- Dependencias listadas en [`requirements.txt`](requirements.txt)  
- Una clave válida de API de OpenAI (`OPENAI_API_KEY`)

## Instalación rápida

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Variables de entorno
Antes de ejecutar cualquier script, defina:

Variable	Descripción
OPENAI_API_KEY	Clave para acceder a los modelos de OpenAI
OPENAI_API_BASE	(Opcional) URL alternativa del endpoint
ENSEMBL_OUT_CSV	(Opcional) Ruta para el CSV generado por ETL

Puede almacenarlas en un archivo .env y cargarlas con python-decouple o exportarlas en consola.

Obtención de datos de ejemplo
Ejecute el ETL para descargar datos desde Ensembl y generar un CSV:

```
python data_pipeline/etl_ensembl.py
Por defecto, el resultado se guarda en data/ensembl_sample.csv. Esta ruta puede modificarse usando la variable ENSEMBL_OUT_CSV
```

Construcción del índice y ejecución del prototipo
El script principal construye el índice FAISS si no existe y ejecuta una consulta demo:
```
python main.py
El índice se guarda en data/faiss.index junto con data/texts.json que contiene los textos usados para embeddings.
```
Ejecutar pruebas
Para correr las pruebas rápidas use:
```
pytest -m fast -q
```
Si faltan dependencias o surgen errores, asegúrese de instalar todos los paquetes en requirements.txt. Un resumen OK indica que todas las pruebas pasaron correctamente.

Arquitectura y flujo general
kernel_genomics_rag/
├── data_pipeline/      # Descarga y normaliza datos de Ensembl
├── rag/                # Construcción del índice FAISS y consultas
├── agents/             # Agentes de generación y validación con GPT-4
└── main.py             # Orquesta la demostración completa

etl_ensembl.py: obtiene datos de la API Ensembl y los guarda como CSV.
vector_store.py: genera o reutiliza índice FAISS a partir del CSV.
rag_engine.py: permite consultar el índice para recuperar textos relevantes.
AnnotatorAgent: usa GPT-4 para proponer hipótesis.
ValidatorAgent: ejemplifica evaluación básica de hipótesis.

Buenas prácticas
Mantenga las claves API fuera del control de versiones, preferiblemente en .env.
Reutilice el índice FAISS para acelerar pruebas y evitar recomputación.
Extienda AnnotatorAgent con nuevos prompts o modelos según necesidades.
Valide los datos descargados antes de alimentar el sistema RAG.
Versione los datos de entrada y los índices generados para asegurar reproducibilidad.
Supervise costos y tiempos de respuesta de las llamadas al modelo de lenguaje.
Documente cualquier cambio relevante para facilitar mantenimiento y evolución.

## Validación de datos y configuraciones

- El CSV generado por `etl_ensembl.py` puede validarse con el esquema JSON
  [`schemas/ensembl_csv_schema.json`](../schemas/ensembl_csv_schema.json).
  Una validación sencilla con `jsonschema` sería:

  ```python
  import json
  import pandas as pd
  from jsonschema import validate

  schema = json.load(open("schemas/ensembl_csv_schema.json"))
  records = pd.read_csv("data/ensembl_sample.csv").to_dict(orient="records")
  for row in records:
      validate(row, schema)
  ```

- La configuración avanzada del índice FAISS se define en
  [`kernel_quantum/rag_index/config/rag_index_config.yaml`](../kernel_quantum/rag_index/config/rag_index_config.yaml)
  y se valida con
  [`kernel_quantum/rag_index/config/schemas/rag_index_config-schema.json`](../kernel_quantum/rag_index/config/schemas/rag_index_config-schema.json).

## Dependencias pesadas

Este módulo requiere `langchain`, `faiss-cpu` y `openai`. Para un entorno local:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Si no se dispone de estas librerías o de conectividad a la API de OpenAI, las
pruebas incluyen ejemplos de *mocks* para simularlas y evitar llamadas reales.
