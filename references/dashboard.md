# Dashboards and product UI

Two levels of certainty here, and you should know which you are using:

- **Measured:** the product fragments Tacto shows on its site (tables, agent messages, tags, status dots, rating bars, small charts, a "control tower" with approvals). These are images on the site; their look is reproduced in `tc-frag` and friends.
- **Derived:** the full screen in `assets/templates/dashboard.html`. The real product sits behind a login and was not seen. The template applies the fragments and the site's tokens to a complete app screen. Do not claim it is a copy of Tacto's product.

Contents: What the fragments show · Screen layout · Components · Status language · Numbers · Charts · Agent panel · Fragments on a page or slide · Mistakes

## What the fragments show

- White panels on light grey, hairlines, almost no shadow. Sans text at 13 to 14px, light; column heads in grey sans, not capitals.
- A supplier row: a 20px tinted square with one small shape (blue square, sea diamond, orange triangle, green circle), the name with its legal form, part numbers as mono tags ("TAC002", "SCREW-W22", "+3"), eight upright rating bars in green, a status as dot plus mono capitals.
- Small cards with a plain label and one large light number ("At-risk suppliers 7", "Compliant suppliers 123") over a thin line.
- An orange step line for price development on a hairline grid.
- An agent message in the head of a panel: the spark in a hairline square, a tiny mono overline, a one-line title of what the agent just did.
- One black button with white text for the decision ("Review & approve").
- The greeting line of the control tower addresses the buyer by name and says what is waiting.

## Screen layout — `.tc-app`

| Part | Class | Notes |
|---|---|---|
| Frame | `tc-app` | Two columns: 240px sidebar, fluid main. Page grey `#F5F5F5`. Root pinned to 16px. |
| Sidebar | `tc-app__side` | White, hairline on the right, sticky. Logo top left, then the customer workspace chip. |
| Workspace chip | `tc-app__customer` | The customer's logo or name, plus a mono fact ("14 sites"). Hairline box, 4px radius. |
| Nav groups | `tc-app__group`, `tc-app__item` | Mono group label in grey capitals, items in 14px light sans with a thin line icon and a mono count on the right. Active item: grey fill, black text. The Agents item carries the spark. |
| User | `tc-app__side-foot`, `tc-app__user` | Name and role at the bottom, above a hairline |
| Top | `tc-app__top`, `tc-app__meta`, `tc-app__title` | A mono context line ("Control tower · week 47"), then a two-tone greeting at 26px: what needs the buyer, dimmed |
| Actions | `tc-app__actions`, `tc-app__search` | Search field (hairline, 4px), then ONE black button |
| Tabs | `tc-app__tabs`, `tc-app__tab` | Mono chips with a grey count; the active one is solid black |
| Grid | `tc-app__grid` | 12 columns, 16px gap. Panels span 3, 4, 5, 7, 8 or 12. |
| Panel | `tc-app__panel` | White, 8px radius, card hairline, 20px padding. `--bare` for tables (the head gets its own hairline). `--agent` is black. |

A screen has, top to bottom: the greeting, tabs, a row of four KPI panels, then the agent panel beside one chart, then the main table, then secondary panels.

## Components

- **KPI** (`tc-app__kpi`): plain label (14px), the number at 42px weight 200, then one mono line with a dot that explains it ("● 3.1% of spend"). An optional 48px-high orange step line in the corner (`tc-app__minichart`). No arrows, no green or red deltas.
- **Table**: column heads 13px grey sans, sentence case. Rows 13px with 12px vertical padding and hairlines. First column: entity mark, name, and a small grey second line. Numbers right aligned with tabular figures. Row hover: `#FAFAFA`. One quiet row action on the right ("Open").
- **Tags** (`tc-code`): part numbers, contract names, indices. Two at most, then "+3".
- **Rating** (`tc-rating`): eight bars. Green, or yellow (`--warn`) and orange-hot (`--bad`) for low scores.
- **Facts row** (`tc-app__facts`): under a chart, three or four values with mono labels and left hairlines.
- **Legend** (`tc-app__legend`): mono, a short line sample before each name. Two entries at most.
- **Buttons**: black for the screen's one primary action; `tc-btn--quiet` (white, hairline) for filter, export and row actions.

## Status language

Status is a 5px dot and two or three words in mono capitals (`tc-status`). The dot carries the meaning; the text stays black.

| Dot | Meaning | Words |
|---|---|---|
| green | fine, done | Signed · Low risk · Compliant · Realised |
| yellow | needs attention | Expires soon · In negotiation · Needs review |
| orange | the agent found something, or it waits for you | Awaiting approval · Price increase · Savings found |
| orange-hot | wrong or late | Expired · High risk · Overdue |
| blue | in progress, informational | RFQ sent · In analysis |
| black | neutral | Draft · Archived |

No tinted pills, no coloured row backgrounds, no red.

## Numbers

Currency first and compact (€4.82M, €376k), percent directly after the figure, tabular figures in columns. A number in a KPI is black; the only number that may be orange is the one the agent points at.

## Charts

One orange line at 1.5px, usually a step line; one dashed grey reference line (should-cost, index, target). Hairline grid, mono labels in grey, the last value labelled at the line's end. Bars are thin and horizontal (`tc-bars`), black, with ours or the highlighted category in orange.

## Agent panel — `tc-app__panel--agent`

The black panel is the centre of the screen: it is why the buyer opened it.

- Head: spark tile, "Requires your approval", a mono count.
- Two or three findings (`tc-app__todo`): a mono index, the agent's name in mono capitals, then one or two sentences in 50% white with the fact in orange: what was asked or found, the comparison that makes it matter, what it is worth.
- One button at the bottom: white on black ("Review all three").
- One agent panel per screen.

## Fragments on a page or slide

To show product inside a landing page, a deck or a post, do not shrink the dashboard. Take one fragment:

- `tc-frag` on `tc-ember` or `tc-veil`, three to six rows, running off the panel's edge (add `data-tc-crop` to the panel).
- or one `tc-agent` card on black.
- or one `tc-proof` card with a thumbnail chart inside a wide white card.

## Mistakes

- Bold or medium weights "for hierarchy". Hierarchy comes from size and from grey.
- Coloured badges for status, or a traffic-light column.
- Uppercase column heads in the sans. Capitals are mono.
- Several primary buttons, or a blue link colour.
- KPI cards with icons, sparklines in several colours, or percentage arrows.
- A dark-mode version. The app is light; only the agent panel is black.
- Presenting the derived screen as "Tacto's real product".
