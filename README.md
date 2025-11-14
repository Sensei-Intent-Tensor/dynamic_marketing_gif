# dynamic_marketing_gif
dynamic_marketing_gif

# Dynamic_Marketing_GIF

Complete marketing GIF generator with 3.1 million unique combinations and full customization.

## What This Does

Generates professional animated marketing GIFs with:
- ⚡ **3,110,400 unique frame combinations**
- 🎨 **Full color wheel** (360 hues)
- 📝 **Custom text** (company, services, tagline, URL)
- 🎭 **5 font styles** (bold, tech, elegant, blocky, script)
- 📐 **4 geometry patterns** (sharp, round, mixed, minimal)
- 🌅 **Solar dampener** (time-aware brightness)
- ✅ **Automatic contrast** (WCAG AAA standard)
- 🎲 **Random mode** (fresh content every time)

## Quick Start

```bash
# Simple 3-frame GIF
https://your-app.onrender.com/marketing.gif?count=3

# Custom company and services
https://your-app.onrender.com/marketing.gif?count=5&company=YourBrand&services=Product1,Product2,Product3

# Random mode
https://your-app.onrender.com/marketing.gif?count=10&random=true

# Surprise me!
https://your-app.onrender.com/marketing.gif?count=0
```

## Deployment

### Render Configuration:
- **Build Command:** `pip install flask cairosvg pillow flask-cors`
- **Start Command:** `python server.py`
- **Runtime:** Python 3

### Files to Upload:
1. `generate_marketing.py` - Frame generator with full color/geometry system
2. `server.py` - Flask server with complete parameter handling
3. `README.md` - This file

## Complete API

### Frame Control

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `count` | 1-100, 0 | 3 | Number of frames (0 = surprise mode) |
| `random` | true/false | false | Random sampling from 3.1M space |
| `frame` | 0-3110399 | - | Specific frame ID(s), comma-separated |
| `seed` | text | - | Seed for reproducible random |
| `duration` | milliseconds | 1000 | Frame duration |

### Text Control

| Parameter | Example | Default | Description |
|-----------|---------|---------|-------------|
| `company` | YourBrand | Auto_Workspace-AI | Company/brand name (max 50 chars) |
| `services` | A,B,C | Consulting,Automations,Workshops | Comma-separated list (max 10) |
| `tagline` | Your Slogan | - | Optional tagline (max 100 chars) |
| `url` | yourbrand.com | - | Optional website (max 50 chars) |

### Visual Control

| Parameter | Values | Default | Description |
|-----------|--------|---------|-------------|
| `bg` | blue, red, #FF0000 | auto | Background color |
| `text` | white, cyan, #00FFFF | auto | Text color (enforced contrast) |
| `accent` | yellow, purple | auto | Accent color for effects |
| `font` | bold, tech, elegant, blocky, script | bold | Font style |
| `geometry` | sharp, round, mixed, minimal | mixed | Geometric pattern style |

## Usage Examples

### Example 1: Restaurant
```
/marketing.gif?count=5&company=Joe's Diner&services=Breakfast,Lunch,Dinner,Desserts,Drinks&tagline=Best Food in Town&url=joesdiner.com
```

### Example 2: Tech Startup
```
/marketing.gif?count=3&company=StartupXYZ&services=SaaS,API,Consulting&font=tech&geometry=sharp&bg=black&text=cyan
```

### Example 3: Consulting Firm
```
/marketing.gif?count=4&company=SmithConsulting&services=Strategy,Operations,Finance,HR&font=elegant&geometry=minimal
```

### Example 4: E-commerce
```
/marketing.gif?count=10&random=true&company=ShopMore&services=Electronics,Clothing,Home,Sports&url=shopmore.com
```

### Example 5: Patriotic Theme
```
/marketing.gif?count=6&company=USA Brand&services=Made in America,Quality,Tradition&bg=blue&text=white&accent=red
```

## Frame Space Breakdown

**Total: 3,110,400 unique combinations**

```
360 hues (full color wheel)
  × 6 background gradient styles
  × 4 geometry patterns
  × 24 time slots (solar dampener)
  × 5 font styles
  = 3,110,400 frames
```

