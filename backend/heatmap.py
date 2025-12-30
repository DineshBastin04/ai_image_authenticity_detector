import cv2
import numpy as np

def generate_heatmap(image: np.ndarray):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    heat = cv2.resize(gray, (image.shape[1], image.shape[0]))
    heat = cv2.applyColorMap(heat, cv2.COLORMAP_JET)
    overlay = cv2.addWeighted(image, 0.7, heat, 0.3, 0)
    return overlay
