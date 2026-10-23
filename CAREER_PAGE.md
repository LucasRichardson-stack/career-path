# Career Path Page: Technical Brief

Read this before changing `career-path.html`. It explains how the page works, where to edit content, the problems that have already been solved, and the next feature to build.

## What this is

A one-screen, presenter-friendly web page for a guest talk to a robotics class at Kettering University (campus in Flint, MI). It walks through Luke Richardson's career as eight "stops" on a curved 3D carousel:

1. Michigan State University (B.A., International Relations)
2. U.S. Peace Corps, Kyrgyzstan
3. Liberty Robotics
4. Kawasaki Robotics
5. Universal Robots
6. University of Illinois Urbana-Champaign (M.S., Management)
7. Apera AI
8. Kettering University ("Your turn": advice and Q&A)

Each stop re-themes the whole page in that organization's colors, shows its logo on the card, and slides in a text panel (dates, role, location, favorite project, what I did, what it taught me, skill tags).

The design comes from a PowerPoint "curved carousel" Morph trick. The web version replaced the PowerPoint version because the web can do a true 3D curve, smooth direct jumps between stops, and theme changes that PowerPoint can't.

## File layout

Today the page is a single self-contained file:

```
career-path.html     everything: CSS, markup, JS, logos (base64)
```

Only external dependency: Google Fonts (Big Shoulders Display, Instrument Sans, JetBrains Mono), with system font fallbacks if offline.

Recommended layout once this is in the repo:

```
career/
  index.html          (renamed career-path.html)
  media/
    logos/            logo PNGs pulled out of the LOGOS constant
    kawasaki-weld.mp4
    peace-corps-1.jpg
    ...
  CAREER_PAGE.md      (this file)
  PROJECT_HISTORY.md
```

Pulling the logos out of the inline `LOGOS` constant into `media/logos/*.png` is a good first refactor. They were only inlined because the earlier hosting blocked outside files. On GitHub Pages, relative paths work fine and the HTML drops from about 500 KB to about 30 KB.

## Where to edit content

Everything editable is in the `STOPS` array near the top of the `<script>`. One object per stop, in chronological order.

| Field | Purpose |
|---|---|
| `short` | Label under the waypoint dot |
| `theme` | Key into `THEMES` (page colors for this stop) |
| `logo` | Key into `LOGOS`. If set, the card shows the logo on a plate |
| `plate`, `plateInk` | Card background and text color behind the logo |
| `photo` | Optional image URL. If set, it replaces the logo card entirely |
| `mark`, `c1`, `c2` | Fallback placeholder card (monogram plus gradient) when there's no logo or photo |
| `org` | Organization name (card and big heading) |
| `heading` | Optional shorter big heading (used for Illinois so it fits) |
| `role`, `years`, `place`, `kind` | Panel details. `kind` shows on the card (Education, Service, Industry, Q&A) |
| `project` | "Favorite project" line in the left column. Omit to hide |
| `did` | Main paragraph. Can also be an array: each item renders as a numbered line (used on the Kettering stop) |
| `lesson` | "What it taught me" box |
| `skills` | Array of tag chips |

Content rules:

- Text in `[square brackets]` renders as grey italic placeholder text. Remove the brackets once a value is final.
- Strings use single quotes. Use a curly apostrophe (’) or `\'` inside text.
- `THEMES` and `LOGOS` are single very long lines. Don't hand-edit them; edit them with a script, or refactor the logos out first (see above).

## How it works

### The cylinder

Cards sit on the inside of a cylinder, viewed from near its center, so the side cards angle toward the viewer like the inside of a drum.

- `pos` is a continuous index of the card at center (it can be fractional mid-animation).
- For card `i`, `d = i - pos`, angle `a = -d * step`.
- Transform: `translate(-50%,-50%) translateZ(R) rotateY(a rad) translateZ(-R)`.
- Geometry set in `measure()`: `cardW` from stage size (desktop about 14% of width, phone 32%), `R = cardW * 5.6`, `step = cardW * 1.12 / R`, stage `perspective = R * 1.18`.
- Cards fade out past `|d| > 3.2` and dim with distance.
- The path is linear, not a loop. A career has a start and an end, so the ring doesn't wrap, and dragging past either end meets resistance. (The Seven Wonders demo used a looping ring; a loop was rejected here on purpose.)
- `animateTo(target)` eases `pos` with a cubic ease-out. Duration scales with distance, so long jumps still feel deliberate.

### Waypoints track their cards

The numbered dots under the ring are not evenly spaced. Each one is placed every frame at its card's projected screen x:

```
project(d) = R * sin(d*step) * P / (P - R * (1 - cos(d*step)))    where P = R * 1.18
```

`stepOrigin` (stage center relative to the waypoint row) is measured in `measure()` from bounding rects. The colored fill runs from the first stop to the center. The row has a mask gradient so edge dots fade like edge cards. This replaced an earlier evenly spaced row that drifted out of alignment with the cards.

