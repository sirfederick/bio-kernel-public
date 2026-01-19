# Methodology & Validation

Bio-Kernel utilizes an **alignment-free, token-based approach** to genomic analysis. The goal is to identify structural recurrence that is statistically unlikely to occur by chance.

## 1. Tokenization (Binarization)
We transform the DNA sequence (A, C, G, T) into a digital alphabet based on physical and chemical properties:
- **Purine vs. Pyrimidine** (0/1)
- **Strong vs. Weak Hydrogen Bonds** (0/1)

This transformation produces a "Bio-OpCode" stream: $[0, 1, 1, 0, \dots]$. By analyzing these streams instead of raw nucleotides, we can apply standard signal processing and binary auditing techniques.

## 2. Trident Pattern Mining
The mining engine scans these streams searching for **$n$-gram recurrence** ($n=8$ tokens by default).
- We look for identical patterns that appear in multiple genes across different chromosomes.
- We quantify the **Entropy** of these patterns: high-entropy patterns (complex logic) are prioritized over low-entropy ones (simple repeats).

## 3. The Null Hypothesis (The "Chaos Monkey")
To ensure our findings are not statistical artifacts, every identified pattern must pass a **Permutation Test**.

### Permutation Strategy
We create $N=1000$ "shuffled" versions of the genomic data for each locus. We use three increasingly strict null models:
1. **Mono-Shuffle:** Randomly shuffles all bits (preserves $0/1$ counts).
2. **Di-Shuffle:** Preserves bit-pair frequencies (preserves local bias).
3. **Block-Shuffle:** Shuffles chunks of bits ($20$ bits per block). This preserves local "motifs" but destroys long-range syntax.

### Statistics (Z-Score & P-Value)
For each pattern, we calculate a **Z-Score** based on its recurrence relative to the null distribution:
$$Z = \frac{x - \mu}{\sigma}$$
Where:
- $x$ is the observed recurrence.
- $\mu$ is the mean recurrence in $1000$ permutations.
- $\sigma$ is the standard deviation in $1000$ permutations.

A **Z-Score > 4.0** (or $p < 0.001$) is required for a pattern to be labeled a **"Survivor"**.

## 4. Survivor Cataloguing
When a pattern survives all null tests across multiple chromosomes (e.g., Chr3, Chr20, Chr22), it is catalogued as a **Shared Library**. These represent the core findings of the Bio-Kernel pipeline.

---
*Next: [Observability Summary](04_MARKETING/README.md)*
