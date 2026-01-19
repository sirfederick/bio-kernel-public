"""
Bio-Batch-Orchestrator: Mass Chromosomal Binarizer
==================================================

Orchestrates the process of downloading and binarizing an entire chromosome.
It fetches genes, sequences, and structural annotations from Ensembl and 
generates .bioelf files.

Usage: python chromosome_binarizer.py --chrom 21 --limit 5
"""

import argparse
import sys
import time
from pathlib import Path
import logging
import concurrent.futures
import json
import os
import platform
import subprocess
from typing import Any

import requests

# Add root to sys.path
sys.path.append(str(Path(__file__).resolve().parents[0]))

from kernel_quantum.shared.bio_connector import get_connector
from kernel_unknown_engine.reverse_engineering.reverse_engineering import ReverseEngineering
from kernel_unknown_engine.reverse_engineering.entropy_analyzer import EntropyAnalyzer
from kernel_unknown_engine.reverse_docs.ghidra_adapter import GhidraAdapter
from kernel_quantum.shared.logging_utils import get_logger

LOGGER = get_logger("chrom_binarizer")

SCHEMA_VERSION = "v1"
METRICS_VERSION = "v1"
TOKENIZER_ID = "bp_char_tokenizer"
TOKENIZER_SCHEMA_VERSION = "v1"


def _safe_div(numer: float, denom: float) -> float:
    if denom == 0:
        return 0.0
    return numer / denom


def _try_get_git_commit() -> str | None:
    try:
        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            value = (res.stdout or "").strip()
            return value or None
    except Exception:
        return None
    return None


def _percentile(sorted_values: list[float], p: float) -> float:
    """Return percentile p in [0, 100] for a pre-sorted list."""
    if not sorted_values:
        return 0.0
    if p <= 0:
        return float(sorted_values[0])
    if p >= 100:
        return float(sorted_values[-1])
    k = (len(sorted_values) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(sorted_values) - 1)
    if f == c:
        return float(sorted_values[f])
    d0 = sorted_values[f] * (c - k)
    d1 = sorted_values[c] * (k - f)
    return float(d0 + d1)

def get_chromosome_length(chrom: str, connector) -> int:
    """Get length of chromosome from Ensembl or Fallback."""
    # Hardcoded known lengths to avoid API dependency/failures
    KNOWN_LENGTHS = {
        "1": 248956422, "2": 242193529, "3": 198295559, "4": 190214555,
        "5": 181538258, "6": 170805979, "7": 159345973, "8": 145138636,
        "9": 138394717, "10": 133797422, "11": 135086622, "12": 133275309,
        "13": 114364328, "14": 107043718, "15": 101991189, "16": 90338345,
        "17": 83257441, "18": 80373285, "19": 58617616, "20": 64444167,
        "21": 46709983, "22": 50818468, "X": 156040895, "Y": 57227415
    }
    
    if str(chrom) in KNOWN_LENGTHS:
         return KNOWN_LENGTHS[str(chrom)]

    url = f"{connector.ENSEMBL_URL}/info/assembly/homo_sapiens/{chrom}"
    try:
        resp = requests.get(url, headers={"Content-Type": "application/json"})
        if resp.status_code == 200:
            return resp.json().get("length", 46709983) 
        return 46709983
    except:
        return 46709983

def fetch_gene_chunk(chrom, start, end, connector):
    """Fetch a single chunk of genes to be used in parallel execution."""
    url = f"{connector.ENSEMBL_URL}/overlap/region/human/{chrom}:{start}-{end}"
    params = {"feature": "gene", "content-type": "application/json"}
    found_genes = []
    
    # Use Robust Connector with Retry Logic
    data = connector.fetch_json(url, params=params)
    if data:
        for g in data:
            if g.get('biotype') == 'protein_coding':
                found_genes.append(g['id'])
    return found_genes

def get_genes_in_chromosome(chrom: str, connector) -> list[str]:
    """
    Fetch list of gene IDs by iterating chromosome in chunks (Parallelized).
    """
    print(f"[*] Obtaining layout for Chr{chrom}...")
    length = get_chromosome_length(chrom, connector)
    print(f"    Length: {length} bps")
    
    chunk_size = 5_000_000 # 5MB chunks
    genes = set()
    
    starts = range(1, length, chunk_size)
    tasks = []
    
    # REDUCED WORKERS: From 10 to 2 to prevent "Read Timeout" congestion
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        for start in starts:
            end = min(start + chunk_size - 1, length)
            tasks.append(executor.submit(fetch_gene_chunk, chrom, start, end, connector))
            
        for future in concurrent.futures.as_completed(tasks):
            result = future.result()
            for g_id in result:
                genes.add(g_id)
                
    # Determinism: stable ordering so limits/selectors are reproducible
    return sorted(genes)

