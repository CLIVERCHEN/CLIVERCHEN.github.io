#!/usr/bin/env python3
"""Generate web-sized derivatives; leave all camera originals untouched.

Requires Pillow. Run from any directory with: python3 scripts/prepare_photos.py
"""
from pathlib import Path
import hashlib
import json
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "static/img/photography"
OUTPUT = ROOT / "static/media/photos"
OUTPUT.mkdir(parents=True, exist_ok=True)

# Titles describe visible subjects, without inferring locations or dates.
SELECTED = [
    ("DSC_4702-3.jpg", "A streak of light", "A bright streak beside the Milky Way above a stone tower", False),
    ("_DSC4257.jpg", "City after sunset", "A city skyline beneath a glowing orange evening sky", False),
    ("未标题-1.jpg", "Departures at dusk", "Airport runways, aircraft, and a control tower under a pastel evening sky", False),
    ("DJI_20250623140048_0168_D.jpg", "Between the clouds", "Green mountain valleys beneath low clouds", True),
    ("DSC_5550.jpg", "Under the Milky Way", "The Milky Way above a silhouetted tree", True),
    ("北京市+石景山区+首钢大桥+CliverChen.jpg", "An arc at dusk", "An illuminated arch bridge beneath a pink evening sky", True),
    ("未标题_全景图-1.jpg", "Desert after dark", "A panoramic night sky above cacti and still water", False),
    ("草原1_low.jpg", "Open country", "Sunlight on green grasslands backed by distant mountains", False),
    ("7F9EF1C8B31E39466B189247AE047C10.png", "City in motion", "Traffic on a busy city street lined with buildings", False),
    ("DSC_1191-Min Horizon Noise.jpg", "A sky of its own", "A circular view of the night sky framed by desert cacti", False),
    ("_DSC4074.jpg", "Below the mountains", "A mountain range above a green meadow under heavy clouds", False),
    ("北京市+东城区+国贸+CliverChen.jpg", "Blue hour", "A city skyline and glass architecture at blue hour", False),
    ("DSC_3462.jpg", "One more night outside", "The Milky Way and a light trail above a parked vehicle", False),
    ("_DSC9431.jpg", "The last light", "Warm light falling between layered rock formations", False),
    ("DJI_20250626180857_0303_D.jpg", "Lines in the land", "Aerial view of eroded ridges and green hills", False),
    ("DSC_7706-已增强-NR-恢复的.jpg", "Following the sun", "A sequence of suns above city traffic at sunset", False),
    ("4B06E6CECF5A011E93F859D0894310D0.jpg", "Moon over the city", "A sequence of moons above an illuminated traditional roof", False),
    ("陕西省+西安市+城墙东南角+CliverChen.jpg", "Old and new", "An illuminated traditional tower framed by modern buildings", False),
]

def derivative(source, dest, size, quality):
    if dest.exists() and dest.stat().st_mtime >= source.stat().st_mtime:
        return
    with Image.open(source) as original:
        im = ImageOps.exif_transpose(original).convert("RGB")
        im.thumbnail(size, Image.Resampling.LANCZOS)
        # Deliberately omit EXIF (including GPS) from public web derivatives.
        im.save(dest, "WEBP", quality=quality, method=6)

def main():
    records = []
    selected_sources = {row[0]: SOURCE / "selected" / row[0] for row in SELECTED}
    items = [(SOURCE / "selected" / name, title, alt, home, True) for name, title, alt, home in SELECTED]
    for p in sorted(SOURCE.iterdir()):
        if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}:
            if p.name in selected_sources and p.read_bytes() == selected_sources[p.name].read_bytes():
                continue
            number = len(items) - len(SELECTED) + 1
            items.append((p, f"From the archive · {number:02}", f"Photograph by Keru Chen, archive {number}", False, False))
    for source, title, alt, home, selected in items:
        # Distinguish different photographs with the same filename in selected/.
        key_name = str(source.relative_to(SOURCE)) if selected and (SOURCE / source.name).exists() and source.read_bytes() != (SOURCE / source.name).read_bytes() else source.name
        key = hashlib.sha256(key_name.encode()).hexdigest()[:12]
        thumb = OUTPUT / f"{key}-720.webp"
        full = OUTPUT / f"{key}-2400.webp"
        derivative(source, thumb, (720, 960), 80)
        derivative(source, full, (2400, 2400), 88)
        with Image.open(thumb) as im:
            width, height = im.size
        records.append(dict(title=title, alt=alt, home=home, selected=selected,
                            thumb=f"media/photos/{thumb.name}", full=f"media/photos/{full.name}",
                            width=width, height=height))
    (ROOT / "data/photos.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n")
    avatar = ROOT / "static/media/profile/avatar.webp"
    with Image.open(ROOT / "static/img/avatar.jpg") as im:
        im = ImageOps.fit(ImageOps.exif_transpose(im).convert("RGB"), (400, 400), Image.Resampling.LANCZOS)
        im.save(avatar, "WEBP", quality=88)
    total = sum(p.stat().st_size for p in OUTPUT.glob("*.webp"))
    print(f"Prepared {len(records)} photographs ({total / 1024 / 1024:.1f} MB); originals unchanged.")

if __name__ == "__main__":
    main()
