# Formats

One recipe per deliverable. Web formats are measured from tacto.ai; decks, A4 pages, emails and office files are derived (the site has none) and apply the same tokens to a new canvas.

Contents: Landing page · Dashboard · Success story · Customer POV · Deck · Article · Social post · Email · Report or document · PowerPoint and Keynote · Word and Google Docs · Images and Figma · A web page as a PDF · Single-file HTML

## Landing page — `templates/landing.html`

The order of the home page, top to bottom. Reorder or drop sections, but keep each one's inner structure.

1. **Nav**: floating white bar.
2. **Hero**: 288px of air, a chip, the two-tone headline at 45px over about 80% of the width, 64px, two buttons (large black, white media button). Left aligned. No picture in the hero itself.
3. **Stage**: a veil panel with one product fragment, the pill menu of product areas, then a centred head (mono label, headline, three lines of text).
4. **Proof on black**: label and claim on the left, the logo wall (6 columns), then four counters with dots.
5. **Statement**: the "Powered by" gradient label, a headline of four short parallel sentences, then a mission card beside a photograph with a glass play button.
6. **The wide card**: two mega titles in opposite corners, each with a dimmed line and a proof card, and the agent orbit between them.
7. **A story**: photograph with "View success story", beside a card with an award chip, a title and three lines.
8. **Impact**: a full-height photograph or ember streak with the black impact card on the right.
9. **Agents on black**: glowing chip, centred head, orange button, the outline word behind, agent cards one below the other, trust badges.
10. **Industries**: label, headline, round arrows, a rail of tiles with line drawings.
11. **Voices on white**: black quote 8 + logo 4, logo 4 + orange digit card 8, quote 8 + portrait 4.
12. **Closing band**: three giant words and a white button.
13. **Footer**: black.

A shorter page keeps 1, 2, 3 or 6, 4, one of 7 to 9, 12, 13.

## Dashboard — `templates/dashboard.html`

See `dashboard.md`. The product has its own system (Inter, greys, Lucide icons, blue figures), measured from Tacto's product film. Two templates: the home dashboard (KPI cards, market indices, shortcuts, supplier map) and `dashboard-detail.html` (breadcrumb, tabs, KPI cards, chart, filter row, table). Look at it at 1440x960.

## Success story — `templates/case-study.html`

Label "Success story" → title at 45px (customer, achievement, how) → full-width 16:9 media with the customer's name or white logo bottom left → fact strip (industry, employees, sites, ERP, live since) → the headline figure at 116px with its time frame → a narrow column (664px) with four parts, each opened by a mono label instead of a heading: **Customer description**, **Without us**, **With us**, **Proven impact** → results as hairlined rows that start with the number → one quote on a black card beside the logo → more stories → short closing band → footer.

Paragraphs are short and stand far apart. One smaller picture sits inside the column. Wording: `voice.md`.

## Customer POV — `templates/pov.html`

One A4 page, portrait, 14mm margins, white. It must be readable in ninety seconds and survive being forwarded without you in the room.

