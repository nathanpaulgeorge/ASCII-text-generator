#!/usr/bin/env python3
"""
ascii_generator.py - Self-contained ASCII text generator (5x7 built-in font).

Features:
  - Size presets: small/medium/large/huge (scales 1/2/4/8)
  - Override with --scale N
  - Choose draw char (e.g., '#' or '█'), spacing between letters
  - Read from stdin or save output to a file
  - No external dependencies

Usage examples:
  - Default (large preset): python ascii_generator.py "Hello, World!"
  - Huge preset:            python ascii_generator.py "Hello" --size huge
  - Explicit scale:         python ascii_generator.py "Hello" --scale 10 --char="█"
  - Save:                   python ascii_generator.py "Hello" -o out.txt
  - Read from stdin:        echo "Hi" | python ascii_generator.py --stdin
"""
from __future__ import annotations
import argparse
import sys
from typing import Dict, List

FONT_5x7: Dict[str, List[str]] = {
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "B": ["11110","10001","10001","11110","10001","10001","11110"],
    "C": ["01111","10000","10000","10000","10000","10000","01111"],
    "D": ["11110","10001","10001","10001","10001","10001","11110"],
    "E": ["11111","10000","10000","11110","10000","10000","11111"],
    "F": ["11111","10000","10000","11110","10000","10000","00000"],
    "G": ["01111","10000","10000","10011","10001","10001","01110"],
    "H": ["10001","10001","10001","11111","10001","10001","10001"],
    "I": ["01110","00100","00100","00100","00100","00100","01110"],
    "J": ["00111","00010","00010","00010","10010","10010","01100"],
    "K": ["10001","10010","10100","11000","10100","10010","10001"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    "M": ["10001","11011","10101","10101","10001","10001","10001"],
    "N": ["10001","11001","10101","10011","10001","10001","10001"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "P": ["11110","10001","10001","11110","10000","10000","00000"],
    "Q": ["01110","10001","10001","10001","10101","10010","01101"],
    "R": ["11110","10001","10001","11110","10100","10010","10001"],
    "S": ["01111","10000","10000","01110","00001","00001","11110"],
    "T": ["11111","00100","00100","00100","00100","00100","00100"],
    "U": ["10001","10001","10001","10001","10001","10001","01110"],
    "V": ["10001","10001","10001","10001","10001","01010","00100"],
    "W": ["10001","10001","10001","10101","10101","11011","10001"],
    "X": ["10001","10001","01010","00100","01010","10001","10001"],
    "Y": ["10001","10001","01010","00100","00100","00100","00100"],
    "Z": ["11111","00001","00010","00100","01000","10000","11111"],
    "0": ["01110","10001","10011","10101","11001","10001","01110"],
    "1": ["00100","01100","00100","00100","00100","00100","01110"],
    "2": ["01110","10001","00001","00010","00100","01000","11111"],
    "3": ["01110","10001","00001","00110","00001","10001","01110"],
    "4": ["00010","00110","01010","10010","11111","00010","00010"],
    "5": ["11111","10000","10000","11110","00001","10001","01110"],
    "6": ["00110","01000","10000","11110","10001","10001","01110"],
    "7": ["11111","00001","00010","00100","01000","01000","01000"],
    "8": ["01110","10001","10001","01110","10001","10001","01110"],
    "9": ["01110","10001","10001","01111","00001","00010","01100"],
    " ": ["00000","00000","00000","00000","00000","00000","00000"],
    ".": ["00000","00000","00000","00000","00000","01100","01100"],
    ",": ["00000","00000","00000","00000","00000","01100","01000"],
    "!": ["00100","00100","00100","00100","00100","00000","00100"],
    "?": ["01110","10001","00001","00010","00100","00000","00100"],
    "-": ["00000","00000","00000","11111","00000","00000","00000"],
    "'": ["00100","00100","00000","00000","00000","00000","00000"],
    ":": ["00000","01100","01100","00000","01100","01100","00000"],
}

SIZE_PRESETS = {
    "small": 1,
    "medium": 2,
    "large": 4,
    "huge": 8,
}

def render_text(text: str, draw: str = "#", scale: int = 1, spacing: int = 1) -> str:
    if scale < 1:
        raise ValueError("scale must be >= 1")
    rows: List[str] = [""] * (7 * scale)
    sep = " " * spacing
    for ch in text:
        key = ch.upper()
        bitmap = FONT_5x7.get(key)
        if bitmap is None:
            # unknown char -> a small placeholder centered
            bitmap = ["00000"] * 7
            bitmap[3] = "00100"
        for r_i, row_pattern in enumerate(bitmap):
            out_row = ""
            for bit in row_pattern:
                out_row += (draw * scale) if bit == "1" else (" " * scale)
            for v in range(scale):
                rows[r_i * scale + v] += out_row + sep
    final = "\n".join(r.rstrip() for r in rows) + "\n"
    return final

def main(argv=None):
    parser = argparse.ArgumentParser(description="Self-contained ASCII text generator (5x7 font). Use --size to make it big.")
    parser.add_argument("text", nargs="?", help="Text to render")
    parser.add_argument("--char", "-c", dest="draw", default="#", help="Draw character (default: '#'). Use a block like █ for denser output.")
    parser.add_argument("--scale", "-s", type=int, help="Scale factor (integer >=1). Overrides --size if provided.")
    parser.add_argument("--size", choices=SIZE_PRESETS.keys(), default="large", help="Preset size (small, medium, large, huge). Default: large.")
    parser.add_argument("--spacing", type=int, default=1, help="Columns between letters (default: 1)")
    parser.add_argument("--output", "-o", help="Write output to file")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    args = parser.parse_args(argv)

    if args.stdin:
        text = sys.stdin.read().rstrip("\n")
    else:
        text = args.text

    if not text:
        parser.print_help()
        return

    scale = args.scale if args.scale is not None else SIZE_PRESETS.get(args.size, 4)
    try:
        out = render_text(text, draw=args.draw, scale=scale, spacing=args.spacing)
    except Exception as e:
        print("Error:", e, file=sys.stderr)
        sys.exit(2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"Wrote ASCII art to {args.output}")
    else:
        print(out)

if __name__ == "__main__":
    main()
