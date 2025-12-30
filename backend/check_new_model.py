from transformers import pipeline

model_id = "Ateeqq/ai-vs-human-image-detector"
print(f"Loading {model_id}...")
try:
    pipe = pipeline("image-classification", model=model_id)
    print("Model loaded successfully!")
    print("Labels:", pipe.model.config.id2label)
except Exception as e:
    print(f"Error loading {model_id}: {e}")
