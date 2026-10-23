# Backdrop generators

Each script writes one SVG into the current folder (python3, no dependencies). Run it from this folder:

    python3 kettering.py

The output filenames are the script's own (msu.svg, peacecorps.svg, liberty.svg, kawasaki4.svg, ur.svg, altgeld.svg, apera.svg, kettering.svg). To update the page, paste the new SVG into the `BACKDROPS` constant in `index.html` under the matching stop key, replacing `class="occ"` with `style="fill:var(--bg)"` and keeping any per-stop `style="color:…;opacity:…"` attribute on the `<svg>` tag. See CAREER_PAGE.md, "Background line drawings".
