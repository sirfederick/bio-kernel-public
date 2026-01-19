
# Claims Guide (Marketing + Reviewer-Safe)

Purpose: let us write strong, compelling posts **without** drifting into mechanistic/ontological claims.

This file is a contract: every claim must map to a reproducible artifact. If it cannot be traced to `reports/` outputs, it belongs in **narrative** and must be labeled.

---

## 1) One-sentence “safe default” (copy/paste)

Use this line (or close variants) everywhere:

> Bio‑Kernel prioritizes recurrent signatures under a defined representation (tokenization + null tests); functional interpretation is out of scope and requires orthogonal validation.

---

## 2) Claim levels (what you’re allowed to say)

### Level A — **Artifact facts** (strongest, always safe)

You may claim counts and parameters if they are written in `reports/`.

Examples (backed by existing artifacts in this repo):
- “This workspace processed chromosomes 20/21/22 and 958 genes.”
- “The validation run evaluated 76 distinct 8-grams and reported 18 survivor patterns under block-shuffle nulls.”
- “Passports contain 198 mapped rows (193 unique loci) with GC%, entropy, stability labels, and q-values.”

### Level B — **Statistical outcomes** (safe if you name the null + universe)

You may claim “exceeds null” only if you include:
- the null model name (e.g., `block_shuffle`),
- permutations N,
- the evaluated universe size,
- and whether you’re discussing **p-values** vs **BH q-values**.

Allowed phrasing:
- “A subset remained significant under a local-structure-preserving block-shuffle null (N=1000), within the evaluated universe.”

Required caution:
- If min $q\approx 0.101$, you must not claim FDR $< 0.05$.

### Level C — **Interpretation / hypotheses** (must be labeled)

Anything about “what it means biologically” must be labeled as narrative.

Required prefixes:
- `[NARRATIVE]` or `[HYPOTHESIS]`.
- If it is LLM-assisted and not derivable from reports, use `[SIMULATED HYPOTHESIS]`.

---

## 3) Mandatory “Receipts Box” template (for every post)

Paste this block near the end of any public post:

**Evidence (reproducible artifacts):**
- `reports/GENOME_PROCESS_SUMMARY_20260117.md` (coverage + artifact counts)
- `reports/SURVIVOR_RUN_METADATA.json` (parameters: n=8, permutations=1000, evaluated_patterns=76, survivors_found=18)
- `reports/SURVIVOR_PATTERNS.md` and `reports/SENSITIVITY_REPORT.md` (survivors + block-size sensitivity)
- `reports/PASSPORTS.csv` (mapped loci table)

**Non-claims:**
- No mechanism/causality/function claims.
- LLM text is narrative unless backed by the artifacts above.

---

## 4) Forbidden claims (do not publish)

Do not claim or imply:
- “We decoded the operating system of life.”
- “System calls / kernel handshakes” as literal biology.
- “First ever”, “proof”, “irrefutable”, “radiography of the species”, “Creator’s code”.
- “Complete human genome processed” (unless the reports show it).
- “Dark DNA is not junk” as a scientific conclusion.

---

## 5) Metaphors policy (allowed only with a safety line)

Metaphors are allowed **only** if you do both:
1) Explicitly label the metaphor (“Think of it like…”), and
2) Immediately restate the literal claim (“…we observed recurring signatures under a defined tokenization and tested them against a null model.”)

Preferred metaphor: “scanner/triage pipeline”.

---

## 6) Language guidance

Prefer:
- “signature”, “recurrence”, “representation”, “null model”, “permutation test”, “evaluated universe”, “artifact”, “triage”.

Avoid:
- “handshake”, “system call”, “kernel space”, “decompiler”, “root access”, “debugger for life”.

---

## 7) Pre-publish checklist

- Every numeric claim has a filename in `reports/`.
- You never state or imply mechanism.
- You distinguish p-values vs BH q-values.
- You state the evaluated universe size when discussing significance.
