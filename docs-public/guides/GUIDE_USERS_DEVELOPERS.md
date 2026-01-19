# Guía rápida para usuarios y desarrolladores

Esta guía resume los pasos esenciales para poner en marcha **BioKernel**, ejecutar las pruebas y colaborar con el proyecto.

## Instalación básica
1. Crear un entorno virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
2. Instalar dependencias principales y de desarrollo:
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```
3. Generar la estructura inicial (si es la primera vez):
   ```bash
   python scaffold.py
   ```
4. Instalar el paquete en modo editable y configurar `pre-commit`:
   ```bash
   pip install -e .
   pre-commit install
   ```

## Configuración
- Edita `secrets_config.yaml` y define tus claves de API en `api_keys`.
- Ajusta rutas globales y parámetros en los YAML dentro de `kernel_quantum/orchestrator/config`.
- Valida los cambios con `jsonschema` para evitar errores en tiempo de ejecución.

## Ejecución del sistema
- Validación rápida de configuraciones:
  ```bash
  python -m kernel_quantum.sanity_pipeline --report
  ```
- Ejecución del orquestador maestro en modo secuencial:
  ```bash
  python -m kernel_brain_main.main --mode sequential
  ```

## Pruebas
- Ejecutar las pruebas rápidas de todo el proyecto:
  ```bash
  pytest -m fast
  ```
- Para una cobertura completa:
  ```bash
  pytest --cov=kernel_quantum --cov-report=term --cov-report=xml
  ```

## Modo Desatendido (God Mode & Full Genome Mining)

Para procesar todo el genoma en dos fases (Offline + Online):

### Fase 1: Minería Masiva (Offline)
Descarga y decompila el genoma completo sin bloqueos de API.
```bash
python run_all_chromosomes.py
```
*Salida:* Directorio `bin/` con binarios y análisis Ghidra.

### Fase 2: Enriquecimiento (Online)
Una vez terminada la Fase 1, ejecuta este script para conectar APIs externas (Ensembl, Homología) e indexar en RAG.
```bash
enrich_genome.bat  # o python tools/enrich_local_data.py
```

## Contribución
1. Crea una rama basada en `dev` y sigue el estilo de commit convencional.
2. Asegúrate de pasar `pre-commit` y las pruebas rápidas antes del PR.
3. Abre la solicitud de cambio contra `dev` detallando propósito y enlaces.
4. El equipo revisará la cobertura y coherencia de documentación antes de fusionar.

## Despliegue
Las acciones de GitHub se encargan de ejecutar linters, pruebas y el orquestador. Revisa los archivos en `.github/workflows` para comprender la secuencia. Para despliegues en servidores propios se recomienda replicar los pasos del workflow `tests.yml` y luego lanzar el orquestador con `python -m kernel_brain_main.main`.
