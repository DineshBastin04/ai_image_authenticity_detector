from transformers import pipeline, AutoModelForImageClassification, AutoImageProcessor
import sys

print("Python version:", sys.version)

MODEL_CANDIDATES = [
    "Ateeqq/ai-vs-human-image-detector",
    "umm-maybe/AI-image-detector",
    "dima806/ai_vs_real_image_detection"
]

for model_name in MODEL_CANDIDATES:
    try:
        print(f"\nAttempting to load model: {model_name}")
        model = AutoModelForImageClassification.from_pretrained(model_name, trust_remote_code=True)
        processor = AutoImageProcessor.from_pretrained(model_name, trust_remote_code=True)
        pipe = pipeline("image-classification", model=model, feature_extractor=processor)
        print(f"Successfully loaded {model_name}!")
        break
    except Exception as e:
        print(f"Failed to load {model_name}: {e}")
        import traceback
        traceback.print_exc()

print("Debug script finished.")
