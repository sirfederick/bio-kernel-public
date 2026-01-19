# kernel_unknown_engine

`kernel_unknown_engine` es el laboratorio autónomo encargado de estudiar genes con puntaje de `unknown_score` elevado. Funciona como complemento de **kernel_quantum** y **kernel_builder_gen**, procesando datos sin caracterizar para generar conocimiento estructurado.

## Submódulos principales

```
kernel_unknown_engine/
 ├── clusterer/           # Código de agrupamiento
 ├── hypotheses/          # Generación de hipótesis
 ├── reverse_engineering/ # Análisis de binarios
 ├── rag_memory/          # Índices vectoriales
 ├── agent_loop/          # Bucle de auto-mejora
 ├── security_layer/      # Sandbox y validaciones
 └── example_data/        # Datos de ejemplo y reportes
     ├── raw/
     ├── clusterer/
     ├── hypotheses/
     ├── reverse_engineering/
     └── reports/
```

Cada carpeta contiene un `README.md` con detalles de objetivos, entradas y salidas.

## Flujo general

1. **Entrada de genes desconocidos** desde `kernel_builder_gen` o `raw/`.
2. **Clusterer** agrupa secuencias y genera `clusters.ndjson`.
3. **Hypotheses** propone funciones potenciales guardadas en `hypotheses.ndjson`.
4. **Reverse engineering** analiza binarios y produce `re_analysis.ndjson`.
5. **rag_memory** indexa embeddings para búsquedas semánticas.
6. **Agent loop** orquesta estas tareas de forma continua.
7. **Reports** consolida la información en `unknown_summary.ndjson` y `unknown_clusters.json`.

### Integración con `agent_loop` y `SecurityOrchestrator`

El componente `agent_loop` permite ejecutar el motor de forma
asíncrona y distribuir tareas en un clúster Ray. Para cada binario
recibido se invoca el `SecurityOrchestrator`, encargado de coordinar
agentes antivirus (heurísticos, gráficos y remotos) y decidir si se
permite el análisis, se pone en cuarentena o se bloquea. El
`SecurityOrchestrator` registra eventos en `security_events.ndjson` y
puede reanudar archivos que queden pendientes en la carpeta de
cuarentena.

## Estandares y convenciones

- Documentación y metadatos siguiendo **ISO/IEC 25010**, **42010** y **11179**.
- Configuración declarativa mediante YAML con validación por JSON Schema.
- Registros operativos en formato **NDJSON** con timestamp ISO8601.
- Interacción directa con el orquestador `kernel_quantum` a través de los reportes generados.

## Esquemas de reportes

Los resultados se validan con los esquemas en [`../schemas`](../schemas):

- [`clusters_schema.json`](../schemas/clusters_schema.json) &ndash; define cada entrada de `clusters.ndjson` producida por el *clusterer*.
- [`master_report_schema.json`](../schemas/master_report_schema.json) &ndash; especifica la estructura del resumen `master_report.json`.

Este documento sirve como guía de alto nivel para navegar el módulo y entender cómo se relacionan sus componentes.

## Ejecución y Despliegue

- **Local**: `python -m kernel_unknown_engine.main`
- **Local Runner**: incluido al ejecutar `python -m local_runner --all`
- **Docker**: `docker-compose up kernel_unknown_engine`
- **Kubernetes**: aplicar `kubernetes/kernel_unknown_engine.yaml`

## Pruebas

Para ejecutar las pruebas rápidas de este laboratorio utiliza:

```bash
pytest tests/kernel_unknown_engine -m fast
```

Las pruebas validan los esquemas generados y la integración básica con el orquestador.
