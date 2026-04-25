"""
MareArts ANPR — Full SDK Test (V16)
Just run:  python test_sdk.py
"""
import sys
import time
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

import numpy as np
from PIL import Image

# ── credentials (auto-load from ~/.marearts/.marearts_env) ─────────
def _load_creds():
    env_path = Path.home() / ".marearts" / ".marearts_env"
    if not env_path.exists():
        print(f"ERROR: {env_path} not found.")
        print("Run 'ma-anpr config' to set up credentials.")
        sys.exit(1)
    print(f"Credentials: {env_path}")
    env = {}
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if line.startswith("#") or "=" not in line:
            continue
        line = line.removeprefix("export ").strip()
        k, v = line.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    user = env.get("MAREARTS_ANPR_USERNAME", "")
    key  = env.get("MAREARTS_ANPR_SERIAL_KEY", "")
    sig  = env.get("MAREARTS_ANPR_SIGNATURE", "")
    if not user or not key:
        print(f"ERROR: MAREARTS_ANPR_USERNAME / MAREARTS_ANPR_SERIAL_KEY missing in {env_path}")
        sys.exit(1)
    return user, key, sig

USER, KEY, SIG = _load_creds()

# ── images ──────────────────────────────────────────────────────────
SAMPLE = Path(__file__).resolve().parent.parent / "sample_images"
EU_IMG = str(SAMPLE / "eu-a.jpg")
KR_IMG = str(SAMPLE / "kr-a.jpg")

# ── result tracking ─────────────────────────────────────────────────
_results = []

def _run(label, fn):
    t0 = time.perf_counter()
    try:
        detail = fn()
        dt = time.perf_counter() - t0
        _results.append(("PASS", label, f"{dt:.2f}s", detail or ""))
        print(f"  ✅ {label}  ({dt:.2f}s)  {detail or ''}")
    except Exception as e:
        dt = time.perf_counter() - t0
        _results.append(("FAIL", label, f"{dt:.2f}s", str(e)))
        print(f"  ❌ {label}  ({dt:.2f}s)  {e}")


# ====================================================================
#  1. PACKAGE & LICENSE
# ====================================================================
def test_package():
    print("\n" + "=" * 64)
    print("  1. Package & License")
    print("=" * 64)

    import marearts_anpr
    _run("import marearts_anpr", lambda: f"v{marearts_anpr.__version__}")

    from marearts_anpr import validate_user_key
    _run("validate_user_key",
         lambda: "valid" if validate_user_key(USER, KEY) else (_ for _ in ()).throw(Exception("invalid")))

    from marearts_anpr import validate_user_key_with_signature
    _run("validate_user_key_with_signature",
         lambda: "valid" if validate_user_key_with_signature(USER, KEY, SIG) else (_ for _ in ()).throw(Exception("invalid")))

    from marearts_anpr import validate_user_key_with_dates
    def _dates():
        ok, s, e = validate_user_key_with_dates(USER, KEY, SIG)
        if not ok:
            raise Exception("invalid")
        return f"{s} → {e}"
    _run("validate_user_key_with_dates", _dates)

    from marearts_anpr import ma_anpr_mmc
    def _mmc_status():
        m = ma_anpr_mmc(USER, KEY, SIG)
        img = np.array(Image.open(EU_IMG))[:, :, ::-1]
        resp = m.enrich(img, [{"ocr": "TEST", "ltrb": [0.1, 0.1, 0.9, 0.9]}])
        today = resp.get("mmc_calls_today", "?")
        limit = resp.get("mmc_daily_limit", "?")
        return f"cloud {today}/{limit} today"
    _run("MMC cloud status", _mmc_status)


# ====================================================================
#  2. DETECTOR V16
# ====================================================================
def test_detector():
    print("\n" + "=" * 64)
    print("  2. Detector V16")
    print("=" * 64)

    from marearts_anpr import ma_anpr_detector_v16

    det = None

    for model in ("640p_fp32", "640p_int8", "320p_fp32", "320p_int8"):
        def _init(m=model):
            nonlocal det
            d = ma_anpr_detector_v16(m, USER, KEY, SIG, conf_thres=0.3, iou_thres=0.5)
            if det is None:
                det = d
            return "OK"
        _run(f"ma_anpr_detector_v16  ({model})", _init)

    return det


# ====================================================================
#  3. OCR V16
# ====================================================================
def test_ocr():
    print("\n" + "=" * 64)
    print("  3. OCR V16")
    print("=" * 64)

    from marearts_anpr import ma_anpr_ocr_v16

    ocrs = {}

    for region in ("eu", "kr", "univ"):
        for model in ("fp32", "int8"):
            def _init(m=model, r=region):
                o = ma_anpr_ocr_v16(m, r, USER, KEY, SIG)
                ocrs[f"{r}_{m}"] = o
                return "OK"
            _run(f"ma_anpr_ocr_v16  ({model}, {region})", _init)

    return ocrs


