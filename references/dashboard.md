# Dashboards and product UI

Tacto's product does not look like Tacto's website. The website is Aspekta light, black and orange. The product is Inter in medium and semibold, neutral greys, white cards with a hairline, figures in blue and a sidebar of line icons. Build an app screen with the product system, and never mix the two on one screen.

- **Measured:** the product system in `.tc-app`. It was read from Tacto's product film (tacto.ai/en/product, Nov 2026), frame by frame at source resolution: the sidebar and its icons, the home dashboard, a supplier page, the findings table, an article page, the analytics page. Text widths were matched against the font files, which is how Inter and the sizes were confirmed.
- **Estimated within that:** exact hex values (video compression blurs colour; they were matched to the nearest steps of a neutral grey scale and to the usual blue, emerald, red, amber and fuchsia steps), hairline colour, corner radii to about 2px, and what the cards cut off by the film's frame contain.
- **Not seen:** hover and focus states, dialogs, forms, empty states, dark mode. Do not invent a dark mode.

Templates: `assets/templates/dashboard.html` (home dashboard) and `assets/templates/dashboard-detail.html` (a record page with tabs, KPI cards, a chart and a table). Start from one of them.

Contents: Type and colour · Frame · Sidebar · Icons · KPI card · Market index card · Shortcuts · Map · Controls · Table · Chart · Whose logo goes where · Fragments on a page or slide · Mistakes

## Type and colour

| | |
|---|---|
| Typeface | Inter. 400 for running text, 500 for labels, nav items, card titles and values in chips, 600 for the active nav item, headings, figures, table heads, finding types. Nothing lighter than 400, nothing heavier than 600. |
| Sizes | 11px chips and badges · 12px group labels and second lines · 13px tables and controls · 14px everything else · 16px card titles · 18px section headings · 22px index values · 30px KPI figures |
| Text | `--tca-ink` #0A0A0A · secondary `--tca-muted` #737373 · placeholder `--tca-faint` #A3A3A3 |
| Surfaces | frame and sidebar `--tca-frame` #F7F7F7 · panel and cards white · chips and table head `--tca-fill` #F5F5F5 · active nav item `--tca-line-strong` #E5E5E5 |
| Lines | card and panel hairline `--tca-line` #EBEBEB · control outline #E5E5E5 |
| Black | `--tca-primary` #171717: the one filled button on a screen |

Colour carries meaning. Use the tone classes (`is-blue`, `is-green`, `is-red`, `is-amber`, `is-pink`, `is-fuchsia`, `is-cyan`, `is-lime`, `is-violet`, `is-orange`, `is-muted`) on the text or the icon:

| Tone | Means |
|---|---|
| blue #2563EB | a figure (every KPI value and its change), the first chart series, a record's icon |
| red #B91C1C | a price that rose, a risk |
| green #047857 | a price that fell, money saved (the savings pill) |
| pink, lime, green, amber, violet, cyan, blue | the type of a finding: each type keeps one colour everywhere it appears |
| fuchsia #C026D3 | the second chart series, the findings tile |
| orange #FF6414 | Tacto's spark, and anything the AI produced (a target price, the agent button) |
| grey | last period, units, ids |

A change is not coloured by its sign on a KPI card: the figure and its change are both blue. Red and green are for prices and money only.

## Frame — `.tc-app`

