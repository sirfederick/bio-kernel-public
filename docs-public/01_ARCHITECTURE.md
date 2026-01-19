# System Architecture

Bio-Kernel is designed as a distributed, modular framework for genomic reverse-engineering. The system follows a decoupled architecture that separates data ingestion, pattern mining, and statistical validation.

## High-Level Design

The framework is organized into three main functional layers:

### 1. The Ingestion Layer
- **Responsibility:** Ingests raw genomic data (FASTA/VCF) and converts it into a standardized digital representation.
- **Representation:**DNA "OpCodes" based on chemical properties.
- **Outcome:** Clean, machine-readable binary streams ready for static analysis.

### 2. The Trident Mining Engine
- **Responsibility:** The computational core of the system. It performs multi-threaded scanning of binarized streams.
- **Mining Logic:** Uses a rolling window $n$-gram approach to detect recurrence.
- **Profiling:** Generates categorical alphabets and entropy profiles for every processed gene.

### 3. The Validation & Intelligence Layer
- **Responsibility:** Acts as the "linter" and statistical gatekeeper.
- **Null Models:** Implements various Monte Carlo simulations (Mono-shuffle, Di-shuffle, Block-shuffle) to test if patterns are random noise.
- **Reporting:** Produces aggregated metrics, "Survivor" catalogues, and observability logs.

## Data Flow
```mermaid
graph LR
    DNA[Raw DNA] --> Ingest[Ingestion]
    Ingest --> Binary[Bio-OpCodes]
    Binary --> Trident[Trident Miner]
    Trident --> Metrics[Unvalidated Patterns]
    Metrics --> Valid[Validation Layer]
    Valid --> Reports[Public Reports]
```

## Key Modules (Conceptual)
- **Orchestrator:** Manages the lifecycle of processing runs and concurrent workers.
- **Pattern Miner:** The high-speed search engine for $n$-gram recurrence.
- **Hypothesis Tester:** The statistical engine that runs permutations to calculate Z-Scores and P-Values.
- **Dashboard:** The observability interface for monitoring pipeline health and results.

---
*Next: [Methodology & Validation](02_METHOD.md)*
