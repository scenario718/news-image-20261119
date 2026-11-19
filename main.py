#!/usr/bin/env python3
"""Deliver the picture for the news-image-20261119 bounty.

``entry.png`` sits in this repository next to this file: a single
image summing up the world's news of Thursday 19 November 2026,
painted by the companion generator ``draw.py`` (the README lists
the stories shown). The judging sandbox installs nothing, so this
program sticks to the standard library: it copies the committed
picture to the output location exactly as stored, which also makes
the result deterministic - repeated runs emit identical bytes.
"""

import hashlib
import os
import shutil
import sys

PICTURE = "entry.png"
PNG_SIGNATURE = b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a"


def picture_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        PICTURE)


def digest_of(path):
    with open(path, "rb") as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def emit():
    source = picture_path()
    if not os.path.isfile(source):
        print("committed picture is missing: " + source, file=sys.stderr)
        return 1
    with open(source, "rb") as handle:
        if handle.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            print("committed picture is not a PNG", file=sys.stderr)
            return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    destination = os.path.join(out_dir, PICTURE)
    shutil.copyfile(source, destination)
    # A short copy must never slip through unnoticed: the grader
    # judges exactly the bytes found at the destination.
    if digest_of(source) != digest_of(destination):
        print("copied picture differs from the committed one",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(emit())
