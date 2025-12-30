from transformers import pipeline, AutoConfig, ViTForImageClassification, AutoModelForImageClassification
import torch

model_id = "dima806/ai_vs_real_image_detection"

print(f"Attempting to load {model_id}...")

# Attempt 1: AutoModel with trust_remote_code
try:
    print("\n--- Attempt 1: AutoModelForImageClassification (trust_remote_code=True) ---")
    model = AutoModelForImageClassification.from_pretrained(model_id, trust_remote_code=True)
    print("Success with AutoModel!")
    print("Config model_type:", model.config.model_type)
except Exception as e:
    print("Failed Attempt 1:", e)

# Attempt 2: Explicit ViT
try:
    print("\n--- Attempt 2: ViTForImageClassification ---")
    model = ViTForImageClassification.from_pretrained(model_id)
    print("Success with ViTForImageClassification!")
except Exception as e:
    print("Failed Attempt 2:", e)

# Attempt 3: Inspect Config (if possible)
try:
    print("\n--- Attempt 3: AutoConfig ---")
    config = AutoConfig.from_pretrained(model_id)
    print("Config loaded:", config)
except Exception as e:
    print("Failed Attempt 3:", e)
