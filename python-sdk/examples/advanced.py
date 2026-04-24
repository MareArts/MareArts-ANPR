"""MareArts ANPR V16 - Advanced Example

Manual pipeline, input formats, region switching, backend comparison.
Demonstrates: load models once, detect many (loop pattern).
"""
import os
import time
from pathlib import Path
import numpy as np
from PIL import Image
from marearts_anpr import (
    ma_anpr_detector_v16,
    ma_anpr_ocr_v16,
    marearts_anpr_from_image_file,
    marearts_anpr_from_pil,
    marearts_anpr_from_cv2,
)


def load_credentials():
    user = os.getenv("MAREARTS_ANPR_USERNAME")
    key = os.getenv("MAREARTS_ANPR_SERIAL_KEY")
    sig = os.getenv("MAREARTS_ANPR_SIGNATURE")
    if not all([user, key, sig]):
        config_file = Path.home() / ".marearts" / ".marearts_env"
        if config_file.exists():
            for line in open(config_file):
                if "USERNAME=" in line:
                    user = line.split("=", 1)[1].strip().strip('"')
                elif "SERIAL_KEY=" in line:
                    key = line.split("=", 1)[1].strip().strip('"')
                elif "SIGNATURE=" in line:
                    sig = line.split("=", 1)[1].strip().strip('"')
    return user, key, sig


if __name__ == "__main__":
    user_name, serial_key, signature = load_credentials()
    if not all([user_name, serial_key, signature]):
        print("No credentials found. Run: ma-anpr config")
        exit(1)

    # ── Load models ONCE (slow, ~seconds) ──
    detector = ma_anpr_detector_v16(
        "640p_fp32", user_name, serial_key, signature,
        backend="auto", conf_thres=0.25, iou_thres=0.5,
    )
    ocr = ma_anpr_ocr_v16(
        "fp32", "eup", user_name, serial_key, signature, backend="auto",
    )

    # ── Manual detection + OCR pipeline with timing ──
    print("=== Manual Pipeline ===")
    img = Image.open("../../sample_images/eu-a.jpg").convert("RGB")
    img_bgr = np.array(img)[:, :, ::-1].copy()

    t0 = time.time()
    detections = detector.detector(img_bgr)
    det_time = time.time() - t0
    print("Detection: %.4fs, found %d plate(s)" % (det_time, len(detections)))

    for i, box in enumerate(detections):
        bbox = box.get("bbox", box.get("box"))
        l, t, r, b = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
        crop_bgr = img_bgr[t:b, l:r]
        if crop_bgr.size == 0:
            continue

        crop_pil = Image.fromarray(crop_bgr[:, :, ::-1])
        t0 = time.time()
        text, conf = ocr.predict(crop_pil)
        elapsed = time.time() - t0
        print("  Plate %d: %s (%s%%) @ [%d,%d,%d,%d] - %.4fs" % (
            i + 1, text, conf, l, t, r, b, elapsed))

    # ── Input format comparison ──
    print("\n=== Input Formats ===")
    result = marearts_anpr_from_image_file(detector, ocr, "../../sample_images/eu-a.jpg")
    print("  from_image_file: %s" % [r["ocr"] for r in result["results"]])

    result = marearts_anpr_from_pil(detector, ocr, img)
    print("  from_pil:        %s" % [r["ocr"] for r in result["results"]])

    result = marearts_anpr_from_cv2(detector, ocr, img_bgr)
    print("  from_cv2:        %s" % [r["ocr"] for r in result["results"]])

    # ── Region switching ──
    print("\n=== Region Switching ===")
    for region in ["univ", "eup", "kr", "na"]:
        ocr.set_region(region)
        result = marearts_anpr_from_image_file(detector, ocr, "../../sample_images/eu-a.jpg")
        plates = [r["ocr"] for r in result["results"]]
        print("  [%s] %s" % (region, plates))

    # ── Load once, detect many (loop pattern) ──
    print("\n=== Load Once, Detect Many ===")
    ocr.set_region("univ")
    images = [
        "../../sample_images/eu-a.jpg",
    ]
    for img_path in images:
        t0 = time.time()
        result = marearts_anpr_from_image_file(detector, ocr, img_path)
        elapsed = time.time() - t0
        plates = [r["ocr"] for r in result["results"] if r.get("ocr")]
        print("  %s: %s (%.3fs)" % (img_path, plates or "(no plates)", elapsed))

    # ── Backend comparison ──
    print("\n=== Backend Check ===")
    for backend in ["cpu", "cuda"]:
        try:
            test_det = ma_anpr_detector_v16(
                "640p_fp32", user_name, serial_key, signature, backend=backend,
            )
            t0 = time.time()
            test_det.detector(img_bgr)
            elapsed = time.time() - t0
            print("  %s: %.4fs" % (backend, elapsed))
        except Exception as e:
            print("  %s: not available (%s)" % (backend, e))

    print("\nDone.")
