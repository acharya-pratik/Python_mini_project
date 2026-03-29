import time
import os
import subprocess
import glob

def run_automation(chunk_dir="data/simulation/chunks", interval=60):
    """
    Main Demo Driver. Ingests data and updates reports every 60s.
    """
    chunks = sorted(glob.glob(f"{chunk_dir}/chunk_*.csv"))
    if not chunks:
        # Try generating chunks if none exist
        print("📦 Chunks not found. Generating...")
        try:
            subprocess.run(["python3", "-m", "member1.chunk_data"], check=True)
            chunks = sorted(glob.glob(f"{chunk_dir}/chunk_*.csv"))
        except Exception as e:
            print(f"❌ Failed to generate chunks: {e}")
            return

    print(f"🚀 Simulation Active (Total: {len(chunks)} chunks, Interval: {interval}s)")
    
    chunk_idx = 0
    while True:
        chunk_file = chunks[chunk_idx]
        print(f"\n--- 🕒 [{time.strftime('%H:%M:%S')}] Chunk {chunk_idx + 1}/{len(chunks)} ---")
        
        # 1. Run ETL (Optimized with skip_schema after first run)
        try:
            skip_flag = ["--skip-schema"] if chunk_idx > 0 else []
            subprocess.run(["python3", "-m", "member1.run_ETL", "--file", chunk_file] + skip_flag, check=True)
        except Exception as e:
            print(f"❌ ETL Fail: {e}")
            time.sleep(5)
            continue
            
        # 2. Update Live Analytics Report
        try:
            subprocess.run(["python3", "member1/generate_report.py", chunk_file], check=True)
            print("📈 Real-time AI Analysis Updated")
        except Exception as e:
            print(f"❌ Report Fail: {e}")

        # Cycle chunks
        chunk_idx = (chunk_idx + 1) % len(chunks)
        
        print(f"😴 Waiting for next ingestion cycle...")
        time.sleep(interval)

if __name__ == "__main__":
    run_automation()
