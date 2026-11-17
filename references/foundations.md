# Foundations

Exact values, measured from tacto.ai (Nov 2026). `assets/tacto.css` implements all of them as `--tc-*` tokens and classes. When a value is needed that is not here, pick the nearest one from this file rather than inventing a new one: the system is calm because it uses so few values.

Contents: The artboard and the rem · Colour · Typography · Spacing and layout · Shape · Elevation · Breakpoints · Print and slide units

## The artboard and the rem

The site is designed on a 1512px artboard where 1rem = 16px, and the root font size follows the window. Everything is written in rem, so the whole page scales like a picture: at 1440px a 45px headline is 42.9px, at 1920px it is 57px.

| Window | Root font size |
|---|---|
| 240 to 479px | 7.78px rising to 16px (phone artboard: 480px) |
| 480 to 991px | 7.74px rising to 16px (tablet artboard: 992px) |
| 992 to 1511px | 10.5px rising to 16px (desktop artboard: 1512px) |
| 1512 to 1919px | 16px rising to 20.38px |
| 1920px and up | 20.38px, container capped at 1920px |

`tacto.css` uses the same curve with a 12px floor. Decks, A4 sheets, covers and the app pin the root to 16px, because a fixed canvas must not change with the window or the printer.

All pixel values below are at the 1512px artboard. Write them as rem (divide by 16).

## Colour

### Neutrals (nearly every surface)

| Token | Value | Used for |
|---|---|---|
| `--tc-black` | `#000000` | Text, primary buttons, black sections and cards, footer. Pure black. |
| `--tc-white` | `#FFFFFF` | Cards, nav bar, text on black, white sections |
| `--tc-paper` | `#F5F5F5` | The page background. A page is grey, not white. |
| `--tc-card-grey` | `#F3F3F3` | Borderless grey card (logo card, quiet quote), chart thumbnail |
| `--tc-fog` | `#FAFAFA` | Table row hover, code tag fill |
| `--tc-line` | `#E4E2DF` | Warm hairline: small cards, dividers, table rows, borders of UI fragments |
| `--tc-card-line` | `#D1D1D1` at 50% | The outline of every white card |
| `--tc-chip-line` | black at 20% | The outline of chips and quiet buttons |
| `--tc-dim` | black at 30% | The second half of a two-tone headline, muted captions |
| `--tc-half` | black at 50% | Meta text, descriptions under a title |
| `--tc-mid` | `#767676` | Quiet label under a product stage, table headers |
| `--tc-grey` | `#AEAEAE` | Secondary text on black (quote body in the impact card) |
| `--tc-white-50` / `-30` / `-10` | white at 50 / 30 / 10% | Secondary text, tertiary text and hairlines on black |
| `--tc-coal` | `#262626` | Hover fill of a logo cell, inactive bullet, photo placeholder |

There is no blue-grey, no slate, no off-black. Black is `#000`.

### Orange (the one brand colour)