def process_single_gene(gene_id, chrom, bin_root, connector, reveng, entropy_scanner, ghidra, fetch_metadata: bool = False):
    """Worker function to process a single gene."""
    try:
        # A. Descargar Secuencia (SOLO LO ESENCIAL)
        seq = connector.fetch_ensembl_sequence(gene_id)
        if not seq:
            return {"gene_id": gene_id, "success": False, "error": "no_sequence"}
            
        # [OPTIMIZATION] Skip secondary API calls to prevent blocking
        struct_data = None  # connector.fetch_gene_structure(gene_id)
        metadata = None
        if fetch_metadata:
            try:
                metadata = connector.fetch_gene_metadata(gene_id)
            except Exception:
                metadata = None
        
        # D. Project Dark Matter: Entropy Analysis (Local CPU calculation, safe to keep)
        dark_matter_hits = entropy_scanner.scan_regions(seq)
        
        # E. De-cloaking: SKIP Vista API calls for now
        decloaked_features = []
        # if dark_matter_hits: ... (Skipped optimization)

        # F. Generar .bioelf y Analisis
        gene_dir = bin_root / gene_id
        gene_dir.mkdir(exist_ok=True)
        output_path = gene_dir / f"{gene_id}.bioelf"
        report_path = gene_dir / "gene_report.json"
        dark_matter_path = gene_dir / "dark_matter_entropy.json"
        
        # 1. .bioelf Generation
        data = {"gene": gene_id, "sequence": seq}
        # generate_bioelf handles None annotations gracefully (defaults to raw processing)
        reveng.generate_bioelf(data, output_path, annotations=struct_data)
        
        # 2. Ghidra Decompilation (Local)
        ghidra_path = gene_dir / "ghidra_analysis.json"
        
        instructions = ghidra.analyze_binary(output_path)
        if instructions:
            with open(ghidra_path, "w", encoding="utf-8") as f:
                json.dump(instructions, f, indent=2)

        # Collect metrics
        bp_len = len(seq)
        bioelf_bytes = 0
        try:
            bioelf_bytes = output_path.stat().st_size
        except Exception:
            bioelf_bytes = 0
        anomalies = len(dark_matter_hits) if dark_matter_hits else 0
        opcodes = 0
        if isinstance(instructions, list):
            opcodes = len(instructions)
        elif isinstance(instructions, dict):
            # Some adapters may return a dict with an instruction list
            opcodes = len(instructions.get("instructions", []) or [])

        gene_symbol = None
        if isinstance(metadata, dict):
            gene_symbol = metadata.get("display_name") or metadata.get("symbol")

        # 3. Reporte JSON (always emit lightweight QC-friendly report)
        report_obj: dict[str, Any]
        if isinstance(metadata, dict) and metadata:
            report_obj = dict(metadata)
        else:
            report_obj = {}

        report_obj.setdefault("id", gene_id)
        report_obj.setdefault("display_name", gene_symbol or "unknown")
        report_obj["schema_version"] = SCHEMA_VERSION
        report_obj["tokenizer_id"] = TOKENIZER_ID
        report_obj["tokenizer_schema_version"] = TOKENIZER_SCHEMA_VERSION
        report_obj["chrom"] = str(chrom)
        report_obj["bp"] = len(seq)
        report_obj["bioelf_bytes"] = bioelf_bytes
        report_obj["opcodes"] = opcodes
        report_obj["anomalies"] = anomalies

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_obj, f, indent=2, ensure_ascii=False)
        
        # 4. Reporte de Entropía (Dark DNA)
        if dark_matter_hits:
            with open(dark_matter_path, "w", encoding="utf-8") as f:
                json.dump(dark_matter_hits, f, indent=2)
        
        # Tokens: explicit definition (bp-as-token) for now
        tokens_emitted = bp_len
        kb = bp_len / 1000.0
        per_1k_tokens = tokens_emitted / 1000.0

        return {
            "schema_version": SCHEMA_VERSION,
            "metrics_version": METRICS_VERSION,
            "tokenizer_id": TOKENIZER_ID,
            "tokenizer_schema_version": TOKENIZER_SCHEMA_VERSION,
            "gene_id": gene_id,
            "success": True,
            "chrom": str(chrom),
            "bp": bp_len,
            "tokens": tokens_emitted,
            "bioelf_bytes": bioelf_bytes,
            "anomalies": anomalies,
            "opcodes": opcodes,
            "anomalies_per_kb": _safe_div(anomalies, kb),
            "opcodes_per_kb": _safe_div(opcodes, kb),
            "anomalies_per_1k_tokens": _safe_div(anomalies, per_1k_tokens),
            "opcodes_per_1k_tokens": _safe_div(opcodes, per_1k_tokens),
            "gene_symbol": gene_symbol,
        }
    except Exception as e:
        return {"gene_id": gene_id, "success": False, "error": str(e)}

