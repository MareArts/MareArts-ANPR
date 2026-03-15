# MareArts ANPR - FAQ

**Last Updated:** March 4, 2026

---

## General Questions

### Q: What types of licenses are available?
**A:** We offer licenses in three durations:

- **Monthly licenses** - Renewable monthly
- **Yearly licenses** - Renewable annually
- **Lifetime licenses** - No expiration, use indefinitely

All licenses include multi-region support (Korea, Europe+, North America, China, Universal) and latest model updates.

### Q: How does license renewal work?
**A:**
- **Monthly and Yearly licenses:** Must be renewed before expiration. We'll send new keys before your license expires, giving you time to update and avoid any service interruption. Each license includes approximately 10 extra days as a buffer.
- **Lifetime licenses:** No expiration date - use indefinitely without any renewal needed.

### Q: When will I receive my renewal key?
**A:** New license keys are sent before your current license expires, ensuring you have adequate time to update without any service interruption.

### Q: What regions are supported?
**A:** Both SDK and Mobile App support multiple regions:
- **Korea** (kor / kr) - Korean license plates
- **Europe+** (euplus / eup) - European+ plates (EU countries + additional countries)
- **North America** (na) - USA, Canada plates
- **China** (china / cn) - Chinese plates
- **Universal** (univ) - All regions (default, but choose specific region for best accuracy)

### Q: What happens if your service discontinues?
**A:** We're committed to our users. If our service ever discontinues, we will either:
- Open-source the code, or
- Provide lifetime licenses to all active users

This ensures you'll always have access to the software you've invested in.

### Q: What is your refund policy?
**A:** We offer a full refund guarantee with the following conditions:
- **Before serial key delivery:** Full refund available if requested before your serial key is sent to your email
- **After serial key delivery:** Refunds cannot be processed once the serial key has been issued and sent to your email
- **Why this policy?** Serial keys work completely offline and cannot be remotely deactivated once issued, making it impossible to revoke access after delivery

### Q: How can I test before purchasing?
**A:** We strongly encourage testing before purchase:
- Use our **free test API** to evaluate the SDK capabilities
- Try our **live test website** to see the software in action
- Try the **Mobile App** with **100 free scans per day** (no license required)

---

## SDK / Python Library

### Q: Do I need an internet connection to use the SDK?
**A:** No, the SDK works fully offline once set up. You only need an internet connection for:
- Initial model download during setup
- Checking for and downloading model updates (automatic when available)
- Without internet, the SDK will use your existing downloaded model

### Q: Can I use my SDK license on multiple computers?
**A:** Yes! SDK licenses have **no limits on the number of computers**. You can use them on multiple computers simultaneously.

### Q: What does an SDK license include?
**A:** All SDK licenses include:
- Access to V14 Detector and V15 OCR models (V14 OCR also supported)
- Multi-backend support (CPU, CUDA, DirectML)
- Multi-region support (kor, euplus, na, china, univ)
- Unlimited computers - no device limits
- Latest model updates

### Q: What model versions are available?
**A:** Current version (v3.8.0) includes:
- **V14 Detector** - Detection models (finds plates in images)
- **V15 OCR** - Latest text recognition (reads plate text) - Recommended
- **V14 OCR** - Backward compatible text recognition

**V15 OCR improvements:**
- 6.7-7.4% better accuracy vs V14 (FP32)
- Major NA improvement (70.34% -> 96.86% in `small_fp32`)
- Strong real-time performance in CUDA benchmark
- Better multi-line plate handling
- INT8 models available (75% smaller files)

### Q: Should I use V14 or V15 OCR?
**A:** **V15 OCR is recommended** for all new projects:
- 6.7-7.4% better accuracy across FP32 models
- Stronger cross-region robustness (especially NA)
- INT8 option for edge/mobile deployment
- Better multi-line plate handling

**Use V14 OCR** only if:
- Maintaining existing production systems
- Need proven stability or maximum FPS on your current hardware
- Already optimized for V14

**Migration is easy:** Just change `ma_anpr_ocr_v14` to `ma_anpr_ocr_v15` or use `ma_anpr_ocr(version='v15')`.

[See detailed comparison →](v14-vs-v15-comparison.md)

### Q: Do I need to specify a region?
**A:** Region parameter is optional with `univ` (universal) as default. However, **we strongly recommend choosing a specific region** (kr, eup, na, or cn) for best accuracy. Only use `univ` when the region is truly unknown or mixed.

### Q: Can I change the region after initialization?
**A:** Yes! Use the `set_region()` method to dynamically switch regions without creating new OCR instances:

```python
# Initialize once (V15 OCR recommended)
from marearts_anpr import ma_anpr_ocr
ocr = ma_anpr_ocr("large_fp32", "kor", user, key, sig, version='v15')

# Switch regions as needed (both short and full codes work)
ocr.set_region('euplus')  # Switch to Europe+ (or 'eup')
ocr.set_region('na')      # Switch to North America
ocr.set_region('china')   # Switch to China (or 'cn')
ocr.set_region('kor')     # Switch to Korea (or 'kr')
```

This saves significant memory - one instance (~180 MB) instead of multiple instances (~540 MB for 3 regions).

### Q: When should I use set_region() vs multiple OCR instances?
**A:**
- **Use `set_region()`**: When processing different regions sequentially, or in memory-constrained environments
- **Use multiple instances**: When processing multiple regions concurrently in different threads
- **Note**: `set_region()` is not thread-safe. For multi-threaded applications, create separate OCR instances per thread.

---

## Mobile App (iOS)

### Q: How many devices can I use with one license?
**A:** Mobile App licenses are **1 license = 1 device** by default. This is different from the SDK, which allows unlimited computers.

### Q: Can I transfer my license to a new device?
**A:** Yes, you can transfer by logging in on the new device and syncing your data from the cloud. However, we recommend keeping device changes to a minimum for sync reliability.

### Q: Is there a free trial?
**A:** Yes! The Mobile App offers **100 free scans per day** without a license. This lets you fully evaluate the app's detection quality before purchasing.

### Q: Does the app work offline?
**A:** The app works partially offline - all AI detection runs on-device so plate recognition works without internet. However, **we recommend staying online** for cloud sync, webhook delivery, and the best overall experience.

### Q: What is cloud sync?
**A:** Cloud sync keeps your rules and detection records synchronized across sessions. Cloud sync is **available to licensed users only**.

### Q: What is the Cloud Scan API?
**A:** The Cloud Scan API lets you send images for plate detection via the cloud. It's available to all users (free and licensed) with a shared daily limit of 1,000 calls across all users.

### Q: What webhook integrations are supported?
**A:** Currently supported:
- **Discord** - Send detection results directly to Discord channels
- **Custom server** - Build your own webhook receiver ([see example code](https://github.com/MareArts/MareArts-ANPR/blob/main/example_code/webhook_receiver.py))

More SNS integrations (Slack, etc.) will be added in future updates.

### Q: What platforms are supported?
**A:** **iOS and Android** are both supported.

### Q: Where can I download the app?
**A:** Search **"marearts anpr"** in the App Store or Google Play, or download directly:

[![Download on App Store](https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg)](https://apps.apple.com/app/marearts-anpr/id6753904859)
[![Get it on Google Play](https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png)](https://play.google.com/store/apps/details?id=com.marearts.anpr)

[Read the full Mobile App Guide →](https://github.com/MareArts/MareArts-ANPR/blob/main/mobile_app/README.md)

---

## Technical Support

### Q: How can I get help with setup or licensing issues?
**A:** Contact our support team at [hello@marearts.com](mailto:hello@marearts.com) with any questions about setup, licensing, or technical issues.