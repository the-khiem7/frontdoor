# The banner and the GitHub social preview

Two pictures end every run: the README banner and the social preview GitHub shows when the repository link is shared. They come from one signature and are named alike.

## File names

| Picture | Item id and file name | Format |
|---|---|---|
| README banner | `banner` | `banner.webp` and `banner-dark.webp`; with an approved motion, `banner.gif` and `banner-dark.gif` instead |
| GitHub social preview | `banner-social` | `banner-social.png` and `banner-social-dark.png`; always a still PNG, even when the banner moves |

Use these names in every repository, so the next person (or the next run) finds them without asking. A repository that already has a banner under another name keeps its file until the user approves the rename.

## GitHub's rules for the social preview

The user sets it by hand in the repository, Settings, Social preview; no API or file in the repository sets it, so the run writes the file and tells the user to upload it.

| Rule | Value |
|---|---|
| Resolution | at least 640x320 px; 1280x640 px for best display; ratio 2:1 |
| File format | GitHub lists PNG, GIF or JPG and refuses anything else, WebP included, so the renderer's rounded WebP is not used for this picture. This skill uses PNG only: a GIF shows no thumbnail in chat and mail apps that unfurl the link, and a JPG is lossy |
| File size | under 1 MB ("Please upload a picture smaller than 1 MB." is the refusal). A still 1280x640 PNG of an illustrated banner is a few hundred KB, so the limit is no reason to shrink the picture |
| Safe zone | keep a 40 pt border, 80 px at 1280x640, free of anything important (name, tagline, logo); a decoration may run past it and off the edge |
| Template | GitHub's "Download template" on the same page shows the border |
| Corners and border | none: the image is shown as a plain rectangle, so it is square and unframed |
| Light or dark | one image only; take the light one unless the repository's own look is dark |

Why PNG and not JPG: a 1280x640 illustrated banner measured 155 KB as PNG and 90 KB as JPG at quality 90, so JPG saves only about 65 KB, and both are far under 1 MB. PNG keeps thin lines and small text crisp and is not lossy, so the saving is not worth it. Size to aim for: a few hundred KB; when the PNG is over 1 MB, simplify gradients and lines first.

Build it as an `.item` in the source page with the attribute `data-social`, 640 px wide and 320 px high (`style="width:640px; height:320px"`, the renderer's zoom makes it 1280x640). Keep the wordmark and tagline 40 CSS px inside every edge; a decoration that bleeds sits inside an element marked `data-bleed`. `render.py` writes the file, checks the size and the 1 MB limit, and warns when text is inside the 40 px border.

The social picture is its own composition, not the banner scaled: the banner is wide and short (about 1200x420), the social card is 2:1. Reuse the same drawing, centred vertically and larger, rather than pasting the banner onto a plain ground.

Content of the card: the brand name on the left and the branding element (the signature shape) on the right, and nothing else. No tagline, slogan or description under the name: the card is shown as a small thumbnail in chat and mail apps, where a line of small text cannot be read, and the name at a large size can. Make the name as large as the safe border and the drawing allow, and keep it clear of the drawing (a ring or shape running through the letters hurts reading). The README banner may keep its tagline.

## The animated banner: offer it, do not default to it

A moving banner is optional and applies to the README banner only; the social preview is always a still image. Do not build it unless the user approves, and ask before the plan is final, as one labelled question with a recommended default. Without an answer (an automated run), build the still banner.

Brief the user on what the motion would be, in a sentence per option, so they can picture the effect:

| Motion | What the reader sees | Cost |
|---|---|---|
| Sway of the signature shapes | the banner's main shape (rings, gears, a grid) turns a few degrees one way, then back, on a slow sine; the pieces move but never rotate, so logos and icons stay upright | easy; the loop is seamless |
| Draw-on | strokes draw themselves once along their path, then hold and loop back to the start | more frames; a pause is needed so the end is readable |
| Pulse along a path | one highlight travels along the flow or line that the project is about, then restarts | small file; suits a pipeline or a flow |
| Staged reveal | the wordmark first, then the picture, then the tagline, each fading in, then a long hold | the first frame is empty unless the loop starts on the held end |

The tradeoffs to say plainly: the file is 1.5 to 2 MB for the light and the same for the dark; a GIF has 128 colours, no soft edges against the page, no rounded corners and no border; README images cannot honour a reader's reduced-motion setting, so keep the motion slow and small, a peak of about 20 degrees per second and a loop of 6 to 10 seconds; a fast spin made a first test reader dizzy; and the still WebP files stay in the repository so the README can switch back by editing one line.

When the user approves, make the source page expose a function that redraws the banner for a value, for example `drawBanner(angle)` that clears the drawing and places everything again, then run

```
uvx --from playwright --with pillow python -I <skill-dir>/scripts/animate.py <page.html> --root <assets dir> --item banner --call "drawBanner({v})" --name banner --out <assets dir>
```

Place things with coordinates instead of rotating them (rotate a group and the icons on it turn too). Look at a frame near each end of the sway in both themes, and check the file sizes the script prints. The still `banner-social` comes from `frontdoor-illustrate` as above; draw it at the sway's rest position so it reads as a finished picture.

The README markup is the same `<picture>` as for the still banner with `.gif` in place of `.webp`; see `github-readme.md`.
