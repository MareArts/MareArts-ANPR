"""MareArts ANPR — Batch Folder Processing

Scan a folder of images, detect plates, and export results to CSV/JSON.
Uses the Python SDK directly (no server needed).
"""
import csv
import json
import os
import sys
import time
from pathlib import Path

from marearts_anpr import (
    ma_anpr_detector_v16,
    ma_anpr_ocr_v16,
    marearts_anpr_from_image_file,
)

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


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


def scan_images(folder: str) -> list:
    folder = Path(folder)
    if not folder.is_dir():
        print(f"ERROR: {folder} is not a directory")
        sys.exit(1)
    images = sorted(
        p for p in folder.iterdir()
        if p.suffix.lower() in EXTENSIONS
    )
    return images


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch ANPR on a folder of images")
    parser.add_argument("folder", help="Path to image folder")
    parser.add_argument("--region", default="univ", help="OCR region (default: univ)")
    parser.add_argument("--output", default=None, help="Output file (.csv or .json)")
    parser.add_argument("--recursive", action="store_true", help="Scan subfolders")
    args = parser.parse_args()

    user_name, serial_key, signature = load_credentials()
    if not all([user_name, serial_key, signature]):
        print("No credentials. Run: ma-anpr config")
        sys.exit(1)

    if args.recursive:
        images = sorted(
            p for p in Path(args.folder).rglob("*")
            if p.suffix.lower() in EXTENSIONS
        )
    else:
        images = scan_images(args.folder)

    if not images:
        print(f"No images found in {args.folder}")
        sys.exit(0)

    print(f"Found {len(images)} image(s) in {args.folder}")
    print(f"Region: {args.region}")
    print("Loading models...")

    detector = ma_anpr_detector_v16(
        "640p_fp32", user_name, serial_key, signature, backend="auto",
    )
    ocr = ma_anpr_ocr_v16(
        "fp32", args.region, user_name, serial_key, signature, backend="auto",
    )

    print("Processing...\n")
    all_results = []
    total_plates = 0
    t_start = time.time()

    for i, img_path in enumerate(images, 1):
        t0 = time.time()
        try:
            result = marearts_anpr_from_image_file(detector, ocr, str(img_path))
            elapsed = time.time() - t0
            plates = result.get("results", [])
            total_plates += len(plates)
            plate_texts = [p["ocr"] for p in plates if p.get("ocr")]

            print(f"  [{i}/{len(images)}] {img_path.name}: "
                  f"{plate_texts or '(no plates)'}  ({elapsed:.2f}s)")

            for p in plates:
                all_results.append({
                    "file": str(img_path.name),
                    "plate": p.get("ocr", ""),
                    "ocr_conf": p.get("ocr_conf", 0),
                    "det_conf": p.get("ltrb_conf", 0),
                    "bbox": p.get("ltrb", []),
                })
        except Exception as e:
            print(f"  [{i}/{len(images)}] {img_path.name}: ERROR {e}")

    total_time = time.time() - t_start
    print(f"\nDone: {len(images)} images, {total_plates} plates, {total_time:.1f}s total")

    if args.output:
        out = Path(args.output)
        if out.suffix == ".csv":
            with open(out, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["file", "plate", "ocr_conf", "det_conf", "bbox"])
                writer.writeheader()
                writer.writerows(all_results)
            print(f"Saved: {out} ({len(all_results)} rows)")
        else:
            with open(out, "w") as f:
                json.dump(all_results, f, indent=2)
            print(f"Saved: {out} ({len(all_results)} entries)")


if __name__ == "__main__":
    main()