# ====================================================================
#  4. INFERENCE  (file / cv2 / pil) × (EU / KR)
# ====================================================================
def test_inference(det, ocrs):
    print("\n" + "=" * 64)
    print("  4. Inference  (detect + OCR → plates)")
    print("=" * 64)

    from marearts_anpr import marearts_anpr_from_image_file, marearts_anpr_from_cv2, marearts_anpr_from_pil

    if det is None:
        _run("SKIP — no detector", lambda: (_ for _ in ()).throw(Exception("detector init failed")))
        return

    def _plates(out):
        if isinstance(out, dict):
            return [d.get("ocr", "?") for d in out.get("results", out.get("detections", []))]
        return out

    ocr_eu = ocrs.get("eu_fp32")
    ocr_kr = ocrs.get("kr_fp32")

    for region, img_path, ocr in [("eu", EU_IMG, ocr_eu), ("kr", KR_IMG, ocr_kr)]:
        if ocr is None:
            continue
        name = Path(img_path).name

        _run(f"from_image_file  ({region}) {name}",
             lambda o=ocr, p=img_path: f"plates={_plates(marearts_anpr_from_image_file(det, o, p))}")
        _run(f"from_cv2         ({region}) {name}",
             lambda o=ocr, p=img_path: f"plates={_plates(marearts_anpr_from_cv2(det, o, np.array(Image.open(p))[:, :, ::-1]))}")
        _run(f"from_pil         ({region}) {name}",
             lambda o=ocr, p=img_path: f"plates={_plates(marearts_anpr_from_pil(det, o, Image.open(p)))}")


# ====================================================================
#  5. MMC
# ====================================================================
def test_mmc(det, ocrs):
    print("\n" + "=" * 64)
    print("  5. MMC (Make/Model/Color)")
    print("=" * 64)

    from marearts_anpr import ma_anpr_mmc, marearts_anpr_from_image_file

    ocr = ocrs.get("eu_fp32")
    if det is None or ocr is None:
        _run("SKIP — no detector/OCR", lambda: (_ for _ in ()).throw(Exception("missing")))
        return

    mmc = [None]

    def _init():
        mmc[0] = ma_anpr_mmc(USER, KEY, SIG)
        return "OK"
    _run("ma_anpr_mmc init", _init)

    if mmc[0] is not None:
        def _enrich():
            result = marearts_anpr_from_image_file(det, ocr, EU_IMG, mmc=mmc[0])
            items = result.get("results", []) if isinstance(result, dict) else result
            if not items:
                return "no plates detected (image may have no plates)"
            sample = items[0]
            make = sample.get("mmc_make", "?")
            model = sample.get("mmc_model", "?")
            color = sample.get("mmc_color", "?")
            usage = result.get("mmc_calls_today", "?")
            limit = result.get("mmc_daily_limit", "?")
            return f"{make} {model} ({color})  cloud={usage}/{limit}"
        _run("mmc.enrich  eu-a.jpg", _enrich)


# ====================================================================
#  6. REGION ALIASES
# ====================================================================
def test_region_aliases():
    print("\n" + "=" * 64)
    print("  6. Region Aliases")
    print("=" * 64)

    from marearts_anpr import normalize_region_alias

    def _check():
        for alias in ("eu", "europe", "kr", "korea", "univ", "universal"):
            n = normalize_region_alias(alias)
            assert n is not None, f"normalize({alias}) failed"
        return "all aliases OK"
    _run("normalize_region_alias", _check)


# ====================================================================
#  REPORT
# ====================================================================
def report():
    print("\n" + "=" * 64)
    print("  REPORT")
    print("=" * 64)

    total = len(_results)
    passed = sum(1 for r in _results if r[0] == "PASS")
    failed = total - passed

    print(f"\n  Total : {total}")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")

    if failed:
        print("\n  Failed tests:")
        for status, label, dt, detail in _results:
            if status == "FAIL":
                print(f"    ❌ {label}  →  {detail}")
        print(f"\n  ⚠️  {failed} test(s) FAILED")
        return 1
    else:
        print(f"\n  🎉 ALL {total} TESTS PASSED")
        return 0


# ====================================================================
def main():
    print("MareArts ANPR — Full SDK Test (V16)")
    print(f"User : {USER}")
    print(f"EU   : {EU_IMG}")
    print(f"KR   : {KR_IMG}")

    test_package()
    det = test_detector()
    ocrs = test_ocr()
    test_inference(det, ocrs)
    test_mmc(det, ocrs)
    test_region_aliases()

    rc = report()
    sys.exit(rc)


if __name__ == "__main__":
    main()
