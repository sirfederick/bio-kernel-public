kernel_brain_main
kernel_brain_main es el orquestador maestro del proyecto bioKernel, encargado de coordinar y gestionar la ejecución integrada de todos los módulos principales del sistema genómico. Su función principal es controlar el flujo de datos y tareas entre los módulos builder, quantum, RAG, unknown engine y agent loop, garantizando una ejecución ordenada, confiable y auditada mediante una configuración centralizada y estándares internacionales.

1. Propósito
El orquestador tiene como objetivos fundamentales:

Ejecución coordinada: Lanza y controla las etapas del pipeline genómico, que pueden ejecutarse de forma secuencial para trazabilidad o paralela para optimización de tiempos usando el framework Ray.

Auditoría y trazabilidad: Registra todos los eventos relevantes (inicios, finalizaciones, errores, resultados intermedios) en archivos NDJSON en `logs/orchestrator_master.ndjson`.
Cada evento sigue el esquema [`../schemas/orchestrator_log_schema.json`](../schemas/orchestrator_log_schema.json) para su validación.

Punto único de entrada: Sirve como interfaz de control central para lanzar procesos, manejar configuraciones y generar reportes consolidados en reports/.

2. Archivo de configuración (config.yaml)
La configuración centralizada se almacena en kernel_brain_main/config.yaml. Esta define parámetros globales, rutas base, opciones específicas de cada módulo y políticas de ejecución. Para asegurar calidad y seguridad, esta configuración sigue las normas:

ISO/IEC 25010: Modelo de calidad de producto software (funcionalidad, fiabilidad, usabilidad, eficiencia, mantenibilidad y portabilidad).

ISO/IEC 12207: Procesos del ciclo de vida del software (gestión, desarrollo, operación y mantenimiento).

ISO/IEC 27001: Gestión de seguridad de la información.

Ejemplo resumido de config.yaml:
yaml
Copiar
version: "1.0.0"

global:
  log_level: INFO           # Nivel de logging: DEBUG, INFO, WARN, ERROR
  max_retries: 3            # Reintentos en caso de fallo en módulos críticos

paths:
  base_data_dir: "/data/bio_kernel/genoma"
  logs_dir: "logs"
  reports_dir: "reports"

modules:
  kernel_builder_gen:
    batch_size: 1000        # Tamaño de lote para procesamiento masivo
    retry_policy:
      max_attempts: 3
      backoff_seconds: 5
  kernel_quantum:
    parallelism_degree: 8   # Número de workers para tareas concurrentes
  kernel_genomics_rag:
    cache_enabled: true
  kernel_unknown_engine:
    timeout_seconds: 120
  agent_loop:
    enabled: true
Esta configuración puede adaptarse a diferentes entornos y escalas, facilitando despliegues reproducibles y auditoría.

3. Ejecución del Orquestador
Antes de ejecutar el orquestador, instala el proyecto en modo editable para facilitar la resolución de dependencias y permitir desarrollo activo:

bash
Copiar
pip install -e .
Modos de ejecución
Secuencial (por defecto): Ejecuta las etapas del pipeline en orden, útil para debugging, pruebas y entornos con recursos limitados.

bash
Copiar
python -m kernel_brain_main.main --mode sequential
Paralelo (con Ray): Aprovecha múltiples núcleos para acelerar la ejecución, especialmente útil en entornos productivos o con gran volumen de datos.

bash
Copiar
python -m kernel_brain_main.main --mode parallel
Los reportes consolidados se generan en reports/ y los logs detallados en logs/. El sistema maneja automáticamente reintentos y errores según políticas configuradas.

4. Estándares y Buenas Prácticas
El proyecto está alineado con estándares internacionales para asegurar calidad y seguridad:

ISO/IEC 25010: Garantiza la calidad del software en aspectos funcionales y no funcionales.

ISO/IEC 12207: Define procesos estructurados para el ciclo de vida del software.

ISO/IEC 27001: Aplica controles y políticas de seguridad de la información.

Se implementan controles de acceso, registro seguro de logs y manejo robusto de errores. Esto permite auditorías externas y cumplimiento normativo para aplicaciones críticas en bioinformática.

5. Mini-módulos, RAG_core y Validación
Arquitectura modular con mini-módulos
Para mantener un diseño escalable y limpio, el directorio mini_modulos/ contiene microservicios especializados en el procesamiento y validación de resultados generados por cada módulo principal. Estos mini-módulos ejecutan tareas de:

Validación estructural y semántica de datos.

Limpieza y transformación de información.

Integración con la base de datos RAG_core, que almacena datos curados y accesibles para consulta y análisis.

Estructura del directorio mini_modulos/:
text
Copiar
mini_modulos/
├── mini_ker_quantum/
├── mini_ker_genomics_rag/
├── mini_ker_unknown_engine/
└── mini_ker_builder_gen/
Esta capa funciona como un filtro que desacopla la alta velocidad de producción de datos en los módulos principales, permitiendo un análisis y validación pausada y exhaustiva.

Validación con esquemas JSON
Todos los archivos generados se validan con esquemas JSON estrictos localizados en ../schemas para asegurar integridad y conformidad.

unknown_genes_schema.json: Valida el formato de kernel_builder_gen/reports/unknown_genes.ndjson antes de su consumo o procesamiento posterior.

master_report_schema.json: Define la estructura definitiva del reporte maestro reports/master_report.json que consolida la información procesada.

Esto asegura que los datos que avanzan en el pipeline son consistentes y confiables.


6. API REST
El archivo `openapi.yaml` define un esquema OpenAPI minimal para exponer el estado y la ejecución del orquestador.

7. Contratos de datos
`schemas/brain_main_config-schema.json` describe la validación de `config.yaml`. Para comunicación gRPC se provee `protos/orchestrator.proto`.

8. Docker
Se incluye `Dockerfile` para construir la imagen del orquestador y Dockerfiles individuales para los mini-módulos.

9. Motor científico (Etapa 02)
El microservicio `scientific_engine` procesa consultas científicas empleando un
motor RAG con modelos LLM locales y auditoría remota.

- **Endpoint principal**: `/engine/query`.
- **LLMs locales**: DeepSeeK, TinyLLaMA y Mistral.
- **Auditor remoto**: ChatGPT vía API (opcional).
- **Seguridad**: autenticación por token, TLS y registro en `logs/scientific_engine.ndjson`.

Para ejecutar de forma independiente:
```bash
uvicorn kernel_brain_main.scientific_engine.engine:app
```
Consulte `scientific_engine/README.md` para más detalles.
