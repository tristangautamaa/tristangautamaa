#!/usr/bin/env python3
"""Generates every SVG used by the profile README.

Numbers come from assets/data.json (refreshed by scripts/fetch_data.py); fonts are subset and embedded
per SVG; colours follow the Storm Navy / Citrus Ember / Glacier Blue palette.
Usage: gen.py [OUTDIR [DATAFILE]]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import content  # noqa: E402
import dashboard  # noqa: E402
import hero  # noqa: E402
import products  # noqa: E402

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "assets")

PILLS = [("PORTFOLIO", "globe"), ("LINKEDIN", "linkedin"), ("GITHUB", "github"),
         ("MIGRAVIA", "diamond"), ("SENSIFY", "diamond"), ("GRIYAPLAST", "diamond")]


def main():
    os.makedirs(OUT, exist_ok=True)
    files = {
        "hero.svg": hero.hero(),
        "now.svg": hero.nowbar(),
        "about.svg": content.whoami(),
        "products-head.svg": hero.heading_svg("02", "PRODUCTS", "Products I've built", "Designed, built and shipped"),
        "product-migravia.svg": products.migravia(),
        "product-sensify.svg": products.sensify(),
        "product-griyaplast.svg": products.griyaplast(),
        "dashboard.svg": dashboard.dashboard(),
        "stack.svg": content.stack(),
        "projects.svg": content.projects(),
        "experience.svg": content.experience(),
        "footer.svg": content.footer(),
    }
    for label, kind in PILLS:
        svg_, _ = hero.pill_svg(label, kind)
        files[f"pill-{label.lower()}.svg"] = svg_
    for n, c in files.items():
        with open(os.path.join(OUT, n), "w", encoding="utf-8") as f:
            f.write(c)
        print(f"{n:28s} {len(c) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
