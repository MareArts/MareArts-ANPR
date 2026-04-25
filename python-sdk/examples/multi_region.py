"""MareArts ANPR — Multi-Region Detection

Compare OCR results across different regions on the same image.
Shows how to switch regions without reloading the model.
"""
import os
import sys
from pathlib import Path

from marearts_anpr import (
    ma_anpr_detector_v16,
    ma_anpr_ocr_v16,
    marearts_anpr_from_image_file,
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
        print("No credentials. Run: ma-anpr config")
        sys.exit(1)

    SAMPLE = Path(__file__).resolve().parent.parent.parent / "sample_images"

    test_images = {
        "EU plate": (SAMPLE / "eu-a.jpg", ["eup", "eu", "de", "univ"]),
        "KR plate": (SAMPLE / "kr-a.jpg", ["kr", "asia", "univ"]),
    }

    print("Loading models...")
    detector = ma_anpr_detector_v16(
        "640p_fp32", user_name, serial_key, signature, backend="auto",
    )
    ocr = ma_anpr_ocr_v16(
        "fp32", "univ", user_name, serial_key, signature, backend="auto",
    )

    for label, (img_path, regions) in test_images.items():
        if not img_path.exists():
            print(f"\nSkipping {label} ({img_path.name} not found)")
            continue

        print(f"\n{'=' * 50}")
        print(f"  {label}: {img_path.name}")
        print(f"{'=' * 50}")
        print(f"  {'Region':<12} {'Plate':<20} {'Conf':>6}")
        print(f"  {'-'*12} {'-'*20} {'-'*6}")

        for region in regions:
            ocr.set_region(region)
            result = marearts_anpr_from_image_file(detector, ocr, str(img_path))
            for plate in result["results"]:
                text = plate.get("ocr", "(none)")
                conf = plate.get("ocr_conf", 0)
                print(f"  {region:<12} {text:<20} {conf:>5}%")
            if not result["results"]:
                print(f"  {region:<12} {'(no detection)':<20}")

    # ── Show available regions ──
    print(f"\n{'=' * 50}")
    print("  Available Regions")
    print(f"{'=' * 50}")
    print(f"  Current: {ocr.current_region}")
    print(f"  All:     {', '.join(ocr.available_regions)}")

    print("\nDone.")
