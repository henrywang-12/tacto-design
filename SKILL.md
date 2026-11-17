---
name: tacto-design
description: Makes whatever you produce look and read as if it came from Tacto (tacto.ai, industrial AI for procurement) - their light typography, mono labels, black and orange, grainy ember panels, cards, numbers, product UI, motion and writing voice, measured from the live site. Use this skill whenever the user asks for the Tacto look, style, brand or design language, says "like Tacto", "Tacto style", "on-brand", "make it look like tacto.ai", or mentions tacto.css - and for ANY deliverable made in that context, whatever the format - landing page, website section, dashboard or app UI, success story or case study, customer POV or one-pager, sales or pitch deck, slides, blog article, LinkedIn post and its image, email, report, chart or diagram. Also use it to restyle or review existing work against this design language. If the user has installed this skill and asks for something visual or written for a manufacturing or procurement customer without naming a style, use it.
---

# Tacto design language

An unofficial, measured reconstruction of how Tacto designs and writes. Everything here was read from the live site (computed styles, the stylesheet, page structure, about 6,500 words of copy in English and German), then rebuilt as a stylesheet, templates and rules. Use it so that a page, a dashboard, a deck or a post looks like it came from the same team, not from a generic AI.

Three things the site does not show, and which are therefore derived from the same system rather than measured: the full product screen (the real product sits behind a login; the site shows fragments of it), slide decks, and A4 documents. Say so if the user asks where one of those rules comes from.

## The look, in one paragraph

Industrial, light and confident. One sans typeface, Aspekta, always in **light weight** (300), large and tightly tracked, in short sentences with full stops; the second half of a headline is dimmed to grey. Every small label is Geist Mono in capitals, often with a 5px coloured dot or an orange four-point spark in front. The page is light grey with tall white cards that are mostly empty: a chip in the top corner, words in the bottom corner. Black sections carry the proof: customer logos, huge light numbers, what the agents found. One colour, orange `#FF6414`, appears as a spark, a hover, one highlighted fact, and as light inside grainy black "ember" panels on which white product fragments float. Buttons are black rectangles with mono capitals. The copy is sure of itself and always has a customer and a number at hand.

If a result feels soft, rounded, colourful, bold or chatty, it is off-brand. Make it lighter, squarer, emptier and more certain.

## Workflow

0. **Know who is speaking.** If `brand.local/brand.md` exists in this skill folder, read it now: it names the company everything is made for by default and holds its logo. If the work is for or about a customer, read `references/cobranding.md` and fetch their logo with `python3 scripts/logo.py "<Customer>" [their-domain]`.
1. **Pick the format** from the table below and open its template and the references listed for it. Templates are working files, not inspiration: start from them.
2. **Use the tokens, never invent values.** Every colour, size, radius and spacing you need is in `assets/tacto.css` (and explained in `references/foundations.md`). If you are about to type a hex code or a font size that is not in there, stop and find the token or class. Write sizes in rem: on web pages the root scales with the window as the site does (1rem = 16px at 1512px wide); decks, A4 sheets, covers and the app pin it to 16px. Writing layout CSS (a grid, a width) is ordinary work.
3. **Write the copy in the house voice** before polishing layout - `references/voice.md`. The voice is half of the likeness.
4. **Build it.** Put a wordmark or `<span data-tc-logo></span>` wherever the sender's logo belongs and `<img class="tc-clogo" src="customer.svg">` for a customer's. Write your HTML with `<link rel="stylesheet" href="tacto.css">` (plus `<script src="tacto.js"></script>` on marketing pages; dashboards, decks and one-pagers do not need it), then run `python3 scripts/inline.py in.html out.html`. It finds both files in this skill's `assets/` folder wherever your file lives, embeds the fonts, swaps in the real logo from the private brand, embeds local images, and writes one file that works offline.
5. **Check it.** `python3 scripts/tacto_check.py out.html` and do not go on until it prints PASS. It opens the file in a real browser and fails when a page or slide is too long, when text is cut, when a font, weight or colour is off the system, when capitals are not mono, when copy has emoji, exclamation marks or advert words (English and German), when a logo or image is missing, or when a template sample name is left in. Because it reads the rendered page, content built by a script is covered. Fix every error; read every warning.
6. **Look at it.** The check cannot judge quality. Render with `scripts/shoot.sh out.html out.png 1440 full` and read the image. For a deck or a document, export `scripts/shoot.sh out.html out.pdf` and read the page pictures it writes (`out-page-1.png` …): the PDF is laid out again for print and is the thing that gets sent. If that export exits with an error, the file is not ready. Compare against the checklist at the end of this file.
7. **Deliver**, and state plainly what is placeholder (logos, photographs, numbers you were not given).

## Formats

