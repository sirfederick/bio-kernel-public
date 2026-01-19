
# Building a genome scanner without claiming meaning (receipts-first)

**By [Your Name/Team Name]**  
*Date: January 18, 2026*

---

## The premise

There’s a temptation in genomics writing to jump straight from “pattern” to “purpose.”

Bio‑Kernel is deliberately trying to do the opposite:

> Build an instrument that can scan, count recurrence under a defined representation, and test it against structured nulls — without claiming biological mechanism.

This is not a philosophy post masquerading as a methods paper. It’s the “why” behind a very specific engineering choice: **artifacts first**.

---

## What Bio‑Kernel does (and does not do)

Bio‑Kernel produces reproducible outputs:

- per-gene artifacts (binary + metadata + profiles),
- token streams (a categorical alphabet used for counting patterns),
- recurrence mining of short $n$-grams,
- permutation-based null testing (including block shuffles),
- export tables (“survivors”, sensitivity, passports).

Bio‑Kernel does **not** claim:

- function, mechanism, causality,
- “the genome is an operating system,”
- “we decoded the species.”

If we ever talk like that, it’s metaphor — and it must be labeled as metaphor.

---

## Receipts you can check today

This repo includes audit artifacts under `reports/` that let a skeptical reader verify the scope:

- A processing snapshot documenting chromosomes 20/21/22 and 958 genes processed.
- A validation metadata file reporting: $n=8$, $N=1000$ permutations, 76 evaluated patterns, 18 survivors under block-shuffle nulls.
- A passports table with 198 mapped rows (193 unique loci), including stability labels and BH q-values.

These are *measurements in a representational space*. They are not claims about biology.

---

## Why this matters

When you treat “recurrence” as a testable statistical object (instead of a narrative hook), you get something useful:

- a prioritized shortlist for downstream experiments,
- a paper that survives reviewer skepticism,
- and a toolchain where future improvements (better nulls, confounder controls) are measurable.

---

## What comes next

Stage 2 is not “bigger claims.” It’s stronger controls:

- explicit repeat/segdup overlap,
- mappability controls,
- ablations on tokenization,
- and replication across datasets.

Follow the development of Bio‑Kernel on GitHub: https://github.com/sirfederick/bio-kernel