| Token | Value | Used for |
|---|---|---|
| `--tc-orange` | `#FF6414` | The spark, button hover, the fact an agent highlights inside a sentence, the action button on black, the orange card, chart lines, text selection in the cookie banner |
| `--tc-orange-hot` | `#FF4F25` | Active slider bullet, a bad rating |
| `--tc-ember-mid`, `--tc-ember-deep` | `#C2410C`, `#5C1C00` | Only inside the ember gradient, between orange and black (reconstructed from the site's panel images) |

Orange is never a section background and never a headline colour. It appears as a small mark, a hover, one sentence, one button on black, or as light inside a panel.

### Signal colours (5px dots, 2px bars, thin lines)

| Token | Value | Seen as |
|---|---|---|
| `--tc-blue` | `#2170EC` | Dot: RFQ agent, spend under management. End colour of the one gradient. |
| `--tc-sea` | `#2ABFC1` | Dot: spend and cost, customers, articles |
| `--tc-green` | `#2ED24F` | Dot: compliance, signed, low risk. Rating bars. |
| `--tc-yellow` | `#FFCC14` | Dot: sourcing, should-cost, production sites, needs attention |

Rules of use:
- A signal colour is a dot next to mono capitals, a rating bar, a chart line or the small shape in an entity mark. It is never a tinted badge, a filled pill, a coloured number or a section tint.
- The four product areas keep their colour everywhere: suppliers orange, spend and cost sea, sourcing yellow, compliance green.
- For status in a table: green = fine, yellow = needs attention, orange = about to go wrong or the agent's finding, orange-hot = wrong.

### The one gradient

Orange into blue at 135°: `linear-gradient(135deg, #FF6414, #2170EC)`. It exists in three places only: the text of the "Powered by ..." label (17px), the hairline of the agent orbit, and as a glow around one chip or the active tab (`--tc-glow`: orange light from the top left, blue light from the bottom right). Never on a headline, a button or a background.

### Panels

| Panel | Recipe |
|---|---|
| Ember | Black, with orange rising from one lower corner (`#FF6414` solid to 30%, through `#C2410C` and `#5C1C00`, gone at 90%), black speckle at 65% and white grain laid over with overlay at 50% |
| Ember streak | The same colours as a diagonal band at 118° |
| Ember full | Solid orange with soft lighter vertical streaks and light grain (the testimonial card with the giant digit) |
| Noir | Black with a faint white light from the top right and grain |
| Veil | Page grey with a soft orange light on the left, a soft blue light on the right, barely visible grain |

For other media, `scripts/panel.py` writes the same panels as PNG.

## Typography

Two families:
- **Aspekta** (Ivo Dolenc, SIL Open Font License) for everything that is read. Weights 300 (text and headlines), 200 (the lightest cut, 250, for numerals and the largest sizes) and 400 (buttons' neighbours, small UI, names).
- **Geist Mono** (Vercel, SIL Open Font License) for every label: uppercase, 10 to 14px, weight 300 (400 on buttons).

Both ship in `assets/fonts/`.

### Scale (at the 1512px artboard)

| Role | Class | Size / line | Weight | Tracking | Notes |
|---|---|---|---|---|---|
| Closing words | `tc-giant` | 160 / 0.9 (first word 204 / 0.8) | 300 | -0.8px | Three words, one per line, white |
| Outline word | `tc-outline-word` | 267 / 1 | 300 | 0 | No fill, 1px stroke at 20 to 30% white, on black |
| Digit as picture | `tc-numeral` | 300 | 300 | -0.03em | One digit on the orange card |
| Figure | `tc-figure b` | 116 / 1 | 200 | 0 | The number in the impact card |
| Mega title | `tc-mega` | 70 / 1 | 300 | -1.6px | Inside one wide card ("Reduce material costs") |
| Page title, large | `tc-title-90`, `tc-title-68` | 90 / 1, 68 / 1.1 | 300 | -1.6px | Product page hero, module names |
| Display: hero and every section headline | `tc-display` | 45 / 1.2 | 300 | -1.12px (hero -0.8px, on black -1.6px) | Two to three lines. Often two-tone. |
| Large quote | `tc-quote`, `tc-title-36` | 36 / 1.2 | 300 | -1.12px | |
| Card title | `tc-title-34` | 34 / 1.3 | 300 | -0.8px | Max width 480px |
| Counter | `tc-stat b` | 48 / 1.1 (3.2vw, 32 to 56) | 300 | 0 | |
| Proof number | `tc-proof b` | 42 / 1.1 | 200 | 0 | |
| Tile title | `tc-title-26` | 26 / 1.3 | 300 | 0 | Industry tiles, app title |
| Small quote, list item | `tc-title-23` | 23 / 1.3 | 300 | 0 | |
| Label above a figure | `tc-text-19` | 19 / 1.5 | 300 | 0 | Also agent card text |
| Body | `tc-text` | 17 / 1.5 | 300 | 0 | The default paragraph |
| Small | `tc-small` | 14 / 1.5 | 300 | 0 | Footer links |
| Tab | `tc-tab` | 12.8 / 1 | 400 | 0 | Pill menu |
| Mono nav | `tc-nav__link` | 14 / 1.2 | 300 | +0.24px | Uppercase |
| Mono button | `tc-btn` | 14 / 1 | 400 | +0.16px | Uppercase |
| Mono caption | `tc-label--13` | 13 / 1.25 | 300 | +0.16px | Two-line caption beside a proof number |
| Mono label | `tc-label` | 12 / 1.3 | 300 | 0 | Above every headline, in every chip |
| Mono name | `tc-label--10` | 10 / 1.5 | 300 | +0.24px | Person and role in the impact card |

Weight rules:
- 300 for everything. 200 for numerals of 40px and more and nothing else. 400 for buttons, tabs, footer certificate titles and the name line in dense UI.
- Never 500 or more. A bold headline is the fastest way to lose the likeness.

Case rules:
- Sentence case, with a full stop when it is a sentence. Headlines are often several very short sentences.
- Uppercase is always Geist Mono and always small. Never uppercase the sans.

Two-tone headlines: the first sentence carries the claim in black, the following sentences are set at 30% black (50% white on black). One headline, two tones; it is the site's most recognisable type gesture.

## Spacing and layout

| Thing | Value |
|---|---|
| Container | full width up to 1920px, 64px padding left and right (16px on a phone) |
| Text column (stories, articles) | 664px (41.5rem), centred |
| Nav | fixed, 16px from the top, inside the gutter: white bar, 62px high, 8px radius, 16px inner padding |
| Hero | 288px above the chip, 160px below the buttons; chip, 16px, headline (80% wide), 64px, buttons |
| Section | 160px above (260px for the airy variant, 80px tight), 100px below |
| Section head | label or chip, 32px, headline, 50px, content |
| Centred head | label, 24px, headline (max 752px), 24px, text (max 664px) |
| Grid | 12 columns, 20px gap. Cards span 6+6, 8+4, 4+8 or 12. |
| Card | 32px padding; heights 544 (default), 712 (tall), 800 (xl), 480 (short), 380 (xs) |
| Card content | chip top left, title and text bottom left, text block max 552px |
| Tile rail | tiles 320 × 448, 16px apart, 28px padding, running off the right edge |
| Logo wall | 6 columns, 16px gap, cells 224:172, 96px below the headline |
| Counters | 4 columns, 24px gap, each with a left hairline and 36px side padding; label, 24px, number |
| Impact card | 480 × 544, padding 32px 37px, on a full-height picture, right aligned |
| Agent card | 540px wide, centred, 192px between cards |
| Closing band | 960px high, words at the bottom, 150px from the edge |
| Footer | 100px above, 32px below; 180px between the link columns and the base line |

Rhythm: a section is mostly air. Cards are tall and half empty on purpose: a chip in the top corner, words in the bottom corner, nothing in between.

Backgrounds alternate by content, not by habit: grey page for the story, black for proof (customers, numbers, agents), white for voices.

## Shape

| Radius | Where |
|---|---|
| 2px | Rating bars |
| 4px | Buttons, chips, code tags, thumbnails, the spark tile, entity marks |
| 8px | Cards, the nav bar, panels, media, large buttons, the impact card |
| 10px | The stage panel, UI fragments |
| 1000px | The tab menu and its tabs, dots |
| 50% | Avatars, round arrow buttons |

Borders: `1px solid #D1D1D180` around cards; `0.5px solid` black at 20% around chips; `1px solid #E4E2DF` inside fragments and on small cards; `1px solid` white at 10% on black. Nothing is 2px.

## Elevation

Flat. These are the only shadows:

| Token | Value | Where |
|---|---|---|
| `--tc-shadow-btn` | `0 10px 16px -3px` black 20% | The large hero button, glass buttons. It disappears on hover. |
| `--tc-shadow-soft` | `0 3.2px 14.4px` black 5% | The white media button |
| `--tc-shadow-frag` | `0 20px 25px -5px` black 10% | UI fragments floating on a panel |
| `--tc-glow` | orange and blue light | One chip or the active tab |

Cards on the page have a hairline and no shadow.

## Breakpoints

991px (everything stacks, nav links hide, 4-column logo wall, 2-column counters) · 767px (3-column logo wall) · 479px (16px gutters, display 40px, closing words 64px). Check 1440px and a phone width.

## Print and slide units

Derived, since the site has neither. The root is 16px on these canvases.

| Web | A4 page | 1280×720 slide | Cover 1200×1200 |
|---|---|---|---|
| Display 45px | title 33/39 | title 52/60 (title slide 104/100) | 104/104 |
| Body 17px | 12.5/19 | 18/27, lead 22/32 | - |
| Mono label 12px | 9.5px | 10 to 12px | 18px |
| Counter 48px | 30/34 | 64px | - |
| Figure 116px | - | 136px | 300px |
| Page margin | 14mm | 64px | 80px |
