# Arquitectura Bio-Kernel

```mermaid
flowchart TD
    A[Collector] --> B[Curator]
    B --> C[Kernel Builder Gen]
    C --> D[RAG Index]
    D --> E[Orchestrator]
    E --> F[Reverse Engineering]
```

Este diagrama resume el flujo principal entre módulos. Cada etapa genera artefactos
que alimentan a la siguiente. Los detalles completos se encuentran en los README
individuales de cada submódulo.
