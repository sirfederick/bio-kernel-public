# Marketing Screenshots Plan (4 portals)

This file maps existing screenshots in `../Imagenes/` to each portal note so the articles stay complementary (no repeated story, different angle per platform).

## General rules (to keep it reviewer-safe)

- Prefer **artifacts/screens** over “mystical” visuals: dashboards, logs, summary tables, Trident validation outputs.
- Avoid implying mechanism: captions must describe **what is shown** (counts, signatures, gating), not “what it means biologically.”
- Max **3–5 screenshots** per note (excluding hero/cover image generated separately).
- Captions should include **what step of the pipeline** it represents (Ingest → Binarize → Profile → Mine → Validate → Report).

---

## Portal 1 — Dev.to / Hashnode (technical build story)

File: `docs/marketing/DEV_TO_Technical_Build.md`

Recommended screenshots:
1. `../Imagenes/sceenshot_trabajando binarice.jpg`
   - Caption idea: “Binarization running: per-gene artifacts being produced (idempotent pipeline).”
2. `../Imagenes/trident_binarization_stream.jpg`
   - Caption idea: “Stream view of binarization / profiling throughput.”
3. `../Imagenes/trident_super_orchestrator_matrix.jpg`
   - Caption idea: “Orchestration view: concurrent processing + retries + idempotency.”
4. `../Imagenes/procesamiento-completo_01.jpg` (or `procesameinto-completo_02.jpg`)
   - Caption idea: “Processing summary screen (what completed, what remains).”
5. `../Imagenes/trident_null_hypothesis_proof.jpg`
   - Caption idea: “Statistical gate output: rejecting structured nulls (when enabled).”

---

## Portal 2 — HackerNoon (reverse-engineering vibe, receipts-first)

File: `docs/marketing/HACKERNOON_Cyberpunk_Story.md`

Recommended screenshots:
1. `../Imagenes/ghidra_acoples_trident_genomic.jpg`
   - Caption idea: “Token-space coupling visualization (representation output; not a biological mechanism claim).”
2. `../Imagenes/trident_deep_pattern_discovery.jpg`
   - Caption idea: “Pattern mining: recurring n-grams detected under the representation.”
3. `../Imagenes/coples_detectados_cromosomas_all.jpg`
   - Caption idea: “Cross-chromosome recurrence overview (signatures, not mechanism).”
4. `../Imagenes/tridente_puzzle_ananlyse.jpg`
   - Caption idea: “Trident puzzle analyzer view (neighborhood context grouping).”

Optional (only if caption is toned down):
- `../Imagenes/trident_kernel_handshake_log2.jpg`
  - Use caption like: “Log excerpt: signature detection event (terminology is metaphorical).”

---

## Portal 3 — LinkedIn (product + collaboration call)

File: `docs/marketing/LINKEDIN_Innovation_Pitch.md`

Recommended screenshots:
1. `../Imagenes/loggin_geenral con menu.jpg`
   - Caption idea: “Bio‑Kernel dashboard: live view of processing + metrics endpoints.”
2. `../Imagenes/resumen_final.jpg`
   - Caption idea: “Executive outputs: what exists today (reports + catalogs).”
3. `../Imagenes/00_Check-list_preLaunch.jpg`
   - Caption idea: “Reproducibility checklist: what we lock down per run.”

Optional:
- `../Imagenes/01_Launch.jpg` (for a “launch moment” post)

---

## Portal 4 — Medium / Substack (Spanish, visionary but bounded)

File: `docs/marketing/MEDIUM_SUBSTACK_Visionary_Manifesto.md`

Recommended screenshots:
1. `../Imagenes/inicio de sitema.jpg` (or `inicio de sitema2.jpg`)
   - Caption idea: “The instrument: the system view at start (pipeline, not claims).”
2. `../Imagenes/trident_null_hypothesis_proof.jpg`
   - Caption idea: “Evidence boundary: statistical gating output (what we can defend).”
3. `../Imagenes/trident_deep_pattern_discovery.jpg`
   - Caption idea: “Recurring signatures: what the scanner surfaces for downstream study.”
4. `../Imagenes/resumen_final.jpg`
   - Caption idea: “Artifacts: reports and catalogs that can be audited.”

---

## Notes on consistency

- Use the **same 1-sentence disclaimer** everywhere:
  - “Bio‑Kernel prioritizes recurrent signatures under a defined representation; functional interpretation is out of scope and requires orthogonal validation.”
- Avoid using `intelligence_reports/*.json` as screenshots/evidence. If referenced, label as **LLM-assisted narrative**.
