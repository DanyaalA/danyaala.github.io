from PIL import Image
from pathlib import Path

# Config
repo_root = Path(__file__).resolve().parents[1]
images_dir = repo_root / 'images'
thumbs_dir = images_dir / 'thumbs'
thumbs_dir.mkdir(parents=True, exist_ok=True)

# List of source filenames to generate thumbnails from (try .png and .PNG where ambiguous)
sources = [
    '500mL Spinner CFD Fluent_cropped.png',
    '500mL Spinner CFD Fluent_cropped.PNG',
    'demo-setup.png',
    'Velocity_contour.png',
    'fluidevice-resazurin-2-mixer-reynolds.png',
    'mach_number_contour.png'
]

# Thumb size for project cards (width, height) - we'll keep aspect ratio and fit inside this box
CARD_SIZE = (640, 360)  # 16:9 card thumbnails


def slug_name(name: str) -> str:
    # create a safe filename for the thumbnail
    s = name.lower()
    s = s.replace(' ', '-')
    s = s.replace('_', '-')
    s = s.replace('.png', '')
    s = s.replace('.jpg', '')
    s = s.replace('.jpeg', '')
    s = ''.join(c for c in s if (c.isalnum() or c in '-'))
    return s


for src in sources:
    src_path = images_dir / src
    if not src_path.exists():
        # try to find a case-insensitive match in the images folder
        matches = [p for p in images_dir.iterdir() if p.name.lower() == src.lower()]
        src_path = matches[0] if matches else None

    if not src_path or not src_path.exists():
        print(f"SKIP: source not found: {src}")
        continue

    try:
        with Image.open(src_path) as im:
            im = im.convert('RGB')
            im.thumbnail(CARD_SIZE, Image.LANCZOS)
            out_name = f"thumb-{slug_name(src)}.png"
            out_path = thumbs_dir / out_name
            im.save(out_path, format='PNG', optimize=True)
            print(f"WROTE: {out_path}")
    except Exception as e:
        print(f"ERROR processing {src_path}: {e}")

print('Done')
