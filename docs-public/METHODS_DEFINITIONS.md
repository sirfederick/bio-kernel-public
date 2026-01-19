# 📏 Bio-Kernel: Formal Definitions & Glossary
> **Document ID:** BK-METHODS-V4 | **Context:** Statistical Framework | **Type:** Standard

```text
     [A] --- [B]
      |       |    "Precision in language is the
      |       |     first step to precision in code."
     [C] --- [D]
```

## 1. Tokenization and Alphabet ($\Sigma$)

**Token / Opcode**: A categorical symbol emitted by the reverse-engineering module from a gene-derived artifact.
- **Alphabet ($\Sigma$)**: The set of all opcode strings observed across all analyzed loci (e.g., `MOV_PROMOTER`, `JMP_EXON`).
- **Token Sequence**: For each locus $\ell$, we obtain an ordered sequence $S_\ell = (s_1, s_2, \dots, s_L)$ with $s_i \in \Sigma$.

> *Caveat*: Tokens are a computational representation for the Bio-Kernel pipeline; they are not asserted to be literal "instructions" in a biological vivo sense.

## 2. Pattern Definition

**n-gram Pattern**: A contiguous subsequence of length $n$ over $\Sigma$.

$$
P = (s_i, s_{i+1}, \dots, s_{i+n-1})\quad,\quad n=8\ \text{(default)}
$$

A pattern is said to be **present** in a sequence if it appears at least once as a contiguous chunk.

## 3. Coupling ("Acople Lógico")

A **Coupling Group** is a set of genomic loci across $\ge 2$ chromosomes selected by the neighborhood heuristic.

For a coupling group $G = \{\ell_1, \dots, \ell_k\}$ with sequences $S_{\ell_j}$:
- Let $\mathcal{N}(S_{\ell_j})$ be the set of all n-grams in $S_{\ell_j}$.
- A coupling exists if $\cap \mathcal{N}(S_{\ell_j}) \neq \emptyset$ (Intersection is non-empty) AND the probability of random intersection is $p < 0.05$.

## 4. Trident Layers
The **Trident** analysis engine operates on four distinct abstraction layers:
1.  **L1 (Static)**: Raw sequence alignment (BLAST-like).
2.  **L2 (Dynamic)**: Symbolic execution of the `.bioelf` binary representation.
3.  **L3 (Semantic)**: Embedding vector lookup in the RAG store.
4.  **L4 (Quantum)**: Probabilistic superposition of unknown gene functions.

---
> *Status: Frozen Definition Set v4.0.1*
