"""Entry program for the make.fun news-image-20261121 bounty.

Copies the pre-rendered poster (entry.png, drawn by tools/draw.py) to the
output directory the grader reads. Uses only the standard library and needs
no network.
"""
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE / "entry.png"
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
DEST = OUT_DIR / "entry.png"


def main():
    if not SRC.is_file():
        raise SystemExit("entry.png missing next to main.py")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SRC, DEST)
    size = DEST.stat().st_size
    if size > 1_048_576:
        raise SystemExit(f"entry.png too large: {size} bytes (limit 1 MiB)")
    print(f"wrote {DEST} ({size} bytes)")


if __name__ == "__main__":
    main()
