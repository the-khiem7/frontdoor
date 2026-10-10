# Verifying the page

Run these in order, and look at the screenshots yourself: the scripts cannot see an empty hero, overlapping text, or copy that does not convince.

## 1. Structure, responsiveness and accessibility

```
uvx --from playwright python -I <skill-dir>/scripts/shoot.py check <root> --page index.html --out <scratch>/shots --axe <path to axe.min.js>
```

`<root>` is the folder that will be served (the repository root or `docs/`). It opens the page at 390, 820 and 1280 px in the light and the dark scheme, scrolls to trigger reveals, saves a full-page PNG each, and prints FAIL or WARN lines. Fix every FAIL. A WARN is a judgment: missing metadata, an `og:image` that is not a file or not 1200x630, and missing alt text should be fixed; a failed request to a font host is expected when offline.

`--axe` injects axe-core in each scheme. Lighthouse only audits the scheme the page starts in, so a dark-theme contrast failure shows up here and nowhere else. The file ships inside the Lighthouse install once step 2 has run once: `find "$LOCALAPPDATA/npm-cache/_npx" ~/.npm/_npx -name axe.min.js 2>/dev/null`. Run step 2 first if the search finds nothing.

For a rough draft, `--widths 1280 --schemes light` writes one screenshot.

The `reduced-motion` PNG is taken after scrolling and must show every section; blank parts mean content depends on motion.

## 2. Lighthouse

```
uvx python -I <skill-dir>/scripts/lighthouse.py <root> --page index.html --preset mobile
uvx python -I <skill-dir>/scripts/lighthouse.py <root> --page index.html --preset desktop
```

The script serves the folder, starts Edge or Chrome itself with a debugging port, runs `npx lighthouse` against it and prints the four scores and the audits that lost points. It starts the browser itself because Lighthouse's own launch of Edge fails on Windows. `npx` downloads Lighthouse into the user's cache and needs no admin rights.

Performance moves 10 points or more between identical runs, mostly with machine load. Run twice, report the range, and fix what the audits name: render-blocking font CSS (see the preload pattern in `page-craft.md`), large images, layout shift. A localhost run cannot show compression or caching, so say that instead of chasing those audits.

## 3. What remains unobserved

Say these in the final report; none was checked here:

- the page on its real Pages URL, including the base path
- the social preview in a real share card
- external links
- behavior in browsers other than the one used
- a real screen reader