1. Top row: the lockup left (our logo × the customer's, see `cobranding.md`); right, in mono capitals: `Point of view · prepared for <Customer> · <month year>`. A value report uses `Value delivered · …` and the same page.
2. Mono label naming the area, then the two-tone title: the outcome with a time frame, then the dimmed half saying how.
3. Fact strip: their facts with mono labels (what they make, sites, purchasing volume, ERP).
4. Two columns: "What we see" (three observations) | "What it costs" (three numbers, light and large).
5. A black band with three or four counters: the outcome.
6. "What we would do": three dated rows (`tc-points`), mono week range on the left.
7. The offer as an agent-style card: spark, one sentence, one button label.
8. Foot in mono: which figures are theirs, what the estimates assume, a contact.

Never run to a second page; cut content instead. The template is already full, so new copy must be as short as what it replaces.

- **Overflow check.** On screen, an orange "A4 ends here" line appears when the content has grown past 297mm. `scripts/tacto_check.py` fails on it.
- **Facts and estimates.** A number the customer gave you stays plain. A number you worked out from their facts, or a target, ends its label with "(est.)" or "(target)". The foot says which is which. Building "What it costs" from their volume and a stated assumption is fine; inventing their volume is not.
- **Date** in the top row: the month the page is sent.
- **Export:** `scripts/shoot.sh pov.html pov.pdf` (A4 PDF). It reports the page count and writes `pov-page-1.png`: look at it, because the PDF is the thing that gets sent.
- **Several pages:** one `<article class="tc-sheet">` per page inside `.tc-sheets`, each with its own top row and foot. Each page must fit by itself; content does not flow from one sheet to the next.

## Deck — `templates/deck.html`

1280×720 slides, 64px padding. Print to PDF for a file (one slide per page). Backgrounds: page grey, white, black, ember. One claim per slide.

| Slide | Build |
|---|---|
| Title | Ember or black. Brand row at the top: our logo left; the lockup with the customer, or the date in mono, right. The title at 104px light at the bottom left, three lines at most, second sentence dimmed. |
| Claim | Grey. Mono label, the two-tone headline at 52px, optionally one lead of two lines at 50% black. Nothing else. |
| Numbers | Grey, white or black. Three counters divided by hairlines at 96px weight 200 (with four they step down to 68px by themselves), or one figure at 136px with its label and whose number it is. Keep each number compact (€640k, not €640,000): the check fails when numbers touch. |
| Product | Split: text left, an ember panel right with one white fragment running off its edge. |
| How it works | Three hairlined rows with mono labels (`tc-points`), or three step boxes. |
| Voice | Black. One quote at 48px, the person below with role and company. Only with a real quote from a named person. |
| Plan | Three step boxes with a dated mono label, a one-word title and one sentence, all marked `is-active` (dim a step only to show where you are); or dated rows; or a comparison as thin bars. |
| Closing | Black or ember. Three giant words, one next step as a white button label, our logo. |

A shorter deck: six slides are title, numbers, product, how it works, plan, closing. Four are title, numbers, plan, closing. Drop the voice slide when there is no real quote and the claim slide when the numbers already make the claim; never drop the closing slide.

Every slide except title and closing has a foot 28px from the bottom: wordmark left, mono page label right ("Northdesk × Hollweg · 03"). Headlines are sentences, three lines at most (the check fails on four). No bullet glyphs, no clip art, no slide transitions.

Export: `scripts/shoot.sh deck.html deck.pdf` and read the page pictures.

## Article — `templates/article.html`

Label "Blog" → title at 45px → a mono byline (author · date · reading time) → wide 16:9 media: an ember panel with one white line drawing and a chip, or a photograph → a narrow column (664px): a lede at 23px, then short paragraphs, light sub-headings at 34px, one sentence pulled out large with a mono cite line, a hairlined list, one figure (a fragment or chart) with a mono caption, optionally one light agent card → author card → "Read next" cards → footer.

## Social post

Text rules: `voice.md` (derived). Image: `templates/cover.html` (1200×1200, feed) or `templates/cover-landscape.html` (1200×627, link previews).

- Ember or noir. Top row: logo left, one chip right. Then either a light title of at most three lines at the bottom left (about 45 characters on the square, 40 on the landscape), second sentence dimmed, or one figure at 300px weight 200 with a caption of one or two lines and, above the caption in mono, whose number it is (`<span class="tc-label">` inside `tc-cover__caption`). Text on the orange part of the panel is full white; dimmed text only where the panel is black.
- The cover says what the first line of the post says.
- Export: `scripts/shoot.sh cover.html cover.png 1200 1200` · `scripts/shoot.sh cover-landscape.html cover.png 1200 627`.
- Naming a real customer in a public post needs that customer's consent; say so to the user.

For a carousel (document post): deck slides at 1080×1350 with the same slide types; first slide ember, last slide black.

## Email

Plain and short. The email itself is nearly unstyled, which is on-brand.

- Font stack `Aspekta, "Helvetica Neue", Arial, sans-serif`, 16/24, weight 300 where the client supports it, colour `#000000`; secondary `#767676`. Max width 600px. Left aligned. White background, no header banner.
- At most: the logo at the top, one headline at 26/32 (light), three short paragraphs, one black rectangular button (`background:#000; color:#fff; border-radius:4px; padding:14px 18px; font-family:"Geist Mono",Menlo,Consolas,monospace; font-size:13px; text-transform:uppercase; letter-spacing:.2px`), a hairline `#E4E2DF`, and a 12px grey footer.
- Numbers may appear as one row of two or three plain figures (30px light with a 11px mono label).
- Use table layout and inline styles for client compatibility. Aspekta will fall back to Helvetica or Arial in most clients, which is acceptable.

## Report or document

A4, portrait, built as `.tc-sheet` pages and printed to PDF.

- Cover: black or ember page, logo top left, a mono label, the title at 44 to 56px light in the lower third, date and author in mono.
- Body pages: white, 14mm margins, 12.5/19 text, section titles 18px light with a mono label above, hairline rules instead of boxes.
- Tables: no vertical lines; hairline row separators; column heads 10px grey sans; numbers right aligned; status as dot plus mono capitals.
- Numbers: a black band with counters once per chapter, not on every page.
- Foot: hairline, document name left, page number right, 8.5px mono.

## PowerPoint and Keynote

When the output must be `.pptx` or `.key`:

| Property | Value |
|---|---|
| Slide size | 13.333 × 7.5 in (16:9) |
| Fonts | Aspekta Light for everything read; Aspekta ExtraLight (250) for big numbers; Geist Mono Light for labels. Both are free: install the desktop fonts from the Aspekta and Geist projects. Fallback: Helvetica Neue Light or Arial; Menlo or Consolas for labels. Never Bold, never Medium. |
| Title | 39pt light, tracking about -2%, line spacing 1.15, `#000000`; 78pt on title and closing slides (line spacing 0.95) |
| Mono label | 8pt, all caps, `#000000` (50% white on black) |
| Lead / body | 16.5pt at 50% black / 13.5pt `#000000`, line spacing 1.5 |
| Big number | 102pt extra light for one figure; 48pt light in a row of counters; label 9pt mono caps with a 4pt coloured dot |
| Margins | 0.67in on all sides; foot baseline 0.3in from the bottom |
| Backgrounds | `#F5F5F5`, `#FFFFFF`, `#000000`, or an ember PNG from `scripts/panel.py out.png 1920 1080` |
| Shapes | Cards: white, corner radius about 0.08in, outline 0.75pt `#D1D1D1` at 50%. Chips: 0.5pt outline black 20%, radius 0.04in. Buttons: black rectangles, radius 0.04in, mono caps. |
| Visuals | An ember PNG for a half-slide panel (corner radius 0.08in) with white rounded rectangles and small text on top |
| Charts | One line 1.5pt `#FF6414`, reference line dashed `#AEAEAE`, gridlines 0.5pt `#E4E2DF` horizontal only, no legend box, 8pt mono axis text |
| Foot | 7.5pt mono caps at 50%: name left, slide label right |

Remove default theme effects: no shadows, no gradient fills other than the ember image, no title underline, no bullet glyphs (use hairline-separated rows with mono labels).

## Word and Google Docs

Styles: Title 26pt Aspekta Light; Heading 1 18pt Light; Heading 2 13pt Light; Normal 10pt Light, 1.5 line spacing, `#000000`; Caption 7.5pt Geist Mono, caps, 50% black. A mono caps label above each heading. Tables with horizontal hairlines `#E4E2DF` only. Page margins 20mm. Accent blocks: black with white text, never tinted colour. Fallback fonts as for PowerPoint.

## Images and Figma

- Backgrounds: `scripts/panel.py out.png W H [--right|--streak|--full|--noir|--veil]`.
- Type on images: white, Aspekta Light, tracking about -2.5%, left aligned, line height 1.0 to 1.2. The second sentence at 50% white.
- White fragments: `#FFFFFF`, radius 10, outline 0.5px `#E4E2DF`, shadow `0 20 25 -5` black 10%.
- Glass: fill black 20%, 30px background blur, 0.5px outline white 20%.
- Chips: 0.5px outline (black 20% or white 50%), radius 4, Geist Mono 12 caps, a 5px dot.
- Export at 2x for retina where possible.

## A web page as a PDF

Do not print a web page or a dashboard to PDF: print lays the page out on a narrow sheet, so it comes out in its phone layout. Send a picture instead (`scripts/shoot.sh page.html page.png 1440 full`), or rebuild the content as `.tc-sheet` pages. Only `.tc-sheet` and `.tc-slide` documents are made for PDF.

## Single-file HTML

`python3 scripts/inline.py in.html out.html` writes one file with the stylesheet, both fonts, the script, the logo and local images inside (about 270 KB before your own images). It needs no network and can be mailed, opened from disk or published as it is. Where a host forbids embedded fonts, the text falls back to Helvetica or Arial and the layout holds.
