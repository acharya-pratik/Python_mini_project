import pandas as pd
import os

def chunk_data(input_file="data/raw/healthcare.csv", output_dir="data/simulation/chunks", chunk_size=250):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Read the header and data
    df = pd.read_csv(input_file)
    num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size > 0 else 0)
    
    print(f"Splitting {len(df)} rows into {num_chunks} chunks of {chunk_size} rows each...")
    
    for i in range(num_chunks):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size
        chunk = df.iloc[start_idx:end_idx]
        chunk.to_csv(f"{output_dir}/chunk_{i:03d}.csv", index=False)
    
    print(f"✅ Successfully created {num_chunks} chunks in {output_dir}")

if __name__ == "__main__":
    chunk_data()
