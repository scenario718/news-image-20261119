"""Write the entry image for the 19 November 2026 news-image bounty.

The picture is committed in this repository as ``entry.png``: one
image summing up the world's news of Thursday 19 November 2026,
drawn by ``draw.py`` (kept beside this file; the README lists the
stories it shows). The grader's container installs nothing and has
no Pillow, so this program is standard library only: it copies the
committed image to the output path byte for byte, which also makes
it deterministic — every run writes the asset's exact bytes.
"""

import hashlib
import os
import shutil
from pathlib import Path

ASSET_NAME = "entry.png"
OUTPUT_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> None:
    here = Path(__file__).resolve().parent
    asset = here / ASSET_NAME
    if not asset.is_file():
        raise SystemExit(f"asset missing from repository: {asset}")
    if not asset.read_bytes().startswith(PNG_MAGIC):
        raise SystemExit("asset is not a PNG file")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / OUTPUT_NAME
    shutil.copyfile(asset, target)
    # Read both files back and compare digests, so a truncated copy
    # can never pass silently: the grader must see the whole image.
    src_digest = hashlib.sha256(asset.read_bytes()).hexdigest()
    out_digest = hashlib.sha256(target.read_bytes()).hexdigest()
    if src_digest != out_digest:
        raise SystemExit("output digest does not match the committed asset")


if __name__ == "__main__":
    main()
