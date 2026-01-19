# kernel_quantum

**kernel_quantum** es el núcleo cognitivo del proyecto **bioKernel**, diseñado para integrar **bioinformática avanzada, aprendizaje multiagente y técnicas de ingeniería inversa** en un mismo motor.  
El sistema convierte datos genómicos, literatura científica, patentes y binarios en **conocimiento computable** para descubrimiento y razonamiento autónomo.

---

## 1. Propósito General

El motor **kernel_quantum**:

- Ingresa datos desde fuentes científicas, APIs y repositorios.
- Estructura, valida y enriquece la información.
- Genera **representaciones vectoriales** (embeddings) para indexación semántica.
- Coordina **agentes autónomos locales y remotos** que colaboran para analizar, correlacionar y descubrir patrones.

La visión es construir un entorno donde la IA **aprenda, razone y genere hipótesis científicas** a partir de múltiples fuentes heterogéneas.

---

## 2. Arquitectura y Componentes

El motor está organizado en **módulos especializados**, cada uno con responsabilidades claras y documentación interna propia.

### Módulos principales

#### 2.1 Collector

- Descarga datos desde APIs científicas y de patentes.
- Almacena datos crudos en formato reproducible.
- **Ruta:** `kernel_quantum/collector/`
- **README:** [collector/README.md](kernel_quantum/collector/README.md)

#### 2.2 Curator

- Limpia, valida y enriquece los datos provenientes de Collector.
- Genera datasets curados y preparados para indexación.
- **Ruta:** `kernel_quantum/curator/`
- **README:** [curator/README.md](kernel_quantum/curator/README.md)

#### 2.3 Models

- Administra modelos locales (GGUF) y remotos (APIs).
- Provee una interfaz unificada para que los agentes accedan a los modelos.
- **Ruta:** `kernel_quantum/models/`
- **README:** [models/README.md](kernel_quantum/models/README.md)

#### 2.4 Orchestrator

- Coordina los agentes y sus flujos de trabajo multiagente.
- Gestiona el uso de modelos y distribuye las tareas.
- **Ruta:** `kernel_quantum/orchestrator/`
- **README:** [orchestrator/README.md](kernel_quantum/orchestrator/README.md)

#### 2.5 Agents

- Implementaciones concretas de agentes locales y remotos.
- **Ruta:** `kernel_quantum/agents/`
- **README:** [agents/README.md](kernel_quantum/agents/README.md)

#### 2.6 RAG Index

- Mantiene los índices vectoriales semánticos (genomas, literatura, patentes y binarios).
- Provee búsquedas contextuales y semánticas.
- **Ruta:** `kernel_quantum/rag_index/`
- **README:** [rag_index/README.md](kernel_quantum/rag_index/README.md)

#### 2.7 Reverse Engineering

- Analiza binarios y librerías (DLL/SO).
- Extrae estructuras y símbolos para generar embeddings y enriquecer el RAG.
- **Ruta:** `kernel_unknown_engine/reverse_docs/`
- **README:** [reverse_docs/README.md](../kernel_unknown_engine/reverse_docs/README.md)

#### 2.8 Shared

- Utilidades comunes (logging, helpers).
- **Ruta:** `kernel_quantum/shared/`
- **README:** [shared/README.md](kernel_quantum/shared/README.md)

#### 2.9 Storage

- Almacena datos intermedios y temporales durante la ejecución.
- **Ruta:** `kernel_quantum/storage/`
- **README:** [storage/README.md](kernel_quantum/storage/README.md)

---

## 3. Flujo de Trabajo Global

Fuentes externas (APIs científicas, patentes, binarios)  
↓  
**Collector** (adquisición y logging)  
↓  
**Curator** (validación, curación y enriquecimiento)  
↓  
**RAG Index** (vectorización e indexación semántica)  
↓  
**Orchestrator** (coordinación multiagente)  
↓  
**Agentes** (razonamiento, descubrimientos, informes)

Los agentes utilizan **Models** para acceder a LLMs locales y remotos, y pueden disparar análisis específicos en **Reverse Engineering**.  
Los módulos **Shared** y **Storage** soportan funciones transversales.

