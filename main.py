import os
import shutil
from pathlib import Path

out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
out_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(Path(__file__).resolve().parent / "entry.png", out_dir / "entry.png")