| You are making | Start from | Read |
|---|---|---|
| Landing page, website, any marketing section | `assets/templates/landing.html` | `components.md`, `imagery.md`, `motion.md` |
| Dashboard, admin, internal tool, app screen | `assets/templates/dashboard.html` | `dashboard.md` |
| Product fragment inside a page, deck or post | stage and agent blocks in `landing.html` | `dashboard.md` (fragments), `imagery.md` |
| Success story, case study | `assets/templates/case-study.html` | `formats.md`, `voice.md` |
| Customer POV, one-pager, brief, value report (A4) | `assets/templates/pov.html` | `formats.md`, `voice.md` |
| Presentation, pitch or sales deck | `assets/templates/deck.html` | `formats.md` |
| Blog article, long-form post | `assets/templates/article.html` | `voice.md`, `formats.md` |
| LinkedIn or social post, post image, cover | `assets/templates/cover.html` (square), `cover-landscape.html` | `voice.md`, `formats.md`, `imagery.md` |
| Chart, diagram, table of numbers | chart in `dashboard.html`, orbit in `landing.html` | `imagery.md`, `dashboard.md` |
| Anything for or about a customer (POV, value report, their dashboard, deck) | lockup in `pov.html` and `deck.html`, workspace chip in `dashboard.html` | `cobranding.md` |
| PowerPoint, Word, PDF, email, Figma, images | - | `formats.md` (translation tables) |

All references live in `references/`. `foundations.md` is the full token table; open it whenever you need an exact value.

## The rules that carry the likeness

Ordered by how much each one contributes. Getting the first five right gets most of the way.

1. **One typeface, light.** Aspekta at weight 300 for everything that is read: headlines, body, quotes. Numerals of 40px and more drop to 200. Buttons, tabs and small UI names are 400. Nothing is ever 500 or heavier: a bold headline is the fastest way to lose the likeness.
2. **Mono capitals for every label.** Geist Mono, uppercase, 10 to 14px, weight 300: the line above a headline, chips, nav, buttons, captions, names under quotes, table tags. Capitals are never set in the sans, and never larger than 14px on a page. Type labels in normal case; the stylesheet sets the capitals.
3. **Short sentences, two tones.** The display size is 45px at line-height 1.2 with tight tracking (about -1px). A headline is one to three short sentences with full stops. The first carries the claim in black; the rest is dimmed to 30% black (`<em>` inside `tc-display`), or 50% white on black.
4. **Black, white, grey, and one orange.** Text is pure black `#000`. The page is `#F5F5F5`, cards are white with one hairline, proof sections are black. Orange `#FF6414` is the only colour that fills anything, and only small things: the spark, a hover, one button on black, one fact inside a sentence, one card. Blue, sea, green and yellow exist only as 5px dots, 2px bars and thin lines.
5. **Ember.** Anything image-like sits on a panel: black burning into grainy orange (`tc-ember`), the soft grey veil with an orange and a blue light (`tc-veil`), or black with grain (`tc-noir`). White product fragments float on it. This is the brand's signature; a screenshot on a flat coloured box is wrong.
6. **Tall, empty cards.** White, 8px radius, 1px hairline, 32px padding, 544 to 800px high, no shadow. Chip top left, title and two lines of text bottom left, nothing in between. Twelve columns with a 20px gap: 6+6, 8+4, or one card across.
7. **Rectangles, not pills.** 4px on buttons, chips and tags; 8px on cards, panels and the nav bar; 10px on product fragments. The only fully rounded things are the tab menu and dots. Buttons are black with mono capitals and turn orange on hover.
8. **Numbers are huge, light and plain.** 116px at weight 200 in an impact card, 48px in a row of counters divided by hairlines, each with a dot and a mono label. Currency first and compact: €640M, 3.2%, 120+. Never coloured, never in a tinted box, never with an icon.
9. **The spark marks the AI.** The orange four-point star stands before anything the agents do or power. An agent speaks in a dark card: what it read, the finding in orange, one orange button.
10. **The copy is certain and industrial.** The buyer decides, the agents do the work. Claims are stated flat and proven at once with a customer and a number. Vocabulary of real procurement: parts, drawing parts, suppliers, RFQs, should-cost, framework agreements, savings. No exclamation marks, no emoji, no advert adjectives. Details and patterns: `references/voice.md`.
11. **Motion is slow and rare.** Things rise 24px and fade in over 0.6s with a slow start and stop, once. Hover is a 0.2s colour change. Nothing bounces.

## Token quick reference

```
black #000000    white #FFFFFF     paper (page) #F5F5F5     card grey #F3F3F3
line #E4E2DF     card outline #D1D1D1 at 50%     chip outline black 20%
dim = black 30%  half = black 50%  on black: white 50% / 30% / 10%   grey #AEAEAE
orange #FF6414   (hot #FF4F25)     ember: #FF6414 > #C2410C > #5C1C00 > black, with grain
dots: blue #2170EC   sea #2ABFC1   green #2ED24F   yellow #FFCC14
gradient (label text, orbit line, one glow only): 135deg #FF6414 > #2170EC

Aspekta 300 (numerals 200, small UI 400)          Geist Mono 300, uppercase
display   45/54   -1.1px          giant     160/144  (first word 204)
mega      70/70   -1.6px          figure    116/116  weight 200
quote     36/43                   card title 34/44   -0.8px
tile      26/34                   small quote 23/30
label txt 19/28                   body      17/25.5
mono: label 12/15.6 · nav 14 +0.24px · button 14 weight 400 +0.16px · name 10

at 1512px wide, 1rem = 16px (root scales with the window on web pages)
container 64px gutters, max 1920 · grid 12 cols, 20px gap · text column 664px
section 160 above, 100 below · head: label, 32, headline, 50, content
card 32px padding · heights 544 / 712 / 800 / 480 / 380
radius 4 button, chip, tag · 8 card, nav, panel, media · 10 fragment, stage · 1000 tab menu
motion 0.6s cubic-bezier(.645,.045,.355,1) · hover 0.2s
```

