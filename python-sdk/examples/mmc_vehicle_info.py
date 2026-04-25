"""MareArts ANPR — MMC Vehicle Info (Cloud AI)

Demonstrates all 7 MMC features: make, model, color, type,
front/rear view, plate nation, and cloud plate OCR cross-check.

Requires internet. Falls back gracefully when offline or quota exhausted.
"""
import os
import sys
from pathlib import Path

from marearts_anpr import (
    ma_anpr_detector_v16,
    ma_anpr_ocr_v16,
    ma_anpr_mmc,
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


def print_mmc_detail(plate):
    """Print all 7 MMC features for a single plate."""
    fields = [
        ("Make",   "mmc_make",          "mmc_make_conf"),
        ("Model",  "mmc_model",         "mmc_model_conf"),
        ("Color",  "mmc_color",         "mmc_color_conf"),
        ("Type",   "mmc_type",          "mmc_type_conf"),
        ("Side",   "mmc_vehicle_side",  "mmc_vehicle_side_conf"),
        ("Nation", "mmc_plate_nation",  "mmc_plate_nation_conf"),
        ("Plate",  "mmc_plate",         "mmc_plate_conf"),
    ]
    for label, key, conf_key in fields:
        val = plate.get(key)
        conf = plate.get(conf_key)
        if val is not None:
            print(f"    {label:8s}: {val}  ({conf})")


if __name__ == "__main__":
    user_name, serial_key, signature = load_credentials()
    if not all([user_name, serial_key, signature]):
        print("No credentials. Run: ma-anpr config")
        sys.exit(1)

    SAMPLE = Path(__file__).resolve().parent.parent.parent / "sample_images"
    images = [SAMPLE / "eu-a.jpg", SAMPLE / "kr-a.jpg"]

    print("Loading models...")
    detector = ma_anpr_detector_v16(
        "640p_fp32", user_name, serial_key, signature, backend="auto",
    )
    ocr = ma_anpr_ocr_v16(
        "fp32", "univ", user_name, serial_key, signature, backend="auto",
    )
    mmc = ma_anpr_mmc(user_name, serial_key, signature)

    for img_path in images:
        if not img_path.exists():
            print(f"\nSkipping {img_path.name} (not found)")
            continue

        print(f"\n{'=' * 50}")
        print(f"  {img_path.name}")
        print(f"{'=' * 50}")

        result = marearts_anpr_from_image_file(detector, ocr, str(img_path), mmc)

        if result.get("mmc_error"):
            print(f"  MMC error: {result['mmc_error']}")
            print("  (local ANPR results still available)")

        for plate in result["results"]:
            local_ocr = plate.get("ocr", "")
            local_conf = plate.get("ocr_conf", 0)
            cloud_ocr = plate.get("mmc_plate", "")
            cloud_conf = plate.get("mmc_plate_conf")

            print(f"\n  Plate: {local_ocr}  (local OCR {local_conf}%)")
            print(f"  BBox:  {plate.get('ltrb')}  (det {plate.get('ltrb_conf')}%)")

            if plate.get("mmc_make"):
                print("  MMC vehicle info:")
                print_mmc_detail(plate)

                if cloud_ocr and cloud_ocr != local_ocr:
                    print(f"\n  OCR cross-check:")
                    print(f"    Local:  {local_ocr} ({local_conf}%)")
                    print(f"    Cloud:  {cloud_ocr} ({cloud_conf})")
                    better = cloud_ocr if (cloud_conf or 0) > local_conf else local_ocr
                    print(f"    Best:   {better}")
            else:
                print("  (no MMC data — offline or quota exhausted)")

        print(f"\n  Timing: det={result['ltrb_proc_sec']:.3f}s  ocr={result['ocr_proc_sec']:.3f}s")
        if "mmc_request_sec" in result:
            print(f"  MMC:    model={result.get('mmc_model_sec', 0):.3f}s  "
                  f"request={result['mmc_request_sec']:.3f}s")
            print(f"  Quota:  {result.get('mmc_calls_today', '?')}/{result.get('mmc_daily_limit', '?')} today")

    print("\nDone.")
