"""MareArts ANPR V16 - Basic Example: All 6 Combinations

Shows: load models once, then detect in a loop.
MMC uses the same credentials (no separate secret needed).
"""
import os
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


def print_result(result):
    for r in result["results"]:
        parts = []
        if r.get("ocr"):
            parts.append("ocr=%s (%s%%)" % (r["ocr"], r["ocr_conf"]))
        parts.append("ltrb=%s (%s%%)" % (r["ltrb"], r["ltrb_conf"]))
        if r.get("mmc_make"):
            parts.append("make=%s model=%s color=%s type=%s side=%s nation=%s plate=%s" % (
                r.get("mmc_make", ""), r.get("mmc_model", ""),
                r.get("mmc_color", ""), r.get("mmc_type", ""),
                r.get("mmc_vehicle_side", ""), r.get("mmc_plate_nation", ""),
                r.get("mmc_plate", "")))
        print("  " + " | ".join(parts))
    print("  timing: det=%.2fs ocr=%.2fs" % (
        result["ltrb_proc_sec"], result["ocr_proc_sec"]))
    if "mmc_request_sec" in result:
        print("  mmc: %.2fs (calls today: %s/%s)" % (
            result["mmc_request_sec"],
            result.get("mmc_calls_today", "?"),
            result.get("mmc_daily_limit", "?")))
    if "mmc_error" in result:
        print("  mmc error: %s" % result["mmc_error"])


if __name__ == "__main__":
    user_name, serial_key, signature = load_credentials()
    if not all([user_name, serial_key, signature]):
        print("No credentials found. Run: ma-anpr config")
        exit(1)

    IMG = "../../sample_images/eu-a.jpg"

    # ── Load models ONCE (slow, ~seconds) ──
    detector = ma_anpr_detector_v16(
        "640p_fp32", user_name, serial_key, signature, backend="cpu",
    )
    ocr = ma_anpr_ocr_v16(
        "fp32", "univ", user_name, serial_key, signature, backend="cpu",
    )
    mmc_client = ma_anpr_mmc(user_name, serial_key, signature)

    # ── Detect (fast, ~milliseconds per call) ──

    # 1. Detection Only: (detector, image)
    print("=== 1. Detection Only ===")
    result = marearts_anpr_from_image_file(detector, IMG)
    print_result(result)

    # 2. OCR Only: (ocr, image)
    print("\n=== 2. OCR Only (full image) ===")
    result = marearts_anpr_from_image_file(ocr, IMG)
    print_result(result)

    # 3. Detection + OCR: (detector, ocr, image)
    print("\n=== 3. Detection + OCR ===")
    result = marearts_anpr_from_image_file(detector, ocr, IMG)
    print_result(result)

    # 4. Detection + MMC: (detector, image, mmc)
    print("\n=== 4. Detection + MMC ===")
    result = marearts_anpr_from_image_file(detector, IMG, mmc_client)
    print_result(result)

    # 5. OCR + MMC: (ocr, image, mmc)
    print("\n=== 5. OCR + MMC ===")
    result = marearts_anpr_from_image_file(ocr, IMG, mmc_client)
    print_result(result)

    # 6. Detection + OCR + MMC: (detector, ocr, image, mmc)
    print("\n=== 6. Detection + OCR + MMC ===")
    result = marearts_anpr_from_image_file(detector, ocr, IMG, mmc_client)
    print_result(result)

    # ── Loop example: load once, detect many ──
    print("\n=== Loop: load once, detect many ===")
    images = ["../../sample_images/eu-a.jpg"]  # add more images here
    for img_path in images:
        result = marearts_anpr_from_image_file(detector, ocr, img_path)
        plates = [r["ocr"] for r in result["results"] if r.get("ocr")]
        print("  %s: %s" % (img_path, plates or "(no plates)"))

    print("\nDone.")
