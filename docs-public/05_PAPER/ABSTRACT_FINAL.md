# Scientific Abstract: Bio-Kernel Framework
# Status: DRAFT (Reviewer-Safe)
# Date: 2026-01-18

## Title
**A Null-Aware, Alignment-Free Framework for Token-Based Recurrence Mining and Genome-Scale Prioritization**

## Abstract
Genomic analysis often relies on alignment and homology search to infer function, but these approaches do not directly answer a different question: *which short signatures recur across loci under a defined representation, and which remain surprising under structured null models?* Here we present **Bio‑Kernel**, an alignment-free token pattern mining pipeline designed for **prioritization**, not functional inference. The pipeline generates per-gene artifacts, maps sequence-derived features into a categorical token alphabet, mines cross-locus $n$-gram recurrence, and evaluates candidates with permutation-based null models including local-structure-preserving block shuffles.

In the current artifacts accompanying this draft, a discovery run evaluates 76 distinct 8-grams across a 3-marker coupling set and reports 18 survivor patterns under the block-shuffle null ($N=1000$ permutations; block-size sensitivity panel $B\in\{5,10,20,50,100\}$). Multiple testing is controlled via Benjamini–Hochberg q-values within the evaluated universe (minimum $q\approx 0.101$; therefore we do not claim FDR $<0.05$). Separately, the workspace processing snapshot documents chromosomes 20/21/22 and 958 genes processed with audit artifacts.

Functional interpretation is explicitly out of scope and requires orthogonal validation.

**Keywords:** alignment-free, tokenization, recurrence mining, permutation tests, structured null models, prioritization.
