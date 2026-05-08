# IconForge

**Download Google Material Icons by category — straight from your terminal.**

No accounts. No API keys. No manual clicking. Just run and pick what you need.

```
  _____            ______
 |_   _|          |  ____|
   | |  ___  ___  | |__ ___  _ __ __ _  ___
   | | / __|/ _ \ |  __/ _ \| '__/ _` |/ _ \
  _| |_\__ \ (_) || | | (_) | | | (_| |  __/
 |_____|___/\___/ |_|  \___/|_|  \__, |\___|
                                   __/ |
                                  |___/
```

---

## Features

- Interactive menu — choose categories and variants without memorizing flags
- 1 200+ icons across **18 categories** (action, maps, editor, social, av, and more)
- **5 variants** per icon: `baseline`, `outline`, `round`, `sharp`, `twotone`
- Parallel downloads — fast even for full sets
- Optional `.zip` archive export after download
- Clean folder structure ready to drop into any project
- Works with Python 3.8+ — zero mandatory dependencies

---

## Requirements

- Python 3.8 or newer

Optional (better colors on Windows):

```bash
pip install colorama
```

---

## Installation

```bash
git clone https://github.com/your-username/iconforge.git
cd iconforge
```

That's it. No `pip install`, no build step.

---

## Usage

### Interactive mode (recommended)

```bash
python iconforge.py
```

You'll see a numbered menu of all categories and variants. Pick what you want and confirm. Done.

---

### Flag mode

```bash
# Download action + navigation icons (baseline only)
python iconforge.py --categories action navigation

# Download all categories, outline variant, into ./my-icons
python iconforge.py --categories all --variants outline --output ./my-icons

# Download action icons in baseline + outline, create a zip
python iconforge.py --categories action --variants baseline outline --zip

# 16 parallel workers for faster downloads
python iconforge.py --categories all --variants baseline --workers 16
```

---

### All flags

| Flag | Short | Description |
|---|---|---|
| `--categories` | `-c` | One or more category names, or `all` |
| `--variants` | `-v` | One or more variants (default: `baseline`) |
| `--output` | `-o` | Output folder (default: `./icons`) |
| `--workers` | `-w` | Parallel threads (default: `8`) |
| `--zip` | `-z` | Create `.zip` archive after download |
| `--list` | `-l` | List all categories and icon counts |
| `--no-banner` | | Skip the ASCII banner |

---

### List categories

```bash
python iconforge.py --list
```

```
  Available categories:

  action              573 icons
  alert                 6 icons
  av                   90 icons
  communication        71 icons
  content              66 icons
  device              106 icons
  editor              130 icons
  file                 42 icons
  hardware             71 icons
  home                 76 icons
  image               155 icons
  maps                169 icons
  navigation           43 icons
  notification         67 icons
  places               68 icons
  search                8 icons
  social              107 icons
  toggle               11 icons
  transportation       47 icons

  Total: 1 206 icons across 18 categories
```

---

## Output structure

```
icons/
├── action/
│   ├── favorite/
│   │   ├── baseline.svg
│   │   └── outline.svg
│   └── search/
│       └── baseline.svg
├── maps/
│   └── directions_car/
│       └── baseline.svg
└── _failed.log   ← only if any downloads failed
```

Each icon lives in its own folder with one file per variant. Drop the folder into your project and reference SVGs directly.

---

## Categories

| Category | Icons | Description |
|---|---|---|
| `action` | 573 | General UI actions — delete, search, settings, share… |
| `alert` | 6 | Warnings, errors, notifications |
| `av` | 90 | Audio/video controls — play, pause, volume, mic… |
| `communication` | 71 | Chat, calls, email, QR codes |
| `content` | 66 | Copy, paste, link, archive, undo… |
| `device` | 106 | Battery, Bluetooth, Wi-Fi, screen, GPS |
| `editor` | 130 | Text formatting, charts, draw, attach |
| `file` | 42 | Cloud, folders, upload, download |
| `hardware` | 71 | Keyboards, monitors, headsets, routers |
| `home` | 76 | Smart home, appliances, furniture, rooms |
| `image` | 155 | Camera, filters, crop, exposure, photo |
| `maps` | 169 | Places, transit, navigation, restaurants |
| `navigation` | 43 | Arrows, chevrons, menus, expand |
| `notification` | 67 | Sync, priority, phone states, events |
| `places` | 68 | Hotels, amenities, buildings, facilities |
| `search` | 8 | Find, scan, lookup |
| `social` | 107 | People, groups, sports, emoji, reactions |
| `toggle` | 11 | Checkboxes, radio buttons, star, toggles |
| `transportation` | 47 | Cars, trains, bikes, flights, transit |

---

## Variants

| Variant | Description |
|---|---|
| `baseline` | Filled — the standard version |
| `outline` | Stroked / unfilled |
| `round` | Rounded corners |
| `sharp` | Angular corners |
| `twotone` | Two-tone fill |

---

## License

Icons are from [Google Material Design Icons](https://github.com/google/material-design-icons) and served via [material-icons.github.io](https://material-icons.github.io).  
Released under the **Apache License 2.0** — free for personal and commercial use.

---

*Created by Emanuel Felipe (Lipe Developer)*
