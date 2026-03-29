import os
import pandas as pd
import joblib

def test_data_processed():
    """Check if clean_data.csv exists and has data."""
    path = "data/processed/clean_data.csv"
    assert os.path.exists(path), f"❌ {path} not found!"
    df = pd.read_csv(path)
    assert not df.empty, "❌ clean_data.csv is empty!"
    print(f"✅ Data processed successfully ({len(df)} rows)")

def test_models_exist():
    """Check if ML models are saved."""
    models = [
        "member3_ml/models/high_billing_model.pkl",
        "member3_ml/models/treatment_success_model.pkl",
        "member3_ml/models/length_of_stay_model.pkl"
    ]
    for model_path in models:
        assert os.path.exists(model_path), f"❌ Model {model_path} not found!"
        # Test loading a model
        model = joblib.load(model_path)
        assert model is not None, f"❌ Failed to load {model_path}"
    print("✅ All ML models found and loadable")

def test_db_populated():
    """Verify patients table is not empty in MySQL."""
    from config.db_config import get_connection
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")
    count = cursor.fetchone()[0]
    conn.close()
    assert count > 0, "❌ Database table 'patients' is empty!"
    print(f"✅ Database check passed ({count} patients found)")

if __name__ == "__main__":
    print("🧪 Running Project Tests...")
    try:
        test_data_processed()
        test_models_exist()
        test_db_populated()
        print("\n🎉 All tests passed!")
    except AssertionError as e:
        print(f"\n{e}")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
