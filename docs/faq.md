# Software Licensing FAQ

**Last Updated:** November 7, 2025

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
- Access to V14 models with digital signature
- Multi-backend support (CPU, CUDA, DirectML)
- Multi-region support (kr, eup, na, cn, univ)
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

## V14 Models & Features

### Q: What are V14 models?
**A:** V14 models are our latest generation featuring:
- Improved accuracy and performance
- Multi-backend support (CPU, CUDA, DirectML)
- Multi-region support with region selection
- Optimized for production use

### Q: What regions are supported?
**A:** V14 models support multiple regions:
- **kr** - Korean license plates (best for Korean)
- **eup** - European+ plates (EU countries + Albania, Andorra, Bosnia & Herzegovina, Liechtenstein, Monaco, Montenegro, North Macedonia, Norway, San Marino, Serbia, Switzerland, UK, Indonesia)
- **na** - North American plates (USA, Canada)
- **cn** - Chinese plates
- **univ** - Universal (all regions) - default, but choose specific region for best accuracy

### Q: Do I need to specify a region?
**A:** Region parameter is optional with `univ` (universal) as default. However, **we strongly recommend choosing a specific region** (kr, eup, na, or cn) for best accuracy. Only use `univ` when the region is truly unknown or mixed.

### Q: Can I change the region after initialization? (>3.7.0)
**A:** Yes! Use the `set_region()` method to dynamically switch regions without creating new OCR instances:

```python
# Initialize once
ocr = ma_anpr_ocr_v14("large_fp32", "kr", user, key, sig)

# Switch regions as needed
ocr.set_region('eup')  # Switch to Europe+
ocr.set_region('na')   # Switch to North America
ocr.set_region('cn')   # Switch to China
```

This saves significant memory - one instance (~180 MB) instead of multiple instances (~540 MB for 3 regions).

### Q: When should I use set_region() vs multiple OCR instances?
**A:** 
- **Use `set_region()`**: When processing different regions sequentially, or in memory-constrained environments
- **Use multiple instances**: When processing multiple regions concurrently in different threads
- **Note**: `set_region()` is not thread-safe. For multi-threaded applications, create separate OCR instances per thread.

## Technical Support

### Q: How can I get help with setup or licensing issues?
**A:** Contact our support team at [hello@marearts.com](mailto:hello@marearts.com) with any questions about setup, licensing, or technical issues.