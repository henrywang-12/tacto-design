# Components

Anatomy and measurements of each component, as built in `assets/tacto.css` and used in `assets/templates/`. Sizes are at the 1512px artboard (1rem = 16px). Copy the markup from the templates; this file says what each part is for and what not to change.

Contents: Nav · Buttons · Labels and section heads · Chips, dots, spark · Cards · Tiles and rail · Tabs · Lists, points, steps, meta · Numbers · Quotes and people · Logos · Panels · UI fragments · Agent card · Closing band · Footer

## Nav — `.tc-nav`

A white bar that floats: fixed, 16px below the top edge, inside the 64px page gutter, 62px high, 8px radius, no border, no shadow. Left: logo (125px wide), then mono links 42px to its right, 16px padding each. Right: language, phone number (mono), then two small buttons 10px apart: "Login" (`tc-btn--quiet`: white, hairline) and "Book a demo" (`tc-btn--header`: black). Links underline on hover. The bar stays white over black sections and photographs. Below 992px the links and meta hide.

## Buttons — `.tc-btn`

Rectangles, 4px radius, mono capitals 14px weight 400, padding 14px 18px. Black with white text; hover turns the fill orange and the text black in 0.2s.

| Variant | Use |
|---|---|
| `tc-btn` | Default: black |
| `tc-btn--lg` | The hero action: 60px high, 48px side padding, 8px radius, a soft drop shadow that disappears on hover |
| `tc-btn--media` | Second hero action: white, hairline, 8px radius, a 80×48 thumbnail or play mark on the left |
| `tc-btn--header`, `tc-btn--quiet` | The two small nav buttons (padding 10px 12px) |
| `tc-btn--orange` | The one action on a black section or inside an agent card. Hover: white. |
| `tc-btn--white` | On a photograph, an ember panel or the closing band. Hover: orange. |
| `tc-btn--glass` | On a photograph: black at 20%, 30px blur, 0.5px white hairline, with a play triangle. "Watch the mission". |
| `tc-btn--sm` | Inside agent cards and dense UI (12px, padding 8px 10px) |

One primary action per view. Never a pill, never a gradient, never an icon-only button except the round arrows (`tc-arrow`, 40px, 1px outline) of a rail or slider.

## Labels and section heads — `.tc-label`, `.tc-head`

Every headline has a small line above it: either a bare mono label (12px, uppercase, weight 300, black, or 50% white on black) or a chip. Then the headline 32px below (16px in the tight variant), then 50px to the content. Left aligned by default; `tc-head--center` for the product stage and the agents section (label, 24px, headline max 752px, 24px, text max 664px, optional button).

`tc-powered` is the special label: the spark, then "Powered by ..." in 17px sans with the orange-to-blue gradient. Once per page at most.

## Chips, dots, spark

- `tc-chip`: 0.5px hairline (black at 20%), 4px radius, padding 8px 12px 6px, 12px gap, mono 12px. Holds a category, an award, a module name. On black the outline is white at 50%. Variants: `--white` (white fill, no outline, on a veil or photo), `--box` (white fill, tighter: the agent names on the orbit), `--glow` (white with the orange and blue light: the centre of the orbit), `--fade` (trust badges on black at low contrast), `--solid` (black: the active filter).
- `tc-dot`: 5px circle. Black by default; `--orange`, `--blue`, `--sea`, `--green`, `--yellow`. It sits before the text inside a chip or a counter label and carries the category.
- `tc-spark`: the orange four-point star, 12px (24px `--lg`). It marks anything the AI does or powers. `tc-spark-tile` puts it in a 36px hairline square, as the icon of an agent.
- `tc-status`: dot plus mono capitals 11px ("Signed", "Expires soon"). `--box` adds the hairline tag.
- `tc-code`: a part number, file name or index in a hairline tag with a faint fill ("TAC002", "CONTRACT_2026_Q2.PDF"). `--more` is the grey "+3".

## Cards — `.tc-card`

White, 8px radius, 1px outline `#D1D1D1` at 50%, 32px padding, no shadow. A flex column with `space-between`: the chip sits in the top left corner, the title and text in the bottom left, and the middle stays empty. Heights: 544px default, `--tall` 712, `--xl` 800, `--short` 480, `--xs` 380, `--auto` for content height.

| Variant | Use |
|---|---|
| default | Mission, story, feature: chip top, `tc-title-34` and a paragraph bottom (text block max 552px) |
| `--black` | A long quote in `tc-quote` with the person at the bottom; a white customer logo, centred |
| `--grey` | `#F3F3F3`, no outline: a customer logo centred, or a quiet quote |
| `--xl` spanning 12 | The wide card with two `tc-mega` titles in opposite corners and the agent orbit between them |
| with `tc-card__bg` | A photograph filling the card, content on top |

