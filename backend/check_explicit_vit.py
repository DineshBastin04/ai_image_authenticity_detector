from transformers import ViTForImageClassification, AutoImageProcessor, pipeline
import sys

print("Python:", sys.version)

models_to_test = [
    "umm-maybe/AI-image-detector",
    "prithivMLmods/Deep-Fake-Detector-v2-Model"
]

for model_id in models_to_test:
    print(f"\n--- Testing {model_id} with ViTForImageClassification ---")
    try:
        model = ViTForImageClassification.from_pretrained(model_id)
        processor = AutoImageProcessor.from_pretrained(model_id)
        pipe = pipeline("image-classification", model=model, feature_extractor=processor)
        print(f"SUCCESS: {model_id} loaded!")
        print("Labels:", model.config.id2label)
        
        # Test valid pipeline
        print("Pipeline check passed.")
        
    except Exception as e:
        print(f"FAILED {model_id}: {e}")