### Per-stop themes

Each stop sets ten color tokens on `:root` from `THEMES`: `bg, panel, line, text, body, muted, accent, accent-text, on-accent, eyebrow`, plus `color-scheme`. The tokens are registered with `@property` as `<color>`, which is what lets them cross-fade over 0.9s. Without registration, custom properties snap instead of animating.

`accent-text` exists because some brand colors (UR light blue, Kawasaki red) are too weak as small text on white. Text uses a darker shade; fills use the true brand color.

### Text panel

On stop change, the old panel slides out and the new one slides in, in the direction of travel (`--dir`). The panel has a fixed minimum height so the stage above it never resizes between stops. A taller panel once squeezed the stage and clipped the cards. `measure()` also re-runs after each change as a safety net.

### Input

- Keyboard: Right, PageDown and Space go forward. Left and PageUp go back. Home and End jump to the ends. Standard presentation clickers send PageUp/PageDown, so they work.
- Click any card or waypoint to jump straight to it.
- Drag or swipe the ring.
- Full-screen button (wrapped in try/catch; some browsers refuse it).
- `prefers-reduced-motion` turns off animation.

### Focus

Clicking a card gives it focus. A bug left the browser's focus ring stranded on that card after moving with the arrow keys. Now focus moves to the new center card whenever a card had focus, and the focus style is drawn on the card face (slightly thicker version of the active ring) instead of a separate outline.

## Gotchas already solved

- **Logo overlapping the card name.** The logo image used `max-height: 100%` inside a grid row, which doesn't constrain reliably. Logos are now absolutely positioned inside their row with `object-fit: contain`.
- **Long org names.** Use `heading` for a shorter big title; the full name still shows on the card.
- **Light and dark themes back to back.** Liberty (near-black) to Kawasaki (white) is a big brightness jump on a projector in a dim room. If it's harsh in rehearsal, soften the white themes to an off-white.
- **Stray focus ring.** See Focus above.

## Testing checklist

Run after any change:

- 1366 x 768 (typical projector): every stop, nothing clipped, waypoint dots sit under their cards.
- About 400px wide (phone): page stacks and scrolls, cards readable.
- Click a card, then use the arrow keys: only the center card has a ring.
- Drag past both ends: rubber-bands back.
- A long jump (stop 1 to 7) and mid-animation: dots stay under cards.

## Next feature: media for each stop

Goal: photos and short videos per stop (for example, a Kawasaki robot doing a welding application) without breaking the one-screen layout.

Proposed design:

- New optional `STOPS` field:
  ```js
  media: [
    { type: 'video', src: 'media/kawasaki-weld.mp4', poster: 'media/kawasaki-weld.jpg', caption: 'Spot welding cell, 2019' },
    { type: 'image', src: 'media/kawasaki-team.jpg', caption: 'Training class in Wixom' },
  ]
  ```
- Stops with media show a small "Media" chip in the panel.
- Clicking the chip or pressing Down opens a full-screen viewer in the stop's theme colors. Left and Right step through items, Esc or Up closes and returns to the carousel.
- Videos: `preload="metadata"`, play when shown, pause when leaving. Sound is allowed because opening the viewer counts as a user interaction.
- The clicker keeps moving between stops. Media is opened deliberately with the chip or the Down key.
- Not a scroll-down section: scrolling pushes the carousel off screen in front of the room.
- Optional: a `photo` on the card instead of the logo plate (field already supported).

Media prep:

```bash
# 720p H.264, small and web-friendly; drop -an to keep audio
ffmpeg -i input.mov -vf "scale=-2:720" -c:v libx264 -crf 26 -preset slow -movflags +faststart -an media/kawasaki-weld.mp4
# poster frame
ffmpeg -ss 2 -i media/kawasaki-weld.mp4 -frames:v 1 -q:v 3 media/kawasaki-weld.jpg
```

Images: resize to about 1600px wide, JPEG or WebP.

## Hosting

- GitHub Pages serves the page and media from the same site, so relative paths just work.
- GitHub limits: 100 MB per file (warning above 50 MB). Keep clips short and compressed.
- Don't use Git LFS for files the site has to serve; Pages doesn't serve LFS objects.
- Pages sites are public even from a private repo. Only publish footage you have rights to (own recordings, or footage the company allows to be shared).
- For the talk itself, run locally from the repo folder (HTML plus `media/`) so the campus network can't stall a video.

## Open content items

- Typos in current text: Liberty "lesson anxiety" (lessen), "commericial" (commercial); Illinois "bettter", "utilizized"; Kettering advice 3 "and or" (and/or).
- MSU "did" line could read: "I wanted to make a global impact, so I set out to be a diplomat in the Foreign Service."
- `years` for MSU and Illinois are still in brackets, and so is "[Online]" in the Illinois location, so they show as grey placeholders.
- Kettering stop has no `project` line (optional).
- Media files and captions to be supplied per stop.