def process_chromosome(
    chrom: str,
    limit: int = 0,
    fetch_metadata: bool = False,
    max_workers: int = 2,
):
    """
    Process entire chromosome concurrently.
    limit: 0 means NO LIMIT (process all).
    """
    logs_dir = Path("logs")
    logs_dir.mkdir(parents=True, exist_ok=True)
    print(f"--- Iniciando Binarización Masiva OPTIMIZADA (GOD MODE): Cromosoma {chrom} ---")

    run_header = {
        "schema_version": SCHEMA_VERSION,
        "tokenizer_id": TOKENIZER_ID,
        "tokenizer_schema_version": TOKENIZER_SCHEMA_VERSION,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "chrom": str(chrom),
        "limit": int(limit),
        "max_workers": int(max_workers),
        "fetch_metadata": bool(fetch_metadata),
        "tokenizer": "bp_char_tokenizer_v1",
        "bioelf_version": getattr(ReverseEngineering, "BIOELF_VERSION", None),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "git_commit": _try_get_git_commit(),
    }
    print("[RUN_HEADER] " + json.dumps(run_header, ensure_ascii=False))
    
    connector = get_connector()
    reveng = ReverseEngineering()
    entropy_scanner = EntropyAnalyzer(window_size=128) 
    ghidra = GhidraAdapter()
    
    # 1. Obtener lista de genes
    print(f"[*] Obteniendo lista de genes para Chr{chrom}...")
    gene_ids = get_genes_in_chromosome(chrom, connector)
    print(f"[+] Encontrados {len(gene_ids)} genes candidatos (filtrado protein_coding).")
    
    # Apply limit if specified
    if limit > 0:
        gene_ids = gene_ids[:limit]
        print(f"[!] Limiting execution to first {limit} genes.")
        
    # --- OPTIMIZATION: Filter out already processed genes ---
    bin_root = Path(f"bin/chr{chrom}")
    bin_root.mkdir(parents=True, exist_ok=True)

    metrics_path = bin_root / "gene_metrics.ndjson"
    
    genes_to_process = []
    for gid in gene_ids:
        bioelf_path = bin_root / gid / f"{gid}.bioelf"
        if not bioelf_path.exists():
            genes_to_process.append(gid)
            
    skipped_count = len(gene_ids) - len(genes_to_process)
    if skipped_count > 0:
        print(f"[INFO] Skipping {skipped_count} already processed genes. {len(genes_to_process)} remaining.")
    
    if len(genes_to_process) == 0:
        print(f"[✓] Chr{chrom} fully processed. Exiting binarizer.")
        return

    # 2. Iterar y procesar en paralelo
    print(f"[*] Launching ThreadPool for {len(genes_to_process)} genes...")
    
    successful_count = 0
    failed_count = 0
    processed_metrics: list[dict[str, Any]] = []

    # REDUCED WORKERS by default.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_gene = {
            executor.submit(process_single_gene, gid, chrom, bin_root, connector, reveng, entropy_scanner, ghidra, fetch_metadata): gid 
            for gid in genes_to_process
        }
        
        completed = 0
        total = len(genes_to_process)
        
        for future in concurrent.futures.as_completed(future_to_gene):
            gid = future_to_gene[future]
            try:
                result = future.result()
                if isinstance(result, dict) and result.get("success") is True:
                    successful_count += 1
                    processed_metrics.append(result)
                    with metrics_path.open("a", encoding="utf-8") as fh:
                        fh.write(json.dumps(result, ensure_ascii=False) + "\n")

                    # Print reviewer-safe normalized metrics line
                    print(
                        "[GENE_METRICS] "
                        + json.dumps(
                            {
                                "schema_version": result.get("schema_version"),
                                "metrics_version": result.get("metrics_version"),
                                "tokenizer_id": result.get("tokenizer_id"),
                                "tokenizer_schema_version": result.get("tokenizer_schema_version"),
                                "gene_id": result.get("gene_id"),
                                "bp": result.get("bp"),
                                "tokens": result.get("tokens"),
                                "bioelf_bytes": result.get("bioelf_bytes"),
                                "opcodes": result.get("opcodes"),
                                "anomalies": result.get("anomalies"),
                                "opcodes_per_kb": round(float(result.get("opcodes_per_kb", 0.0)), 4),
                                "anomalies_per_kb": round(float(result.get("anomalies_per_kb", 0.0)), 4),
                                "opcodes_per_1k_tokens": round(float(result.get("opcodes_per_1k_tokens", 0.0)), 4),
                                "anomalies_per_1k_tokens": round(float(result.get("anomalies_per_1k_tokens", 0.0)), 4),
                                "gene_symbol": result.get("gene_symbol"),
                            },
                            ensure_ascii=False,
                        )
                    )
                else:
                    failed_count += 1
                    err = result.get("error") if isinstance(result, dict) else "unknown_error"
                    print(f"[GENE_FAIL] {gid} :: {err}")
            except Exception as exc:
                print(f'{gid} generated an exception: {exc}')
                failed_count += 1
            
            completed += 1
            if completed % 10 == 0:
                print(f"    - Progress: {completed}/{total} ({successful_count} OK)")

    # Per-chromosome snapshot
    opcodes_per_kb_vals = sorted([float(m.get("opcodes_per_kb", 0.0)) for m in processed_metrics])
    anomalies_per_kb_vals = sorted([float(m.get("anomalies_per_kb", 0.0)) for m in processed_metrics])
    processed_bp_total = sum(int(m.get("bp", 0) or 0) for m in processed_metrics)
    expected_chrom_bp = int(get_chromosome_length(chrom, connector))
    unknown_display_name_count = sum(
        1 for m in processed_metrics if str(m.get("gene_symbol") or "").strip().lower() in {"", "unknown"}
    )

    snapshot = {
        "schema_version": SCHEMA_VERSION,
        "snapshot_version": "v1",
        "tokenizer_id": TOKENIZER_ID,
        "tokenizer_schema_version": TOKENIZER_SCHEMA_VERSION,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "chrom": str(chrom),
        "genes_total": int(len(gene_ids)),
        "genes_skipped_existing": int(skipped_count),
        "genes_attempted": int(len(genes_to_process)),
        "genes_ok": int(successful_count),
        "genes_failed": int(failed_count),
        "unknown_display_name_count": int(unknown_display_name_count),
        "expected_chrom_bp": expected_chrom_bp,
        "processed_gene_bp_total": int(processed_bp_total),
        # NOTE: This is a throughput-like ratio (sum of gene seq bp / chrom bp), not true genomic coverage.
        "throughput_ratio": round(_safe_div(float(processed_bp_total), float(expected_chrom_bp)), 6),
        "normalization": {
            "tokenizer": "bp_char_tokenizer_v1",
            "opcodes_per_kb": {
                "p50": _percentile(opcodes_per_kb_vals, 50),
                "p90": _percentile(opcodes_per_kb_vals, 90),
                "p99": _percentile(opcodes_per_kb_vals, 99),
            },
            "anomalies_per_kb": {
                "p50": _percentile(anomalies_per_kb_vals, 50),
                "p90": _percentile(anomalies_per_kb_vals, 90),
                "p99": _percentile(anomalies_per_kb_vals, 99),
            },
        },
        "artifacts": {
            "gene_metrics": str(metrics_path),
        },
        "run_header": run_header,
    }
    snapshot_path = bin_root / "chromosome_snapshot.json"
    snapshot_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")
    print("[CHROM_SNAPSHOT] " + json.dumps(snapshot, ensure_ascii=False))

    print(f"[SUCCESS] Processed {successful_count}/{len(gene_ids)} genes from Chr{chrom}. Failed: {failed_count}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--chrom", type=str, default="21")
    parser.add_argument("--limit", type=int, default=0) # Default 0 = Unlimited
    parser.add_argument("--fetch-metadata", action="store_true", help="Fetch Ensembl gene metadata (slower).")
    parser.add_argument("--max-workers", type=int, default=2, help="ThreadPool max workers (default: 2).")
    args = parser.parse_args()
    
    process_chromosome(args.chrom, args.limit, fetch_metadata=args.fetch_metadata, max_workers=args.max_workers)
