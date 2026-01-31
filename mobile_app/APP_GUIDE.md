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

**Version 1.8.0 (Build 180)** - January 31, 2026

**⚡ Faster Performance** - App launches quicker and runs smoother

**📋 Smart Rules Grouping** - Rules organized A-Z for easy navigation with large lists

**🌐 Download Rules from Web** - Upload rules on marearts.com, download on your phone

**🔄 Background Sync** - Keep using the app while syncing in the background

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

### Camera Settings:

Tap the **⚙️ icon** next to the mode buttons to adjust:

**Resolution:**
- **1080p (1920×1080)** - Highest quality, best for detail (~140-160ms)
- **720p (1280×720)** - Balanced quality and speed (~100-130ms) ⭐ Recommended
- **480p (640×480)** - Fastest processing, good for high-volume (~80-110ms)

**Frame Rate:**
- **60 FPS** - Smooth preview (default)
- **30 FPS** - Battery saver mode

💡 **Tip:** Lower resolution = faster processing and less storage space!

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

### Export Data:

Tap **⋮ menu** in top-right corner:

**Export All Data (CSV)**
- Downloads all your detections as a CSV file
- Includes: Plate number, date, time, GPS coordinates, confidence scores
- Compatible with Excel, Google Sheets, and marearts.com
- Use for backup, analysis, or reporting
- Share via AirDrop, Files app, or email

💡 **Tip:** Export regularly to keep backups of your detection history!

---

## ✅ 3. Rules Page

<div align="center">
  <img src="rules_page_grouping.PNG" alt="Rules Page Screenshot" width="300"/>
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

**Smart Grouping** (NEW! 📋)
- Rules organized by letter (A, B, C... sections)
- Tap section header to expand/collapse
- Easy to navigate with hundreds or thousands of rules
- Quick scroll to any letter

**Management:**
- **Search Bar** - Type to filter plates (real-time)
- **Tab Counter** - Shows total: "White List (200)"
- **+ Button** (bottom center) - Add new plate
- **Swipe left** to delete
- **Group Sections** - Tap to expand/collapse
- Type full plate number or partial (e.g., "ABC" matches "ABC-123")
- Auto-uppercase
- Tap "X" to clear search, "Done" to dismiss keyboard

**Use Cases:**
- Parking: Whitelist residents, blacklist violators
- Security: Whitelist staff, blacklist banned vehicles
- Delivery: Track known vehicles

### Bulk Management:

Tap **⋮ menu** in top-right corner for more options:

**Export All Rules**
- Downloads all your whitelist and blacklist plates as CSV
- Compatible with Excel, Google Sheets, and marearts.com
- Perfect for backup or editing in spreadsheet

**Import Rules**
- Upload a CSV file to add rules to your phone
- Download sample template first to see the format
- Great for bulk adding plates (e.g., 100+ employee vehicles)

**Download Sample CSV**
- Get a template file with instructions
- Fill in: Plate Number, Type (whitelist/blacklist), Note
- Import when ready

💡 **Workflow:** Export → Edit in Excel → Import back for bulk updates!

---

### Download Rules from Web (NEW! 🌐)

<div align="center">
  <img src="rules_page_package_ready.PNG" alt="Rules Package Ready" width="300"/>
</div>

**Upload rules on marearts.com, download on your phone:**

**Step 1: Upload on Web**

<div align="center">
  <img src="webpage_upload_rule_package_button.png" alt="Web Upload Button" width="600"/>
</div>

1. Go to marearts.com/my-account
2. Click "Upload Rule Package" button
3. Choose your CSV file
4. Click upload

<div align="center">
  <img src="webpage_upload_rule_package_uploaded.png" alt="Upload Complete" width="600"/>
</div>

**Step 2: Download on Phone**
1. Open Rules page in app
2. See blue banner: "Rules package ready"
3. Tap to download
4. Choose "Replace All" or "Add to Existing"
5. Done! Rules imported automatically

**Benefits:**
- Upload large CSV files on computer (easier than phone)
- Share rules between team members
- Bulk import thousands of rules at once
- Works across all your devices

💡 **Tip:** Great for importing company vehicle lists or large databases!

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

### Cloud Sync:

<div align="center">
  <img src="setting_page_sync_backround.PNG" alt="Background Sync" width="300"/>
</div>

**Sync to Cloud** (Login required)
- **Two-way sync** - Keeps data in sync across all devices
- Tap **"Sync Now"** button to synchronize
- **Runs in background** - Keep using the app while syncing
- **Step 1:** Upload your device changes to cloud
- **Step 2:** Download data from cloud (other devices/web)
- **Step 3:** Merge changes automatically
- **Progress shown** - See sync status in real-time

**What Gets Synced:**
- ✅ All detections (plate numbers, timestamps, GPS)
- ✅ All rules (whitelist & blacklist)
- ✅ Detection images from all devices
- ✅ Changes from marearts.com web

**Benefits:**
- 📱 Use multiple devices with same account
- 🌐 View all data on marearts.com web dashboard
- 🔄 Rules added on web appear on all devices
- 💾 Cloud backup of all your data
- ⚡ Keep using app while syncing (NEW!)

<div align="center">
  <img src="setting_page_sync_data.PNG" alt="Sync Statistics" width="300"/>
  <p><i>See what's synced and when</i></p>
</div>

💡 **Tip:** Sync runs in background - no need to wait!

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
- 🌍 **Universal** - All regions (default)
- 🇪🇺 **Europe+** - EU, UK, Switzerland, Norway, etc.
- 🇰🇷 **Korea** - South Korea (한국)
- 🇺🇸🇨🇦🇲🇽 **North America** - USA, Canada, Mexico
- 🇨🇳 **China** - China (中国)
- Selecting specific region improves accuracy

### Storage:

**Save Images** 📷
- Save full-resolution images with detections
- Viewable in Detections page
- Uses device storage

**Clear All Data** 🗑️
- Delete all detections AND rules
- Shows count before deletion
- **Warning**: Cannot be undone unless logged in (syncs deletion to cloud)

**Factory Reset** 🔄 (NEW!)
- Fresh start - deletes all local data
- **Cloud backup stays safe** - can sync to restore
- Resets settings to defaults
- Keeps login credentials
- Located in Advanced section at bottom
- **Use when:** Corrupted data, want fresh start, or troubleshooting

**Data Retention** (7-365 days)
- Auto-delete old detections
- **Default**: 30 days
- Applies to detections only (rules kept)

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
✅ **Local Database**: All data stored locally  
✅ **GPS Optional**: Can disable location tracking  
✅ **Your Control**: Cloud sync only when you choose  

**Cloud Mode** (Optional):
- Sends image to API for processing
- Used only when you tap cloud button
- More accurate (server-side AI)
- Requires internet connection

**Cloud Sync** (Optional):
- Only syncs when you tap "Sync Now"
- Images uploaded only if you enable sync
- Can work 100% offline if preferred

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

