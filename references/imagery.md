# Imagery

What pictures look like in this design language, and how to make them when you have no photographer. Measured from tacto.ai (Nov 2026): the panel recipes are reconstructions of its background images, built in CSS.

Contents: Which surface for which content · Ember · Veil and noir · UI fragments · Photography · Line drawings · The spark and the orbit · Giant type as a picture · Charts · Covers · Logos · What never appears

## Which surface for which content

| You are showing | Put it on |
|---|---|
| A piece of the product (table, agent message, form) | `tc-ember` (dark, dramatic) or `tc-veil` (light, on the product stage) |
| A real photograph | `tc-photo`, full bleed in a card-sized box, 8px radius |
| A number and a voice | `tc-impact` (black card) on a photograph or `tc-ember--streak` |
| A single huge digit | `tc-ember--full` (the orange card) |
| A diagram, a data map, agents at work | black (`tc-section--black` or `tc-noir`) with white hairlines |
| A technical part | a thin grey line drawing on a white tile |
| A title for a post or a slide | `tc-cover` / `tc-slide--ember` / `tc-slide--black` |

Nothing image-like sits on a flat coloured rectangle, and nothing floats on the grey page without a card or panel around it.

## Ember

The signature. Black that burns into orange from one lower corner, with heavy film grain: in the transition the orange breaks up into specks. White UI fragments float on it and may be cut off by its edge.

- `tc-ember`: light from the lower left. `tc-ember--right`: lower right. Choose the corner away from the content.
- `tc-ember--streak`: a soft diagonal cloud of light, dark all around, for wide full-bleed sections and the closing band. Never a hard-edged band.
- Orange is rare. One or two orange surfaces on a page (an ember panel, the closing band, an orange section), not one in every section: the check warns from the third.
- `tc-ember--full`: solid orange with soft lighter streaks: one per page, for the giant digit and a short quote in white.
- Text on ember is white. Labels in mono, 50% white for secondary lines.
- For PowerPoint, Figma or an image editor: `python3 scripts/panel.py out.png 1920 1080 [--right|--streak|--full]`.

At most two ember panels in one view. If everything glows, nothing does.

## Veil and noir

- `tc-veil`: the page grey with a soft orange light on the left and a soft blue light on the right. The product stage under the hero sits on it (10px radius, 80px top and 128px bottom padding): a fragment, the pill menu, then the centred head.
- `tc-noir`: black with a faint light from the top right and grain. For counters, agent cards, a data map, the quiet half of a deck.

## UI fragments

The site never shows a full screenshot. It shows a fragment: one table with five rows, one agent message, one card with two numbers. Rebuild it in HTML with `tc-frag` (see `components.md`) rather than pasting a screenshot.

- White, 10px radius, soft shadow, 14px text, hairlines between rows.
- Three to six rows. Real-looking content: supplier names with a legal form, part numbers in mono tags, a status with a dot, eight rating bars.
- The fragment is larger than its panel and runs off the right or bottom edge. Add `data-tc-crop` to the panel when you do that.
- One fragment per panel. Two may overlap (a table and an agent message on top) but never three.
- Names in fragments are invented and plausible (Kessler Antriebe GmbH, Varga Precision s.r.o.). Never a real company that is not the user's customer.

## Photography

The site's photographs are of industry: a hand holding a cast part against a caliper, a production cell behind a mesh fence, a worker with a badge on the shop floor, a laptop on a workbench, the founders on a grey sofa. Cool or neutral light, shallow depth, greys and steel blues with the occasional orange or teal object. No stock handshakes, no people pointing at screens, no rendered robots.

- Full bleed in its box with `object-fit: cover`, 8px radius, no border.
- Text on a photograph sits bottom left on a dark fade (`tc-photo--fade`), or in a glass button in the middle ("Watch the mission").
- A customer's logo on their photograph: white, bottom left, about 100px wide.
- You cannot generate or download such a photograph here. Use `tc-photo tc-photo--empty` with a mono caption that says which picture belongs there ("Photo: casting cell at the Verden plant"), or use an ember panel instead, and tell the user what to supply.

## Line drawings

Industries and parts are shown as thin technical drawings: one stroke of 1px in `#D1D1D1`, no fill, cropped by the tile so that only part of the object is visible (a flange, a circuit board, a wheel, a vial, a carton). Draw them as SVG with class `tc-lineart`; keep to circles, straight lines and a few arcs, as an engineering sketch would. They are never coloured and never shaded.

On black, the same idea in white hairlines at 10 to 30%: a grid of dots, boxes joined by lines, labels in mono ("Global data", "Company data", "FX rates", "Drawing parts").

## The spark and the orbit

- The spark (`tc-spark`) is the mark of the AI: orange, four points, 12 to 24px. It appears in chips, in the head of a fragment, as an agent's icon, before the "Powered by" label. It is the published skill's own drawing of a common sparkle shape, not Tacto's logo; with a private brand folder the real logo replaces wordmarks, and the spark stays as the AI marker.
- The orbit (`tc-orbit`): a tilted ellipse drawn as a 1px line with the orange-to-blue gradient. Four agent chips sit on it (each with its own dot colour) and a glowing chip sits in the centre. One per page, inside the wide card.

## Giant type as a picture

Three devices use type instead of an image:

- The closing band: three words at 160 to 204px, white, weight 300, one per line.
- The outline word: one word at 267px with no fill and a 1px stroke at 20% white, across a black section, partly behind the content.
- The digit: a single numeral at 300px on the orange card.

Each at most once per page.

## Charts

Charts are small and quiet: they prove a card's claim, they are not dashboards.

- One line, orange, 1.5px, often a step line (prices change in steps). A second, dashed grey line for the reference (index, target).
- Hairline grid in `#E4E2DF`, no axes drawn, mono labels 10px in grey.
- Thumbnail charts in a proof card are 74 × 66 on `#F3F3F3`: one line or seven thin bars, no labels.
- Comparisons: thin horizontal bars (`tc-bars`), black for the others, orange for ours.
- A world or region map is dark grey land on black with tiny white dots; counters sit below it.
- No pie charts, no 3D, no legends with more than three entries, no colour fills.

## Covers

For a post image or a slide title: `tc-cover` (1200 × 1200) or `tc-cover--landscape` (1200 × 627). Ember or noir. Top row: logo left, one chip right. Then either a light white title of at most three lines at the bottom left, with the second sentence dimmed, or one huge figure (300px, weight 200) with a one-line label. Nothing else: no screenshot, no portrait, no icons.

## Logos

- Own logo: white on black and ember, black on white and grey. 125px wide in the nav.
- Customers on black: their logo in white at 75%, in the wall cells. On light: grey at 50% in a quiet row. In a story: white on the hero photograph, bottom left.
- A customer logo is their own file. See `cobranding.md`.

## What never appears

Stock illustrations, 3D blobs, isometric scenes, emoji, icon grids, gradient meshes in purple or blue, glass cards on colourful backgrounds, drop shadows on cards, rounded "pill" tags in tinted colours, full screenshots with browser chrome, avatars in a row, star ratings.
