import pickle
import os
from db.queries import insert_alert, block_ip
from capture.feature_extractor import packet_to_ml_vector
import pandas as pd

MODEL_PATH = os.path.join(os.path.dirname(__file__), "../models/model.pkl")
META_PATH  = os.path.join(os.path.dirname(__file__), "../models/model_meta.pkl")

class MLEngine:
    def __init__(self):
        self.model    = None
        self.encoders = {}
        self._load()

    def _load(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(META_PATH):
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)
            with open(META_PATH, "rb") as f:
                meta = pickle.load(f)
                self.encoders = meta["encoders"]
            print("[ML Engine] Model + encoders loaded (UNSW-NB15).")
        else:
            print("[ML Engine] WARNING: model.pkl not found. Run: python -m models.train")

    def analyze(self, features: dict):
        if not self.model:
            return
        
        # Skip localhost traffic
        if features["src_ip"] in {"127.0.0.1", "::1"}:
            return
        
        try:
            vector = packet_to_ml_vector(features, self.encoders)
            # wrapping the vector in a DataFrame with proper column names before prediction
            df = pd.DataFrame(
                [vector], 
                columns=["proto","service","state","dur","sbytes","dbytes","sttl","dttl","sloss","dloss"]
                )
            proba = self.model.predict_proba(df)[0]
            attack_prob = float(proba[1])   # convert numpy.float64 → plain Python float

            if attack_prob > 0.75:
                src_ip  = features["src_ip"]
                details = f"ML confidence: {attack_prob:.2%} (UNSW-NB15 model)"
                print(f"[ML ALERT] Anomaly from {src_ip} — {details}")
                insert_alert(src_ip, "ml_anomaly", confidence=attack_prob, details=details)
                block_ip(src_ip, reason="Auto-blocked: ML anomaly")
        except Exception as e:
            print(f"[ML Engine] Prediction error: {e}")