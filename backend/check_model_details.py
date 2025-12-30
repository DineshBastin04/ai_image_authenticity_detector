from huggingface_hub import hf_hub_download
import json
import sys
from transformers import AutoModelForImageClassification, AutoConfig

print("Python:", sys.version)

# 1. Inspect Ateeqq config
try:
    print("\n--- Inspecting Ateeqq config ---")
    config_path = hf_hub_download(repo_id="Ateeqq/ai-vs-human-image-detector", filename="config.json")
    with open(config_path, 'r') as f:
        config = json.load(f)
    print("Model Type:", config.get("model_type"))
    print("Architectures:", config.get("architectures"))
except Exception as e:
    print("Error inspecting Ateeqq:", e)

# 2. Test PrithivMLmods model
print("\n--- Testing PrithivMLmods/Deep-Fake-Detector-v2-Model ---")
try:
    model_id = "prithivMLmods/Deep-Fake-Detector-v2-Model"
    model = AutoModelForImageClassification.from_pretrained(model_id)
    print("PrithivMLmods loaded successfully!")
    print("Labels:", model.config.id2label)
except Exception as e:
    print("Error loading PrithivMLmods:", e)
