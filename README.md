# Bio-Kernel: Alignment-Free Genome Scanner

**Public Documentation & Observability Release**

## What is Bio-Kernel?

Bio-Kernel is an experimental alignment-free pattern mining framework designed to treat genomic sequences as legacy code. Instead of relying on traditional biological alignment, it converts DNA into token streams and identifies high-entropy recurrent structures ("survivor signatures") that persist against rigorous null-hypothesis testing.

This project approaches the genome from a software engineering perspective: treating non-coding regions not as "junk", but as libraries that have lost their linker references.

## Repository Scope

This repository (`bio-kernel-public`) is a **documentation-only snapshot** of the core internal system. It is designed to provide transparency, methodology details, and aggregated observability data without exposing the proprietary core logic or sensitive datasets.

### Included:
*   **Documentation:** High-level architecture, methodology, and definitions (`docs-public/`).
*   **Observability Snapshots:** Aggregated metrics, Z-Scores, and validation summaries from the latest audit (`docs-public/03_OBSERVABILITY/`).
*   **Marketing & Papers:** Public notes, articles, and scientific summaries (`docs-public/04_MARKETING/`, `docs-public/05_PAPER/`).
*   **Figures:** Visualizations of the pipeline and findings.

### NOT Included (Internal Core):
*   **Core Logic:** `kernel_*`, `agent_loop/`, `trident_engine/`.
*   **Raw Data:** `bin/` (binarized artifacts), `data/` (genomic references), `reports/` (raw CSVs/logs).
*   **Models:** FAISS indices, embeddings, and trained neural nets.

## Navigation

*   **[Mission & Overview](docs-public/SCIENTIFIC_MISSION_STATEMENT.md):** Conceptual introduction and scientific goals.
*   **[Blueprint](docs-public/BLUEPRINT.md):** Detailed system blueprint and architecture.
*   **[Infrastructure](docs-public/BIO_INFRASTRUCTURE.md):** Implementation details.
*   **[Methodology](docs-public/METHODS_DEFINITIONS.md):** Null hypothesis generation and validation logic.
*   **[Observability](docs-public/03_OBSERVABILITY/SUMMARY.md):** Latest run metrics and "Survivor" catalog summary.

## Validation & Transparency

While the source code is private, the methodology is open. We provide:
1.  **Strict Null Models:** Details on block-shuffling and permutation tests used to validate findings.
2.  **Aggregated Metrics:** Verifiable counts of processed genes and significant patterns.
3.  **Reproducible Logic:** Descriptions of the tokenization schemas to allow independent reproduction of the representation layer.

## Contact & Contribution

We welcome discussion on the methodology and interpretation of results.
*   **Issues:** Use the Issue tracker for questions regarding the documentation or methodology.
*   **Collaboration:** Contact the maintainers directly for access to the core research partnership program.