| Part | Class | Notes |
|---|---|---|
| Frame | `tc-app` | Grey. Two columns: 244px sidebar, fluid main. Root pinned to 16px; sizes in px. |
| Panel | `tc-app__main` | White, 12px corners, hairline, inset 8px from the top, right and bottom of the frame |
| Top bar | `tc-app__top` | 48px, hairline below. A title (`tc-app__title`, 14px medium) or a breadcrumb (`tc-app__crumbs`: parent in grey, chevron, the record's icon, its id in grey, its name). Page actions on the right (`tc-app__actions`). |
| Content | `tc-app__content` > `tc-app__page` | 40px above, 24px at the sides, at most 1184px wide, 40px between sections. `tc-app__content--flush` for a full-bleed table. |
| Section | `tc-app__section`, `tc-app__h`, `tc-app__lead` | Heading 18px semibold, one grey line under it |
| Card | `tc-app__card`, `tc-app__card-title` | White, hairline, 12px corners, 16px padding. `--bare` when a table fills it. No shadow. |

Look at an app screen at 1440x960 (`scripts/shoot.sh out.html out.png 1440 960`). Below that height the nav scrolls, as it does in the product.

## Sidebar — `.tc-app__side`

Top to bottom, as in the product:

1. **Workspace switcher** (`tc-app__ws`): a 32px slot for the workspace's own mark, its name in semibold (cut with an ellipsis after about 13 letters), `chevron-down`, and `panel-left` at the far right.
2. **Nav** (`tc-app__nav`): rows of 28px with 4px between (`tc-app__item`), a 16px icon in grey, 14px medium text. The open page is a grey pill with semibold text (`is-active`). The search row is grey and regular (`tc-app__item--quiet`). Counts are small grey badges (`tc-app__count`). A row that opens gets a `chevron-down` (open) or `chevron-right` (closed) at the right.
3. **Second level** (`tc-app__sub`): no icons, hung on a hairline under the parent's icon.
4. **Group labels** (`tc-app__label`): 12px grey with a small chevron: "Supply chain data", "Tools".
5. **Foot** (`tc-app__side-foot`): the maker's logo, a dot, the `bug` icon, and the help button at the right.

Tacto's own nav, in order, with its icons:

| Item | Icon | | Item | Icon |
|---|---|---|---|---|
| Search | `search` | | Order confirmations | `list-checks` |
| Dashboard | `layout-grid` | | Analytics | `chart-no-axes-column` |
| Tasks | `square-check-big` | | Savings → Dashboard, Findings, Opportunities | `piggy-bank` |
| Notifications | `bell` | | RFQs | `handshake` |
| Suppliers | `building-2` | | Drawing Analysis | `drafting-compass` |
| Contacts | `user-round` | | BOM → Project Pricing, Scenario Analysis, Material Compliance | `list-tree` |
| Articles → Drawing Parts | `scan-barcode` | | Requests | `arrow-left-right` |
| Categories | `tag` | | Evaluations | `clipboard-check` |
| Supply Sources | `network` | | Agents | `bot` |
| Transactions → Orders, Goods Receipts, Invoices, Quantity contracts | `receipt-text` | | Help | `circle-help` |
| Documents | `file-lock-2` | | | |

For another product, keep the structure and choose the icons that say what each item is.

## Icons

Lucide (lucide.dev, ISC licence), the set the product uses. 146 of them ship in `assets/icons/`.

```html
<i data-tc-icon="bell"></i>
```

- The icon takes the text colour and is 16px. Set `width` and `height` for another size (14px in tabs and chips, 22px in a tile).
- `python3 scripts/icons.py` lists the names, `--find chart` searches them.
- Need one that is missing? Save the Lucide SVG as `assets/icons/<name>.svg` and run `python3 scripts/icons.py --build`.
- Never draw an icon by hand, never mix in another icon family, never use emoji. A name that does not exist draws nothing, and the check reports it.

## KPI card — `tc-app__kpi`

Title (14px medium), a period chip (`tc-app__period`, 11px on grey), the figure in blue at 30px semibold with its change in 14px beside it, then last period in grey with its own chip. Numbers are written out in full with separators (€8,432,015, not €8.4M). On a record page the period chip sits to the right of the title (`tc-app__kpi-head`). A value that is words ("30 days net") uses `tc-app__kpi-value--text`. Cards sit in `tc-app__kpis`, at least 220px wide.

## Market index card — `tc-app__index`

Name with an `info` icon, the value at 22px semibold with its unit in grey and an arrow, then either one sentence ("30-day average +11.60% vs. previous 30 days") or three period chips (1D, 7D, 30D) with their changes. A small trend line sits top right (`tc-app__spark`, drawn in the value's tone). Red when the price rose, green when it fell: for a buyer a rising price is the bad one.

## Shortcuts — `tc-app__shortcut`

A 48px tinted tile with a 22px icon (`tc-app__tile`, blue by default, `--fuchsia`, `--green`, `--amber`), a 16px medium title and one 12px grey line. Three or four in a row.

## Map — `tc-app__map`

A grey map with blue supplier dots and a white card floating top left (`tc-app__float`): a title with a count, the newest finding in its type colour (`tc-app__finding`), "Potential savings" with the amount in a green pill (`tc-app__pill`), a thin progress line.

```bash
python3 scripts/map.py --region europe --labels --dot 9.99,53.55,Hamburg --dot 13.40,52.52 > map.svg
```

Then `<div class="tc-app__map"><img src="map.svg" alt="..."></div>`. Regions: europe, dach, uk, nordics, north-america, asia, world, or `--center lon,lat --span degrees`. The outlines are Natural Earth data (public domain).

## Controls

- **Buttons** (`tc-app__btn`): black with white text, 32px, 8px corners. One per screen. `--outline` (white, grey outline) for everything else, `--ghost` for "Add filter", `--sm` (28px) in bars, `--icon` for an icon alone.
- **Tabs** (`tc-app__tab`): outlined pills with a 14px icon; the open one is filled grey with semibold text.
- **Segmented control** (`tc-app__seg`): joined segments with icons; the chosen one filled grey.
- **Filter pills** (`tc-app__filter`): "**Category** is one of **all**", joined by a grey "and" (`tc-app__and`).
- **Search** (`tc-app__search`): outlined field with the `search` icon, at the right end of the filter row.
- **Checkbox** (`tc-app__check`, `is-on`).

## Table

Head row on `#F5F5F5` in semibold; rows of 36px at 13px with hairlines; numbers right aligned (`class="num"`); a head may carry a small coloured icon.

- **Finding type** (`tc-app__type` plus a tone): a `lightbulb` and the type in semibold, both in the type's colour.
- **Chips** (`tc-app__chip`): white pills with a hairline: a coloured 14px icon, the id in grey (`<small>`), the name in medium. `link` in green for an opportunity, `scan-barcode` in green for an article, `tag` in pink for a category.
- **Bar beside a number** (`tc-app__meter`, `--rose`): `style="--v: 62%"`.
- **Foot** (`tc-app__tablefoot`): a count on the left, a total on the right.

Keep a table inside the panel at 1440px: fewer columns, or `tc-app__tablewrap--wrap`.

## Chart — `tc-app__chart`

Grey bars for volume or time (`.bar`), a blue line first (`.line`), a fuchsia line second (`.line--fuchsia`), 2.5px dots on every point (`.pt`), hairline grid, 11px grey labels in Inter. A dot legend above (`tc-app__legend`). Two axes are fine when bars and lines measure different things: say which is which in a comment or the card's lead. At most three series.

## Whose logo goes where

| Place | What goes there |
|---|---|
| Workspace slot, top left | The customer whose data this is: their mark (`<img src="customer.svg" alt="">` in `tc-app__ws-logo`) or two initials (`<b>AG</b>`), then their name |
| Sidebar foot | The maker of the product: a wordmark or `<span data-tc-logo></span>`, which `scripts/inline.py` turns into the real logo, 19px high |

## Fragments on a page or slide

To show product inside a landing page, a deck or a post, do not shrink a whole screen. The website shows product as redrawn fragments in its own type:

- `tc-frag` on `tc-ember` or `tc-veil`, three to six rows, running off the panel's edge (add `data-tc-crop` to the panel),
- or one `tc-agent` card on black,
- or one `tc-proof` card with a thumbnail chart inside a wide white card.

A real screenshot of an app screen (`scripts/shoot.sh`) may also be placed on a panel as an image.

## Mistakes

- Aspekta, mono capitals, ember gradients or orange buttons inside the app. Those belong to the website.
- Inter, blue figures or tinted pills on a page, deck or document. Those belong to the app.
- Weight 700 or more, or light text. Inter is 400, 500 or 600 here.
- A change coloured red or green on a KPI card. Figures are blue.
- Abbreviated money (€8.4M) where the product writes the number out.
- Hand-drawn or emoji icons, or icons from another family.
- Shadows on cards. Only the card floating on the map has one.
- Several black buttons on one screen.
- A dark mode.