---

## 4. Buenas Prácticas y Estándares

El desarrollo sigue normas y principios internacionales:

- **ISO/IEC 25010:** Calidad, mantenibilidad y portabilidad
- **ISO/IEC 42010:** Arquitectura modular documentada
- **ISO/IEC 11179:** Gestión de metadatos
- **ISO/IEC 27001:** Seguridad de datos y trazabilidad
- **FAIR Principles:** Datos accesibles, interoperables y reutilizables

**Buenas prácticas adoptadas:**

- Configuración declarativa mediante YAML/JSON validados por esquemas.
- Logging estructurado en formato NDJSON.
- Separación clara entre datos crudos, curados y vectorizados.
- Documentación modular con READMEs detallados.
- Estrategia incremental: primero documentación y diseño, luego implementación por etapas.

---

## 5. Próximos Pasos

- Completar **integración distribuida** con Ray para procesos multiagente.
- Ampliar cobertura de tests unitarios e integración (CI/CD).
- Extender reverse engineering a análisis dinámico.
- Automatizar ingestión masiva y workflows científicos con modelos híbridos.

---

## 6. Índice de Documentación Interna

Para cada módulo, revisar su README:

- **Collector:** [kernel_quantum/collector/README.md](kernel_quantum/collector/README.md)
- **Curator:** [kernel_quantum/curator/README.md](kernel_quantum/curator/README.md)
- **Models:** [kernel_quantum/models/README.md](kernel_quantum/models/README.md)
- **Orchestrator:** [kernel_quantum/orchestrator/README.md](kernel_quantum/orchestrator/README.md)
- **RAG Index:** [kernel_quantum/rag_index/README.md](kernel_quantum/rag_index/README.md)
- **Reverse Engineering:** [kernel_unknown_engine/reverse_docs/README.md](../kernel_unknown_engine/reverse_docs/README.md)
- **Shared:** [kernel_quantum/shared/README.md](kernel_quantum/shared/README.md)
- **Storage:** [kernel_quantum/storage/README.md](kernel_quantum/storage/README.md)

Además, en `kernel_quantum/docs/` se encuentran guías de instalación y diagramas de arquitectura
para facilitar la puesta en marcha del sistema.

## 7. Esquemas de validación

Los reportes clave generados a lo largo del proyecto se validan con los esquemas ubicados en
[`../schemas`](../schemas):

- [`unknown_genes_schema.json`](../schemas/unknown_genes_schema.json) &ndash; define cada línea del
  archivo `unknown_genes.ndjson` producido por _kernel_builder_gen_.
- [`clusters_schema.json`](../schemas/clusters_schema.json) &ndash; comprueba el formato de
  `clusters.ndjson` generado por el _clusterer_ en _kernel_unknown_engine_.
- [`master_report_schema.json`](../schemas/master_report_schema.json) &ndash; describe la estructura
  del consolidado `master_report.json` que integra el orquestador.

---

## 8. Ejecución y Despliegue

- **Local**: `python -m kernel_quantum.orchestrator`
- **Local Runner**: incluido al ejecutar `python -m local_runner --all`
- **Docker**: `docker-compose up kernel_quantum`
- **Kubernetes**: aplicar `kubernetes/kernel_quantum.yaml`

## 9. Filosofía del Proyecto

Este motor es todavía joven, como un **potrero científico** en el que se entrenan modelos e ideas.  
Con cada iteración, kernel_quantum busca convertirse en una **infraestructura de IA científica distribuida** que, al igual que un talento innato como Maradona a los 12 años, ya demuestra el potencial para transformar su campo.

---

## Pruebas

Para validar el funcionamiento básico del motor ejecuta:

```bash
pytest tests/kernel_quantum -m fast
```

Estas pruebas cubren la validación de configuraciones y utilidades principales sin depender de modelos pesados.

---

**kernel_quantum** no es solo un motor, es una apuesta por **crear conocimiento a partir de los datos** y abrir nuevas rutas de descubrimiento en ciencia y tecnología.
