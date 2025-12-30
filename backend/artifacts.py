import cv2
import numpy as np

def detect_artifacts(image: np.ndarray):
    artifacts = []

    # check for unnatural symmetry (simple free heuristic)
    h, w = image.shape[:2]
    left = image[:, :w//2]
    right = cv2.flip(image[:, w//2:], 1)
    diff = cv2.absdiff(left, right)
    score = np.mean(diff)
    if score < 10:
        artifacts.append("Unnatural face/image symmetry")

    # check for text irregularities using contour density
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 300:
        artifacts.append("Possible AI-generated text or noise patterns")

    # check for blurry eye-like regions (Laplacian variance)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    var = np.var(lap)
    if var < 50:
        artifacts.append("Unnatural blur or low detail texture")

    return artifacts
