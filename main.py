"""Entry program for the make.fun news-image-20261121 bounty.

Hands the pre-rendered poster (entry.png, drawn by tools/draw.py) to the
grader: it copies the image into the output directory the grader reads.
Standard library only; no network is needed.
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
IMAGE = ROOT / "entry.png"
MAX_BYTES = 1_048_576


def output_dir():
    """Where the grader looks: $MAKEFUN_OUTPUT_DIR, else /output."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def hand_in():
    if not IMAGE.is_file():
        raise SystemExit("entry.png missing next to main.py")
    dest_dir = output_dir()
    dest_dir.mkdir(parents=True, exist_ok=True)
    target = dest_dir / "entry.png"
    shutil.copyfile(IMAGE, target)
    size = target.stat().st_size
    if size > MAX_BYTES:
        raise SystemExit(f"entry.png too large: {size} bytes (limit 1 MiB)")
    print(f"wrote {target} ({size} bytes)")


if __name__ == "__main__":
    hand_in()
