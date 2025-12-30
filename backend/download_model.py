from huggingface_hub import hf_hub_download
import os
import shutil

model_id = "umm-maybe/AI-image-detector"
local_dir = "models/umm-maybe"
files_to_download = ["config.json", "pytorch_model.bin", "preprocessor_config.json"]

print(f"Downloading {model_id} to {local_dir}...")

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

for filename in files_to_download:
    try:
        print(f"Downloading {filename}...")
        path = hf_hub_download(repo_id=model_id, filename=filename, local_dir=local_dir)
        print(f"Saved to {path}")
    except Exception as e:
        print(f"Error downloading {filename}: {e}")

print("Download complete.")
