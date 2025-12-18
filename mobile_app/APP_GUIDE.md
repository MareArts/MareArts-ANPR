# MareArts ANPR - App Guide

## ⭐ Important Notice

> **✅ No Additional License Required!**  
> This app can be used as an ANPR license without any additional purchase.  
> Get your license at: [MareArts ANPR Solution](https://www.marearts.com/products/anpr)
> 
> 🔍 **Find the app by searching "marearts anpr" in the App Store**

---

## 📱 App Overview

MareArts ANPR is a professional license plate recognition app for parking management, security checkpoints, and vehicle tracking. All AI processing happens on-device for privacy and speed.

---

## 🆕 Latest Release

**Version 1.5.16 (Build 81)** - December 18, 2025

New: Year selector, custom date range, search in rules, swipe navigation, and more!

[📖 View Release Notes](https://github.com/MareArts/MareArts-ANPR/releases/latest)

---
## 📲 Download

<div align="center">

[![Download on App Store](https://developer.apple.com/assets/elements/badges/download-on-the-app-store.svg)](https://apps.apple.com/us/app/marearts-anpr/id6753904859)

**Android** - Coming Soon! 🚀

</div>

---
## 🧭 Navigation

The app has 5 main tabs at the bottom:

| Icon | Tab | Purpose |
|------|-----|---------|
| 📷 | **Scan** | Fast on-device plate scanning |
| 🕐 | **Detections** | View history and saved plates |
| ✅ | **Rules** | Manage whitelists/blacklists |
| 📊 | **Stats** | View statistics and charts |
| ⚙️ | **Settings** | Configure app behavior |

---

## 📷 1. Scan Page

<div align="center">
  <img src="scan_page.png" alt="Scan Page Screenshot" width="300"/>
</div>

**Purpose**: Fast and accurate on-device license plate detection and recognition

### Features:

**Camera View** (middle 50% of screen)
- Live camera preview
- Tap anywhere to focus
- Automatic plate detection
- Green/red bounding boxes show detected plates

**Top Bar:**
- **Flash** 🔦 - Toggle camera flash
- **Zoom** - Pinch or tap to zoom (1x-5x)
- **Camera Switch** - Front/back camera toggle

**Bottom Controls:**
- **Single Capture** (⭕) - Capture one plate
- **Continuous Mode** (🔄) - Auto-scan continuously
- **Cloud Mode** (☁️) - Send to cloud API for processing
- **Swipe left/right** - Quick switch between modes

**Status Display:**
- Shows last detected plate number
- Green/Red/Orange indicator for whitelist/blacklist status
- Confidence percentage
- Tap to view full details

**Free Trial Mode:**
- 100 scans per day
- Counter shows: "Today: X/100"
- Resets daily at midnight
- **Login for unlimited scans** (infinite usage)

---

## 🕐 2. Detections Page

**Purpose**: View all captured license plates

### Three View Modes:

#### **📋 List View** (Default)
- All captured plates in chronological order
- Grouped by date (Today, Yesterday, This Week, etc.)
- Shows: Plate number, time, location, thumbnail
- **Swipe left to right** - Opens side menu to quickly change status (whitelist/blacklist/unknown)
- **Tap** to view full details
- **Status badges**: Green (whitelist), Red (blacklist), Orange (unknown)

<div align="center">
  <img src="preview_page.png" alt="Full Preview Screenshot" width="300"/>
</div>

#### **📸 Full Preview** (tap any detection)
- Large plate image
- Plate number (tap ✏️ to edit)
- Status badge (whitelist/blacklist/unknown)
- Detection confidence
- OCR confidence
- Date & time
- GPS location & address
- **Buttons**:
  - 📋 **Copy** - Copy plate number
  - 🗑️ **Delete** - Remove from history
  - ➕ **Add to Whitelist**
  - ➖ **Add to Blacklist**

<div align="center">
  <img src="map_page.png" alt="Map View Screenshot" width="300"/>
</div>

#### **🗺️ Map View**
- Shows all plates on a map
- **Clusters** nearby detections (shows count)
- **Tap cluster** to zoom in
- **Tap marker** to see plate details
- **Top buttons**:
  - 🛰️ **Satellite/Road** toggle
  - 🏷️ **Show Labels** - Display all plate numbers
- **Search bar**: Filter by plate number
- **Header**: Shows total locations count

---

## ✅ 3. Rules Page

<div align="center">
  <img src="rules_page.png" alt="Rules Page Screenshot" width="300"/>
</div>

**Purpose**: Manage plate whitelists and blacklists

### Features:

**Whitelist** (Green)
- Allowed/approved vehicles
- Shows green badge on scan
- Plays "success" sound

**Blacklist** (Red)
- Blocked/unwanted vehicles
- Shows red badge on scan
- Plays "alert" sound

**Management:**
- **Search Bar** - Type to filter plates (real-time)
- **Tab Counter** - Shows total: "White List (200)"
- **+ Button** (bottom center) - Add new plate
- **Swipe left** to delete
- **Scroll** - Smooth iOS-style scrolling for long lists
- Type full plate number or partial (e.g., "ABC" matches "ABC-123")
- Auto-uppercase
- Tap "X" to clear search, "Done" to dismiss keyboard

**Use Cases:**
- Parking: Whitelist residents, blacklist violators
- Security: Whitelist staff, blacklist banned vehicles
- Delivery: Track known vehicles

---

## 📊 4. Stats Page

<div align="center">
  <img src="stat_page.png" alt="Stats Page Screenshot" width="300"/>
</div>

**Purpose**: View scanning statistics and trends

### Overview Section:
- **Total Scans** - All-time count
- **Today** - Scans captured today
- **This Week** - Last 7 days
- **This Month** - Current month
- **This Year** - Year-to-date

### Top 10 Vehicles:
- Most frequently detected plates
- Shows scan count for each
- **Tap** to view all scans for that plate

### Time Period Selector:
- **Today** - Hourly breakdown
- **This Week** - Monday to today (calendar week)
- **This Month** - First day to today
- **Year** - Full year with year selector (2024, 2025, 2026...)
- **Custom Range** - Pick any start and end dates

### Charts:
- Automatic layout based on period selected
- **Date range displayed** below selector (e.g., "Dec 1, 2025 - Jan 7, 2026")
- Scrollable for year view (12 months)

### Status Filter:
- **All** - Show everything
- **Whitelist** - Green plates only
- **Blacklist** - Red plates only
- **Unknown** - Orange plates only

**Pull down** to refresh data

---

## ⚙️ 5. Settings Page

<div align="center">
  <img src="setting_page.png" alt="Settings Page Screenshot" width="300"/>
</div>

**Purpose**: Configure app behavior

### Account Section:

**Login** (Business/Enterprise accounts)
- Enter email + signature
- **Infinite scans** (unlimited usage)
- Shows expiry date
- **Logout** button when logged in

**Free Trial Mode**
- Shows daily limit: X/100 scans
- Resets at midnight
- **Login for infinite scans**

### Notifications:

**Sound** 🔊
- Play audio alerts for detections
- Green plates: "Success" sound
- Red plates: "Alert" sound
- Orange plates: "Unknown" sound

**Vibration** 📳
- Haptic feedback on detection
- Different patterns for whitelist/blacklist

### Detection Settings:

**Sync Thresholds** 🔄
- Toggle to sync detection + OCR thresholds together
- Simplifies tuning

**Detection Threshold** (60-95%)
- Minimum confidence to detect plate
- Higher = fewer false positives
- Lower = more detections
- **Recommended**: 90%

**OCR Threshold** (60-95%)
- Minimum confidence for text recognition
- Higher = more accurate text
- Lower = read more plates
- **Recommended**: 90%

**Max Detections** (1-10)
- Maximum plates to capture per scan
- **Recommended**: 1 (parking/security)
- Higher for busy intersections

**Ignore Duplicate Plate** (0-60 seconds)
- Prevents saving same plate multiple times
- 0 = Save all (no filtering)
- 5s = Default (ignore if seen within 5 seconds)
- 60s = Maximum (ignore for 1 minute)

**Plate Region** 🌍
- **Universal** - All regions (default)
- **Europe+** - EU, UK, Switzerland, Norway, etc.
- **Korea** - South Korea (한국)
- **North America** - USA, Canada, Mexico
- **China** - China (中国)
- Selecting specific region improves accuracy

### Storage:

**Save Images** 📷
- Save full-resolution images with detections
- Viewable in Detections page
- Uses device storage

**Clear History** 🗑️
- Delete all detection records
- **Warning**: Cannot be undone

**Data Retention** (7-365 days, Never)
- Auto-delete old records
- **Default**: 30 days
- **Never**: Keep forever

### Location:

**Enable GPS** 📍
- Save location with each detection
- Required for Map view
- Shows address in details

### About:

- App name & version
- Website: www.marearts.com
- Support email: hello@marearts.com
- **Report Bug / Request Feature** - Opens GitHub Issues
- Build number (for troubleshooting)

---

## 🎯 Common Workflows

### Parking Management:
1. **Add residents** to Whitelist (Rules page)
2. **Scan** vehicles entering (Scan page)
3. **Check status** - Green = Allowed, Red = Blocked
4. **Review** violations (Detections page)

### Security Checkpoint:
1. **Add approved** vehicles to Whitelist
2. **Add banned** vehicles to Blacklist
3. **Continuous scan** at entrance
4. **Audio/vibration** alerts for blacklist

### Vehicle Tracking:
1. **Scan** vehicles continuously
2. **View history** in Detections
3. **Use Map** to see locations
4. **Export** data (via share button)

---

## 💡 Tips & Best Practices

### For Best Detection:

✅ **Distance**: 2-3 meters from vehicle  
✅ **Angle**: Perpendicular to plate (not tilted)  
✅ **Lighting**: Good outdoor light (daytime)  
✅ **Focus**: Tap plate area to focus  
✅ **Stability**: Hold steady while capturing  

❌ **Avoid**:
- Too far (>5 meters)
- Extreme angles
- Low light conditions
- Motion blur
- Dirty/damaged plates

### Settings Recommendations:

**High Accuracy** (parking/security):
- Detection: 90%
- OCR: 90%
- Max: 1 plate
- Region: Specific (if known)

**High Recall** (traffic monitoring):
- Detection: 70%
- OCR: 70%
- Max: 5 plates
- Region: Universal

---

## 🔒 Privacy & Security

✅ **100% On-Device**: All AI processing on your device  
✅ **No Cloud Storage**: Images never uploaded (unless you use cloud mode)  
✅ **Local Database**: All data stored locally  
✅ **GPS Optional**: Can disable location tracking  
✅ **No Analytics**: We don't track your usage  

**Cloud Mode** (Optional):
- Sends image to API for processing
- Used only when you tap cloud button
- More accurate (server-side AI)
- Requires internet connection

---

## 📞 Support

**Email**: hello@marearts.com  
**Website**: https://www.marearts.com  

**For Issues**:
- Include app version (Settings page)
- Describe the problem
- Include screenshot if possible 

---

## ⭐ Remember

> **✅ No Additional License Required!**  
> This app can be used as an ANPR license without any additional purchase.  
> Get your license at: [MareArts ANPR Solution](https://www.marearts.com/products/anpr)
> 
> 🔍 **Find the app by searching "marearts anpr" in the App Store**

---

**Need help?** Contact hello@marearts.com

