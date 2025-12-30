from huggingface_hub import list_repo_files
import sys

models = [
    "Ateeqq/ai-vs-human-image-detector",
    "prithivMLmods/Deep-Fake-Detector-v2-Model",
    "umm-maybe/AI-image-detector"
]

print("Python version:", sys.version)

for model_id in models:
    print(f"\n--- Files in {model_id} ---")
    try:
        files = list_repo_files(model_id)
        for f in files:
            print(f)
    except Exception as e:
        print(f"Error listing files: {e}")
