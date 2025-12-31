# Changelog

## Version 1.0.0 (2025-12-31)

### Initial Release

Professional ANPR management server with REST API and Web Dashboard.

### Features

- REST API with 3 input methods (file, bytes, base64)
- Web dashboard with 4 tabs (Dashboard, Upload, History, Settings)
- SQLite database for history
- Auto-load credentials from `~/.marearts/.marearts_env`
- Live model and region switching
- Quick date filters (Today, Week, Month, 3 Months, Custom, All)
- Combined statistics and analytics on Dashboard tab
- Two-column layout (image | info) for efficient space usage
- Clickable images with full-size modal view
- Model download status tracking
- Web-based credential configuration
- Bounding box display in all views

### Bug Fixes

#### Fixed: KeyError 'bbox'
- **Issue:** Server crashed when processing images
- **Cause:** Field name mismatch between SDK output ('ltrb') and API format ('bbox')
- **Fix:** Added proper field mapping in all detection endpoints
- **Status:** ✅ Resolved

#### Fixed: Button Activation Bug
- **Issue:** Wrong period buttons stayed active in History tab
- **Cause:** Incorrect button selection logic
- **Fix:** Improved button activation with proper text matching
- **Status:** ✅ Resolved

#### Fixed: Double Database Insert
- **Issue:** Detection data was being saved twice
- **Cause:** Called `db.add_detection()` twice in `process_image_bytes()`
- **Fix:** Removed duplicate call, save only once with image paths
- **Status:** ✅ Resolved

#### Fixed: Date Filtering
- **Issue:** History queries returned 0 results even with data
- **Cause:** SQLite timestamp comparison not using date() function
- **Fix:** Changed to `date(timestamp)` for day-level filtering
- **Status:** ✅ Resolved

#### Fixed: Tab Menu Scrollbar
- **Issue:** Horizontal scrollbar on smaller screens
- **Cause:** Using flexbox with overflow-x
- **Fix:** Changed to CSS Grid with equal columns
- **Status:** ✅ Resolved

### UI Improvements

#### Compact Design
- Reduced card padding (20px → 15px)
- Reduced plate text size (1.5em → 1.3em)
- Reduced image width (400px → 350px)
- Tighter gaps throughout (20px → 12px)
- Result: More professional, less empty space

#### Professional Styling
- Clean white cards with subtle borders
- Neutral gray color palette (#f5f7fa, #2c3e50, #7f8c8d)
- Professional blue accent (#3498db)
- Corporate-grade appearance
- Removed colorful gradients

#### Responsive Layout
- 5-column grid for tabs (no scrollbar)
- Dynamic card sizing
- Mobile-friendly design
- Works on any screen size

### API Endpoints

**Detection:**
- `POST /api/detect` - File upload
- `POST /api/detect/binary` - Raw bytes
- `POST /api/detect/base64` - Base64 image

**Management:**
- `GET /api/stats` - Server statistics
- `GET /api/history` - Detection history with filters
- `GET /api/history/{id}` - Specific detection
- `GET /api/daily-stats` - Daily statistics
- `GET /api/health` - Health check

**Configuration:**
- `POST /api/configure` - Set credentials
- `POST /api/models/update` - Update models/region
- `GET /api/models/status` - Model download status
- `POST /api/database/clear` - Delete all data
- `GET /api/debug/database` - Debug database contents

### Performance

- CPU: ~150-300ms per image (~3-7 FPS)
- GPU: ~20-30ms per image (~30-50 FPS)
- SQLite database for fast queries
- Auto-refresh dashboard every 30 seconds

### Security

- No credentials in code
- Auto-load from secure config file
- Web-based credential input with validation
- Proper .gitignore for sensitive files
- Safe for public repositories

---

## Known Issues

None reported.

## Planned Features

- Export detection history (CSV, JSON)
- Email notifications
- Webhook support
- Multi-user authentication
- Real-time video streaming
- Batch image upload

---

**Version:** 1.0.0  
**Release Date:** 2025-12-31  
**Status:** Stable
