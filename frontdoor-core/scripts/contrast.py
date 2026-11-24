#!/usr/bin/env python
"""Print the WCAG contrast ratio of color pairs, so a picture's text contrast is computed, not judged.

    uvx python -I contrast.py <foreground> <background> [<foreground> <background> ...]

Colors are #rgb or #rrggbb. Each pair prints its ratio and PASS for 4.5 or more (normal text), or
LARGE-ONLY for 3 to 4.5, or FAIL below 3. Exit 1 if any pair is under 4.5.
"""
import re
import sys


def lum(hex_color):
    h = hex_color.strip().lstrip("#")
    if re.fullmatch(r"[0-9a-fA-F]{3}", h):
        h = "".join(c * 2 for c in h)
    if not re.fullmatch(r"[0-9a-fA-F]{6}", h):
        sys.exit(f"contrast.py: not a hex color: {hex_color}")
    ch = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    ch = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in ch]
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def ratio(a, b):
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def main():
    args = sys.argv[1:]
    if len(args) < 2 or len(args) % 2:
        sys.exit(__doc__)
    low = False
    for fg, bg in zip(args[::2], args[1::2]):
        r = ratio(fg, bg)
        verdict = "PASS" if r >= 4.5 else "LARGE-ONLY" if r >= 3 else "FAIL"
        low = low or r < 4.5
        print(f"{fg} on {bg}  {r:5.2f}  {verdict}")
    sys.exit(1 if low else 0)


if __name__ == "__main__":
    main()
