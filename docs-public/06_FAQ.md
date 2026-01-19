# Frequently Asked Questions (FAQ)

## 1. Is Bio-Kernel claiming to have "solved" the genome?
No. Bio-Kernel is a **statistical prioritization tool**. It identifies patterns that are statistically unexpected under specific null models. While these patterns are interesting candidates for biological study, Bio-Kernel does not claim to know their biological function or mechanism.

## 2. Why is the core engine not open source (yet)?
The core engine is currently under internal audit for security and performance optimization. We are releasing the methodology, documentation, and results first to engage with the community and validate our statistical approach.

## 3. How can I reproduce the results?
You can use the aggregated metrics in `03_OBSERVABILITY` and the methodology in `02_METHOD` to understand how the scores were calculated. We are working on a "Lite" version of the scanner that can be run on individual genes.

## 4. What are "Survivors"?
"Survivors" are patterns that persist even after we shuffle the genomic data 1,000 times using a structure-preserving block-shuffle. This means the pattern is not an artifact of simple nucleotide counts or local dinucleotide bias.

## 5. Can I contribute?
Yes! We are looking for:
- Peer review of our statistical null models.
- Better "Block-Shuffle" algorithms to control for genomic confounders.
- Integration with external biological databases for annotation support.

## 6. How do I contact the team?
Please open an issue on the GitHub repository or contact the lead author via the links provided in the [Overview](00_OVERVIEW.md).

---
*License: Refer to the LICENSE file in the root directory.*