## Brand, logo and fonts

- **Name and logo.** The published skill carries the design language, not Tacto's trademarks: the templates use sample names ("Northdesk", "Hollweg Präzision", "Auerberg Guss", "Lindqvist Hydraulik", "Jana Petrovic") and a neutral mark (an orange dot before the name). Who you actually write for comes from the private brand folder `brand.local/` (not in the repo): when it exists, its company is the sender of everything by default and `scripts/inline.py` puts its real logo in. Without it, use the company the user names; if they name none, ask once. Sample names never stay in a deliverable (the check fails on them). Do not redraw or trace the Tacto logo, and do not produce anything that presents itself as an official Tacto communication (their name, people, contact details, customers) for someone who is not working with them.
- **The spark.** `tc-spark` is this skill's own drawing of a common four-point sparkle. It marks the AI. It is not Tacto's logo and is not used as one.
- **Typefaces.** Aspekta (Ivo Dolenc) and Geist Mono (Vercel) are both open source under the SIL Open Font License and ship in `assets/fonts/` with their licences. `inline.py` embeds them, so a delivered file needs no network.
- **Real names in public.** Before a real customer is named in anything public (a post, a success story, a logo wall), tell the user it needs that customer's consent.
- **Language.** Write in the language the user writes in, unless they name the audience's language. Set it on the page (`<html lang="de">`): numbers then count up in that language's format and long German words hyphenate. German notes: `references/voice.md`.
- **Customer logos, photographs, figures.** Never invent a customer logo, a testimonial, a certificate or a metric and present it as real. The brand leans on industrial photography that you cannot produce: use the labelled placeholder (`tc-photo--empty`) or an ember panel, and say which photograph belongs there.

## Before you hand it over

Look at the rendered result and answer these honestly:

- Is every headline light (300), in sentence case, with the second sentence dimmed where there are two?
- Is every capital letter run set in mono and small? Any uppercase sans, any label typed in capitals?
- Could you delete any colour without losing information? Is orange limited to small things, and are the other colours only dots, bars and lines?
- Does every image-like thing sit on an ember, veil, noir or photo panel, with grain?
- Are the cards tall and calm, with the chip top left and the words bottom left? Any shadows, pills, tinted badges or icons the templates do not have?
- Is there one primary action per view, as a black rectangle (orange on black)?
- Do the numbers stand alone, huge and light, with a dot and a mono label that says exactly what they count and whose they are?
- Does the copy sound like an industrial company that is sure of itself, with a customer and a number beside each claim? Any "!", emoji, "seamless", "powerful", "excited"?
- Does it still look right on a phone (web: shoot at 500px wide) or printed (deck, one-pager)?
- Did `scripts/tacto_check.py` print PASS, and did the PDF export (if there is one) exit without an error?

## Files

```
assets/tacto.css            tokens and every component (the source of truth for values)
assets/tacto.js             reveal on scroll, count-up numbers, tabs, rail arrows
assets/fonts/               Aspekta 250/300/400 and Geist Mono, with their OFL licences
assets/templates/           landing, dashboard, case-study, pov, deck, article, cover, cover-landscape
references/foundations.md   the artboard, colour, type, spacing, radius, elevation, breakpoints
references/components.md    anatomy and measurements of each component
references/imagery.md       ember, veil, noir, fragments, photography, line drawings, charts, covers
references/dashboard.md     product UI: the fragments the site shows and the full screen derived from them
references/motion.md        what moves, how far, how long
references/voice.md         how the copy is written, with patterns per format, English and German
references/formats.md       recipe per deliverable, and PPTX / DOCX / email / image translations
references/cobranding.md    your logo and the customer's: finding it, sizes, where each goes
brand.local/                private, not in the repo: your company, your logo, saved customer logos
scripts/shoot.sh            render HTML to PNG or PDF (headless Chrome); `full` measures the page height
scripts/tacto_check.py      THE check before delivery: opens the file in a browser; fit, print, look, copy, brand
scripts/tacto_lint.py       the source-only part of that check (markup and CSS); tacto_check runs it for you
scripts/inline.py           one self-contained file: CSS, fonts, JS, your logo and local images embedded
scripts/logo.py             find a company's logo (saved files, brand source, their website)
scripts/panel.py            generate an ember, noir or veil background as a PNG, any size
```
