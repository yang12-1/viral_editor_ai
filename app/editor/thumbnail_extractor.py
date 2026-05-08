from pathlib import Path

import cv2
import numpy as np


def _colorfulness(frame):
    b, g, r = cv2.split(frame.astype("float"))
    rg = np.absolute(r - g)
    yb = np.absolute(0.5 * (r + g) - b)
    return float(np.sqrt(np.std(rg) ** 2 + np.std(yb) ** 2) + 0.3 * np.sqrt(np.mean(rg) ** 2 + np.mean(yb) ** 2))


def _frame_score(frame):
    resized = cv2.resize(frame, (360, 640))
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = np.mean(gray)
    saturation = np.mean(cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)[:, :, 1])
    color = _colorfulness(resized)

    center = resized[160:480, 70:290]
    center_edges = cv2.Canny(cv2.cvtColor(center, cv2.COLOR_BGR2GRAY), 80, 160).mean()

    return float(
        0.35 * min(sharpness / 500.0, 1.0)
        + 0.25 * min(color / 80.0, 1.0)
        + 0.20 * min(saturation / 120.0, 1.0)
        + 0.15 * min(center_edges / 40.0, 1.0)
        + 0.05 * (1.0 - abs(brightness - 135.0) / 135.0)
    )


def extract_hook_frame(video_path, output_path="output/hook_thumbnail.jpg", max_scan_seconds=45, sample_per_second=2):
    """Save the most visually punchy early frame for Shorts thumbnail/hook use."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video: {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    max_frames = min(total_frames, int(max_scan_seconds * fps)) if total_frames else int(max_scan_seconds * fps)
    step = max(1, int(fps / sample_per_second))

    best_score = -1.0
    best_frame = None
    best_time = 0.0

    frame_idx = 0
    while frame_idx < max_frames:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if not ok:
            break

        score = _frame_score(frame)
        if score > best_score:
            best_score = score
            best_frame = frame
            best_time = frame_idx / fps

        frame_idx += step

    cap.release()

    if best_frame is None:
        raise RuntimeError("No frame could be sampled for thumbnail extraction.")

    cv2.imwrite(str(output_path), best_frame)
    return {"path": str(output_path), "timestamp": best_time, "score": best_score}
