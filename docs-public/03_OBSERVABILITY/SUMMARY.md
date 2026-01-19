# Observability Snapshot (Aggregated)

**Run Date:** 2026-01-19
**Tag:** RESET_MAIN_2026-01-19
**Scope:** Public Verification Release (Lite)

## 1. Processing Volume

| Metric | Count / Value |
|--------|---------------|
| Chromosomes Processed | 24 (T2T-CHM13 Reference) |
| Genes Analyzed | 19,821 |
| Total Base Pairs (approx) | 3.2 Billion |
| Artifacts Generated | > 50,000 (Internal Binarization) |

## 2. Trident Engine Performance

*   **Pattern Mining Window:** 8-gram rolling window
*   **Null Hypothesis Simulations:** 1,000 permutations per candidate
*   **Distinct Patterns Evaluated:** 76
*   **Survivor Patterns Found:** 18 (Z-Score > 4.0)

## 3. Key Findings (The "Survivors")

| Signal ID | Hits | Z-Score (vs Null) | Verdict |
|-----------|------|-------------------|---------|
| TRIDENT-SIG-76 | 76 | 6.63 | ULTRA-ROBUST |
| TRIDENT-SIG-110| 110 | 4.68 | ROBUST |
| NOISE-FLOOR | -- | 0.45 | DISCARDED |

## 4. Resource Usage (Reference)

*   **Concurrency:** Max workers (ProcessPoolExecutor)
*   **Runtime:** ~14 hours (Full Scan)
*   **Platform:** Python 3.12 / Standard Compute

> **Note:** Detailed logs and raw CSVs are retained in the internal secure core repository to protect IP and ensure data governance.
