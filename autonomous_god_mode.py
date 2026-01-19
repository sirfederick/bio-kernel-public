
import time
import os
import sys
from pathlib import Path

# Ensure root is in path
sys.path.append(str(Path(__file__).resolve().parent))

from kernel_quantum.main import Orchestrator
from audit_flows.genome_status_dashboard import generate_dashboard_md

def main():
    print("🔱 BIO-KERNEL: GOD MODE ACTIVATED 🔱")
    print("Mega-Brain Motor Unificador en marcha...")
    
    # Set necessary environment variables
    os.environ["PYTHONPATH"] = "."
    
    orch = Orchestrator()
    cycle = 1
    
    try:
        while True:
            print(f"\n--- INICIANDO CICLO MAESTRO DE INTELIGENCIA #{cycle} ---")
            
            # 1. Pipeline Execution (PARALLEL MODE: Multithreaded Chromosome Processing)
            orch.run_all(mode="parallel")
            
            # 2. Update Dashboard MD
            generate_dashboard_md()
            
            print(f"--- CICLO #{cycle} COMPLETADO. DURMIENDO PARA RECARGA DE ENERGÍA SINAÁPTICA... ---")
            cycle += 1
            time.sleep(60) # Espera de un minuto entre ciclos "GOD"
            
    except KeyboardInterrupt:
        print("\n[!] God Mode desactivado manualmente.")

if __name__ == "__main__":
    main()