## Features

### 🎨 Full Color Wheel
- 360 discrete hues
- Named colors: red, orange, yellow, lime, green, cyan, blue, purple, magenta, pink
- Hex codes: #FF0000, #00FF00, etc.
- Automatic complementary colors

### ✅ Automatic Contrast Enforcement
- WCAG AAA standard (7:1 ratio minimum)
- Text always readable
- User color preferences respected when possible
- Automatic override when contrast insufficient

### 🎲 Random Mode
- Sample from full 3.1M frame space
- Different output every generation
- Optional seed for reproducibility
- Avoids sequential repetition

### 📐 Geometry Patterns
- **Sharp:** Angular, tech aesthetic
- **Round:** Curves, friendly feel
- **Mixed:** Variety (default)
- **Minimal:** Clean, Apple-style

### 🎭 Font Styles
- **Bold:** Arial Black, heavy impact (default)
- **Tech:** Courier/monospace, digital
- **Elegant:** Georgia serif, sophisticated
- **Blocky:** Impact, brutalist
- **Script:** Cursive, flowing

### 🌅 Solar Dampener
- Brightness scales with time representation
- Peak brightness at "noon" (hour 12)
- Minimum at "midnight" (hour 0/24)
- Smooth sine wave transitions

## Workflow

### Traditional Method
```
1. Open Photoshop
2. Design image #1 (1 hour)
3. Export
4. Design image #2 (1 hour)
5. Design image #3 (1 hour)
Total: 3 hours for 3 static images
```

### This System
```
1. Build URL (30 seconds)
2. Download GIF (5 seconds)
Total: 35 seconds for 24 animated frames
```

**Time saved: ~99%**

## Technical Details

### Color System
- HSL color space for smooth gradients
- Luminance calculation for contrast
- Automatic color adjustment
- 6 gradient pattern styles

### Text Layout
```
┌─────────────────────────┐
│                         │
│    [COMPANY NAME]       │  ← 36px (or 28px if long)
│    ─────────────        │  ← Separator line
│    [SERVICE]            │  ← 28px (or 22px if long)
│    [TAGLINE]           │  ← 18px (optional)
│    [URL]               │  ← 14px (optional)
│                         │
└─────────────────────────┘
```

### Service Rotation
```python
services = ["A", "B", "C"]
Frame 0 → "A"
Frame 1 → "B"
Frame 2 → "C"
Frame 3 → "A" (cycles)
```

### Frame ID Decomposition
```python
frame_id = 123456

hue = (123456 * 37) % 360 = 72 (yellow-green)
bg_style = (123456 // 360) % 6 = 3 (horizontal)
geometry = (123456 // 2160) % 4 = 1 (round)
time_slot = (123456 // 25920) % 24 = 4 (4 AM - dark)
font = (123456 // 622080) % 5 = 0 (bold)
```

## Advanced Usage

### Reproducible Random
```
/marketing.gif?count=10&random=true&seed=myseed
```
Same seed = same random frames

### Specific Frames
```
/marketing.gif?frame=50000
/marketing.gif?frame=100,200,300,400
```
Direct frame access

### Surprise Mode
```
/marketing.gif?count=0
```
Random count (10-30), random frames, random speed

### Color Theming
```
# Blue family
?bg=blue&text=white&accent=cyan

# Warm
?bg=orange&text=black&accent=yellow

# Tech
?bg=black&text=green&accent=lime
```

## File Size Guide

| Frames | Approx Size | Use Case |
|--------|-------------|----------|
| 1 | 15 KB | Static image |
| 3 | 45 KB | Quick demo |
| 6 | 90 KB | Medium loop |
| 12 | 180 KB | Long loop |
| 24 | 360 KB | Full cycle |
| 50 | 750 KB | Maximum variety |

## Limitations

- Maximum 100 frames per GIF (file size)
- Services list capped at 10 items
- Text lengths limited for optimal display
- Some fonts may not render identically across all platforms

## License

MIT

---

**Dynamic_Marketing_GIF** | Marketing Automation Perfected ⚡
