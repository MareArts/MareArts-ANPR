# Regional Support

MareArts ANPR provides comprehensive license plate recognition across multiple regions with specialized models optimized for each area.

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
    "Y", "Z", "a", "d", "i", "m", "o",
    "Ö", "Ü",  # German characters
    "Ć", "Č", "Đ", "Š", "Ž",  # Croatian/Serbian characters
    "П"  # Cyrillic character
]
```

### Recommended Model
- **OCR Model**: `v13_euplus` or `v11_euplus`
- **Coverage**: All EU countries + Indonesia
- **Accuracy**: 96.2% - 98.2%

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
    '가', '강', '거', '견', '경', '고', '곡', '공', '광', '교', '구', '국', '군', '금', '급', '기',
    '나', '남', '너', '노', '녹', '논', '누',
    '다', '단', '대', '더', '도', '동', '두',
    '라', '러', '렬', '령', '례', '로', '루', '륜', '률', '린', '림', '립',
    '마', '머', '면', '명', '모', '목', '무', '문',
    '바', '배', '백', '버', '병', '보', '봉', '부', '북', '빙',
    '사', '산', '삼', '상', '서', '성', '세', '소', '수', '순', '신',
    '아', '안', '양', '어', '역', '연', '영', '예', '오', '완', '왕', '외', 
    '용', '우', '운', '울', '원', '월', '위', '유', '육', '은', '이', '익', '인', '일', '임',
    '자', '작', '장', '재', '저', '적', '전', '정', '제', '조', '종', '주', '진',
    '차', '창', '채', '천', '철', '청', '초', '춘', '출', '충',
    '태', '택', '토', '통', '특',
    '파', '팔', '평', '포', '표',
    '하', '학', '한', '함', '합', '해', '행', '허', '헌', '협', '형', '호', '홍',
    '화', '황', '흑', '흥'
]
```


### Recommended Model
- **OCR Model**: `v13_kr` or `v11_kr`
- **Accuracy**: 97.2% - 99.4%

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
    '云', '京', '冀', '吉', '宁', '川', '新', '晋', '桂',
    '沪', '津', '浙', '渝', '港', '湘', '澳', '琼', '甘', '皖',
    '粤', '苏', '蒙', '藏', '豫', '贵', '赣', '辽', '鄂', '闽', 
    '陕', '青', '鲁', '黑',
    # Special prefix
    '挂'  # Trailer plate prefix
]
```


### Recommended Model
- **OCR Model**: `v13_cn`
- **Accuracy**: 96.6%

## Universal Model

### Overview
The Universal model is designed to handle license plates from all supported regions with automatic detection.

### Features
- **Auto-detection**: Automatically identifies plate region
- **Multi-language**: Supports all character sets
- **Flexibility**: No need to specify region beforehand
- **Accuracy**: 98.3% overall accuracy


### Recommended Model
- **OCR Model**: `v13_univ`

## Model Selection Guide

### By Region

| Region | Best Model | Alternative | Notes |
|--------|------------|-------------|-------|
| Europe | `v13_euplus` | `v11_euplus` | Includes EU + Indonesia |
| Korea | `v13_kr` | `v11_kr` | Highest accuracy for Korean plates |
| China | `v13_cn` | `v13_univ` | Optimized for Chinese characters |
| Mixed | `v13_univ` | - | Best for multi-region support |

### By Use Case

| Use Case | Recommended Model | Reason |
|----------|------------------|---------|
| EU parking system | `v13_euplus` | Region-specific optimization |
| Korean toll gates | `v13_kr` or `v11_kr` | Maximum accuracy needed |
| International airport | `v13_univ` | Handles all regions |
| Border control | `v13_univ` | Multi-country plates |
| City traffic monitoring | Region-specific model | Better accuracy |

## Implementation Example

```python
from marearts_anpr import ma_anpr_detector, ma_anpr_ocr

# Initialize detector (same for all regions)
detector = ma_anpr_detector("v13_middle", user_name, serial_key)

# Region-specific OCR
ocr_eu = ma_anpr_ocr("v13_euplus", user_name, serial_key)  # Europe
ocr_kr = ma_anpr_ocr("v13_kr", user_name, serial_key)       # Korea
ocr_cn = ma_anpr_ocr("v13_cn", user_name, serial_key)       # China
ocr_universal = ma_anpr_ocr("v13_univ", user_name, serial_key)  # All regions

# Process based on expected region
def process_by_region(image_path, region):
    ocr_models = {
        'eu': ocr_eu,
        'kr': ocr_kr,
        'cn': ocr_cn,
        'universal': ocr_universal
    }
    
    ocr = ocr_models.get(region, ocr_universal)
    return marearts_anpr_from_image_file(detector, ocr, image_path)
```

## Adding New Regions

For custom regions or special requirements, contact [hello@marearts.com](mailto:hello@marearts.com) for:
- Custom model training
- Additional character support
- Special plate formats
- Enterprise solutions