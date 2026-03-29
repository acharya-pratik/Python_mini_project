import os
import subprocess
import sys

def run_step(name, command):
    print(f"\n--- Running Step: {name} ---")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"❌ Step '{name}' failed with exit code {result.returncode}")
        sys.exit(result.returncode)
    print(f"✅ Step '{name}' completed successfully")

def main():
    print("🏥 Healthcare Analytics Project Main Runner")

    # Step 1: Run ETL
    run_step("ETL Pipeline", "python3 -m member1.run_ETL")

    # Step 2: ML Training
    run_step("ML Training - High Billing", "python3 -m member3.train_high_billing")
    run_step("ML Training - Treatment Success", "python3 -m member3.train_treatment")
    run_step("ML Training - Length of Stay", "python3 -m member3.train_length_of_stay")

    # Step 3: Evaluation
    run_step("ML Evaluation", "python3 -m member3.evaluate")

    print("\n🚀 All steps completed successfully!")
    print("\nTo start the dashboard, run: streamlit run member4/app.py")
    print("To start the scheduler, run: python3 -m member2.scheduler")

if __name__ == "__main__":
    main()
