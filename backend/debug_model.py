from transformers import pipeline, AutoConfig
import sys

print("Python version:", sys.version)
try:
    print("Loading pipeline...")
    pipe = pipeline("image-classification", model="dima806/ai_vs_real_image_detection")
    print("Success!")
except Exception as e:
    print("Error loading pipeline:")
    print(e)

try:
    print("Attempting to load config manually...")
    config = AutoConfig.from_pretrained("dima806/ai_vs_real_image_detection")
    print("Config loaded:", config)
except Exception as e:
    print("Error loading config:")
    print(e)