Pair a text card with a picture of the same height (6+6). In the voices grid: black quote 8 + logo 4, then logo 4 + orange card 8.

## Tiles and rail — `.tc-tile`, `.tc-rail`

Upright white tiles, 320 × 448, 28px padding, in a horizontal rail that runs off the right edge, 16px apart. Title (26px) top left, a thin grey line drawing of a part filling the lower two thirds. Hover: the tile fades to 60%. Two round arrows sit right of the section headline.

## Tabs — `.tc-tabs`

A pill menu: half-transparent white, fully rounded, 3px padding, tabs 12.8px sans weight 400 with 12px 18px padding. The active tab is white with the orange and blue glow and may carry the spark. It sits centred between the product fragment and the section head.

## Lists, points, steps, meta

- `tc-list`: capabilities inside a card. Each line 23px with a 1px hairline on its left; the open one gets a black hairline and a 17px description at 50%.
- `tc-points`: rows with a hairline above, a mono label in a 64px left column (a date, "01", a role) and text right. For plans, results and agendas.
- `tc-steps`: three to four boxes in a row (strategy, execution, monitoring): mono label on top, one sentence below. On a photograph or ember they are dark glass.
- `tc-meta`: facts in columns, each with a left hairline: mono label over a plain value. For the fact strip of a story or a one-pager.

## Numbers — `.tc-figure`, `.tc-stats`, `.tc-proof`

- `tc-figure`: a 19px label, then the number at 116px weight 200. One per card.
- `tc-stats`: a row of counters. Each: left hairline, 36px padding, a dot and mono label, then the number at 48px. On black the hairline is white at 16%.
- `tc-proof`: a small white card with the number at 42px weight 200, a two-line mono caption and a 74×66 thumbnail chart. It floats inside the wide card.
- `tc-rating`: eight upright bars, 2px wide. Green filled, grey empty.
- `tc-chart`: one orange line of 1.5px, hairline grid, mono axis text. `tc-bars`: thin horizontal comparison, ours in orange.

Numbers are never coloured, never in a tinted box, never with an icon.

## Quotes and people — `.tc-quote`, `.tc-person`, `.tc-impact`

- `tc-quote`: 36px light, in curly quotes; `--sm` 23px. On a black card (8 columns) with the person at the bottom.
- `tc-person`: an 80px square portrait with 4px radius (37px round in the impact card), name in black or white, role and company below at 30% (50% white on black). `--mono` sets both in 10px mono capitals.
- `tc-impact`: the black card on a full-height photograph or ember: label, the figure, then the quote in `#AEAEAE`, the person in mono, slider bullets (`tc-bullets`, the active one orange).

## Logos — `.tc-logos`, `.tc-logorow`

- On black: a wall of 6 columns, cells 224:172 with 7px radius, white at 2% fill and 4% outline, logos in white at 75% opacity. Hover lightens the cell.
- On light: a quiet centred row, logos grey at 50% opacity, max 115 × 45, 50px apart, under a mono line.
- Until real logos exist, set customer names as text in the cells and say so.

## Panels — `.tc-ember`, `.tc-veil`, `.tc-noir`, `.tc-photo`

The background for anything image-like. See `imagery.md` for when to use which. `tc-panel` adds the stage padding (80px top, 128px bottom) and centres its content. `tc-media` gives a 16:9 slot.

## UI fragments — `.tc-frag`

A piece of product redrawn in HTML: white, 10px radius, 0.5px warm hairline, one soft shadow, 14px text. Head row with the spark tile, a tiny mono overline and a title; body with nested hairline items (`tc-item`), key and value pairs (`tc-kv`) or a table. Entity marks (`tc-ent`) are 20px tinted squares with one small shape: blue square, sea diamond, orange triangle, green circle. A fragment may run off the edge of its panel on purpose; put `data-tc-crop` on the panel so the check knows.

## Agent card — `.tc-agent`

What an agent reports. On black: 540px wide, dark glass with a white 10% outline, spark tile and the agent's name, then one paragraph at 19px in 50% white with the finding in orange, then one small orange button. `--light` is the same on white for light surfaces and documents.

## Closing band — `.tc-band`

Full width, 960px high. A wide photograph (as `<img>`) or the ember streak. Three giant white words at the bottom, one per line (204px, then 160px), and one white button beside the second word.

## Footer — `.tc-footer`

Black. Logo and two certificate lines on the left, then four link columns with mono heads; links 14px at 50% white, white on hover. 180px lower, the base line: copyright at 30% white on the left, legal links on the right.
