# Regional Support

**Last Updated: February 4, 2026**

MareArts ANPR provides comprehensive license plate recognition across multiple regions with specialized models optimized for each area. Uses V14 Detector with V15 OCR (latest) or V14 OCR (backward compatible).

## Universal Model

### Overview
The Universal model is designed to handle license plates from all supported regions.

### Features
- **Multi-language**: Supports all character sets from all regions
- **Flexibility**: No need to specify region beforehand (default option)
- **Convenience**: Works out-of-the-box without region configuration

### Region Code
- **Code**: `univ` (Universal - default)
- **Usage**: `ma_anpr_ocr('large_fp32', 'univ', ..., version='v15')`
- **Recommendation**: Use specific region codes for best accuracy when region is known

---

## European Union & Plus Countries

### Supported Countries

#### Core EU Countries
- 🇦🇹 Austria
- 🇧🇪 Belgium
- 🇧🇬 Bulgaria
- 🇭🇷 Croatia
- 🇨🇾 Cyprus
- 🇨🇿 Czechia
- 🇩🇰 Denmark
- 🇫🇮 Finland
- 🇫🇷 France
- 🇩🇪 Germany
- 🇬🇷 Greece
- 🇭🇺 Hungary
- 🇮🇪 Ireland
- 🇮🇹 Italy
- 🇱🇺 Luxembourg
- 🇲🇹 Malta
- 🇳🇱 Netherlands
- 🇵🇱 Poland
- 🇵🇹 Portugal
- 🇷🇴 Romania
- 🇸🇰 Slovakia
- 🇸🇮 Slovenia
- 🇪🇸 Spain
- 🇸🇪 Sweden

#### Additional European Countries
- 🇦🇱 Albania
- 🇦🇩 Andorra
- 🇧🇦 Bosnia and Herzegovina
- 🇱🇮 Liechtenstein
- 🇲🇨 Monaco
- 🇲🇪 Montenegro
- 🇲🇰 North Macedonia
- 🇳🇴 Norway
- 🇸🇲 San Marino
- 🇷🇸 Serbia
- 🇨🇭 Switzerland
- 🇬🇧 United Kingdom

#### Plus Countries
- 🇮🇩 Indonesia

### Character Support

```python
characters = [
    "-", ".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", 
    "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", 
    "Y", "Z", "a", "d", "g", "i", "j", "m", "o", "p",
    "Ä", "Å", "Ö", "Ø", "Ü",  # Nordic/German characters
    "Ć", "Č", "Đ", "Š", "Ž",  # Croatian/Serbian characters
    "Б", "М", "П", "Р", "Т", "а", "в", "г", "е", "к", "о", "с", "т", "у", "х"  # Cyrillic characters
]
```

### Region Code
- **Code**: `euplus` or `eup` (Europe Plus)
- **Usage**: `ma_anpr_ocr('large_fp32', 'euplus', ..., version='v15')`

## Korea Support

한국 자동차 번호판 인식 솔루션

### Character Support

#### Numbers
```python
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
```

#### Korean Characters
```python
korean_chars = [
    '가', '강', '거', '경', '계', '고', '관', '광', '구', '금', '기', '김',
    '나', '남', '너', '노', '누',
    '다', '대', '더', '도', '동', '두', '등',
    '라', '러', '로', '루', '리',
    '마', '머', '명', '모', '무', '문', '미',
    '바', '배', '뱌', '버', '보', '부', '북',
    '사', '산', '서', '세', '소', '수', '시',
    '아', '악', '안', '양', '어', '연', '영', '오', '용', '우', '울', '원', '육',
    '이', '인',
    '자', '작', '저', '전', '제', '조', '종', '주', '중', '지',
    '차', '천', '초', '추', '충',
    '카', '타', '파', '평', '포',
    '하', '허', '호', '홀', '후', '히'
]
```


### Region Code
- **Code**: `kor` or `kr` (Korea)
- **Usage**: `ma_anpr_ocr('large_fp32', 'kor', ..., version='v15')`

## China Support

中国车牌识别解决方案

### Character Support

#### Numbers and Letters
```python
alphanumeric = ['0-9', 'A-Z']
```

#### Chinese Characters
```python
chinese_chars = [
    '·',  # Special separator
    # Province/Region codes
    '云', '京', '冀', '吉', '宁', '川', '挂', '新', '晋', '桂',
    '沪', '津', '浙', '渝', '港', '湘', '澳', '琼', '甘', '皖',
    '粤', '苏', '蒙', '藏', '豫', '贵', '赣', '辽', '鄂', '闽',
    '陕', '青', '鲁', '黑'
]
```


### Region Code
- **Code**: `china` or `cn` (China)
- **Usage**: `ma_anpr_ocr('large_fp32', 'china', ..., version='v15')`

## North America Support

🇺🇸 🇨🇦 USA and Canada License Plate Recognition

### Character Support

#### Numbers and Letters
```python
alphanumeric = ['0-9', 'A-Z', '#', '-', '.', '@']
```

### Region Code
- **Code**: `na` (North America)
- **Usage**: `ma_anpr_ocr('large_fp32', 'na', ..., version='v15')`

---

## Implementation Example

```python
from marearts_anpr import ma_anpr_detector_v14, ma_anpr_ocr

# Initialize V14 Detector (same for all regions)
detector = ma_anpr_detector_v14(
    "medium_640p_fp32", 
    user_name, 
    serial_key, 
    signature, 
    backend="cuda"
)

# Initialize OCR for your target region (V15 - Latest)
# For Universal (handles all regions):
ocr = ma_anpr_ocr("large_fp32", "univ", user_name, serial_key, signature, version='v15')

# OR for specific region (better accuracy when region is known):
# ocr = ma_anpr_ocr("large_fp32", "kor", user_name, serial_key, signature, version='v15')    # Korean (or 'kr')
# ocr = ma_anpr_ocr("large_fp32", "euplus", user_name, serial_key, signature, version='v15') # Europe+ (or 'eup')
# ocr = ma_anpr_ocr("large_fp32", "na", user_name, serial_key, signature, version='v15')     # North America
# ocr = ma_anpr_ocr("large_fp32", "china", user_name, serial_key, signature, version='v15')  # China (or 'cn')

# For V14 OCR (backward compatible):
# ocr = ma_anpr_ocr("large_fp32", "univ", user_name, serial_key, signature, version='v14')

# NEW (>3.6.5): Dynamic region switching for multi-region applications
# Supports both V14 and V15 OCR
# ocr.set_region('euplus')  # Switch to Europe+ (or 'eup')
# ocr.set_region('kor')     # Switch to Korea (or 'kr')
# ocr.set_region('na')      # Switch to North America
# ocr.set_region('china')   # Switch to China (or 'cn')
# ocr.set_region('univ')    # Switch to Universal
# Use ONE instance for all regions - saves memory!

# Process image
result = marearts_anpr_from_image_file(detector, ocr, image_path)
```

> **Performance Details**: See [Model Performance Documentation](models.md) for detailed benchmarks and accuracy metrics.

---

## Adding New Regions

For custom regions or special requirements, contact [hello@marearts.com](mailto:hello@marearts.com) for:

- Custom model training
- Additional character support
- Special plate formats
- Enterprise solutions
