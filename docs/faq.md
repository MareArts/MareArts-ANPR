# Software Licensing FAQ

**Last Updated:** February 4, 2026

---

## General Questions

### Q: Do I need an internet connection to use the software?
**A:** No, the software works fully offline once set up. You only need an internet connection for:
- Initial model download during setup
- Checking for and downloading model updates (automatic when available)
- Without internet, the SDK will use your existing downloaded model

### Q: Can I use my license on multiple computers?
**A:** Yes! All licenses have no limits on the number of computers. You can use them on multiple computers simultaneously.

## License Types & Renewal

### Q: What types of licenses are available?
**A:** We offer licenses in three durations:

- **Monthly licenses** - Renewable monthly
- **Yearly licenses** - Renewable annually
- **Lifetime licenses** - No expiration, use indefinitely

All licenses include:
- Access to V14 Detector and V15 OCR models (V14 OCR also supported)
- Multi-backend support (CPU, CUDA, DirectML)
- Multi-region support (kor, euplus, na, china, univ)
- Unlimited computers - no device limits
- Latest model updates

### Q: How does license renewal work?
**A:** 
- **Monthly and Yearly licenses:** Must be renewed before expiration. We'll send new keys before your license expires, giving you time to update and avoid any service interruption. Each license includes approximately 10 extra days as a buffer.
- **Lifetime licenses:** No expiration date - use indefinitely without any renewal needed.

### Q: When will I receive my renewal key?
**A:** New license keys are sent before your current license expires, ensuring you have adequate time to update without any service interruption.

## Service Continuity

### Q: What happens if your service discontinues?
**A:** We're committed to our users. If our service ever discontinues, we will either:
- Open-source the code, or
- Provide lifetime licenses to all active users

This ensures you'll always have access to the software you've invested in.

## Refund Policy

### Q: What is your refund policy?
**A:** We offer a full refund guarantee with the following conditions:
- **Before serial key delivery:** Full refund available if requested before your serial key is sent to your email
- **After serial key delivery:** Refunds cannot be processed once the serial key has been issued and sent to your email
- **Why this policy?** Serial keys work completely offline and cannot be remotely deactivated once issued, making it impossible to revoke access after delivery

### Q: How can I test before purchasing?
**A:** We strongly encourage testing before purchase:
- Use our **free test API** to evaluate the software capabilities
- Try our **live test website** to see the software in action
- These testing options ensure the software meets your needs before committing to a purchase

## Models & Features

### Q: What model versions are available?
**A:** Current version (v3.8.0) includes:
- **V14 Detector** - Detection models (finds plates in images)
- **V15 OCR** - Latest text recognition (reads plate text) ⭐ Recommended
- **V14 OCR** - Backward compatible text recognition

**V15 OCR improvements:**
- 2.8-3.7% better accuracy
- 6-11% faster inference
- Better multi-line plate handling
- INT8 models available (75% smaller files)

### Q: What regions are supported?
**A:** All models support multiple regions:
- **kor** (or kr) - Korean license plates
- **euplus** (or eup) - European+ plates (EU countries + additional countries)
- **na** - North American plates (USA, Canada)
- **china** (or cn) - Chinese plates
- **univ** - Universal (all regions) - default, but choose specific region for best accuracy

**Note:** Both short codes (kr, eup, cn) and full names (kor, euplus, china) work

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

### Q: Should I use V14 or V15 OCR?
**A:** **V15 OCR is recommended** for all new projects:
- 2.8-3.7% better accuracy
- 6-11% faster inference  
- Better multi-line plate handling
- INT8 models available (75% smaller)

**Use V14 OCR** only if:
- Maintaining existing production systems
- Need proven stability
- Already optimized for V14

**Migration is easy:** Just change `ma_anpr_ocr_v14` to `ma_anpr_ocr_v15` or use `ma_anpr_ocr(version='v15')`.

[See detailed comparison →](v14-vs-v15-comparison.md)

## Technical Support

### Q: How can I get help with setup or licensing issues?
**A:** Contact our support team at [hello@marearts.com](mailto:hello@marearts.com) with any questions about setup, licensing, or technical issues.