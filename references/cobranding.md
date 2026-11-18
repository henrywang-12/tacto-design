# Us and them: your logo and the customer's

How the sender ("us") and a customer ("them") appear together. Measured from how Tacto presents its customers on its site (logo wall, voices grid, success stories, impact slider); the POV, deck and dashboard placements are derived from those.

Contents: Our own logo · Finding the customer's logo · Rules for a customer's logo · Where each logo goes · Naming and facts

## Our own logo

If this installation has a private brand (`brand.local/brand.md` exists), read it first. It names the default company and holds its logo files. You never paste a logo by hand:

- Write the wordmark exactly as the templates do, `<span class="tc-wordmark"><span class="tc-wordmark__mark"></span>Name</span>`, or simply `<span data-tc-logo></span>`.
- Run `python3 scripts/inline.py in.html out.html`. Every wordmark carrying the brand's name (or a template sample name) and every `data-tc-logo` becomes the real logo.
- Dark and white versions are both embedded and `tacto.css` shows the right one: white inside a black section, the footer, a black or ember slide, an ember or noir panel and the closing band; dark everywhere else. Override with `data-tc-logo="dark"` or `"white"`.
- Size it with `font-size` on the element or its parent: the logo is 1.6em tall.

Without a private brand, the wordmark stays as text in the user's company name with a small orange dot. Sizes: 26px type in the nav bar, 26px on a deck's title slide, 14px in a slide footer, 22px at the top of an A4 page, 20px in the product sidebar.

## Finding the customer's logo

```bash
python3 scripts/logo.py "Auerberg Guss"                       # saved logos only
python3 scripts/logo.py "Auerberg Guss" auerberg-guss.example # also the customer's website
```

It looks in the saved logos, then in the private brand's logo source if one is defined, then on the customer's site, and it is strict: it only returns a file the site itself marks as its logo. Read its last lines:

- **A path and a source:** open or screenshot the file and check it is the right company and the full logo before using it.
- **"SITE ICON ONLY":** it found the small mark, not the logo. Fine for the workspace slot in a dashboard sidebar; for anything larger get the real logo.
- **"no logo found":** open the company's website in the browser and take the logo from the page header or the press page, save it next to your file or in `brand.local/customers/`, or ask the user for the file.

Until a real file is in hand, set the customer's name as text in the logo slot (`.tc-clogo-text`) and say so. Never draw, trace or approximate a logo, and never use a different company's mark as a stand-in.

Reference the file by name (`<img class="tc-clogo" src="auerberg-guss.svg" alt="Auerberg Guss">`); `inline.py` finds it in `./logos/` or `brand.local/customers/` and embeds it in the output.

## Rules for a customer's logo

Tacto shows customers in one colour, as a quiet row of equals, not in their brand colours:

- **On black** (logo wall, black card, ember, a photograph): the customer's own white or single-colour version, at 75% opacity in the wall and full white on a photograph. If they publish no white version, put the colour logo on a white tile (`.tc-clogo-tile`); do not recolour it yourself.
- **On the grey card** (`tc-card--grey`, the voices grid): their logo in full colour, centred, about a third of the card's width.
- **In a quiet row on light:** grey at 50% opacity, max 115 × 45.
- Sized by height (`.tc-clogo`): 52px in a story head (`--lg`), 44px in a row (`--md`), 32px on a card (default), 20px inline (`--sm`). Width follows.
- Their own file, original proportions. Never crop, outline, redraw or add effects.
- If the logo already spells the company's name, show the logo alone. If it is a symbol, put the name next to it in text.

## Where each logo goes

| Deliverable | Us | Them |
|---|---|---|
| **Customer POV, value report (A4)** | Top left, as the first half of the lockup | Top-left lockup: `us × them`. Top right, mono: "Point of view · prepared for <Customer> · <month year>". Name repeated in the fact strip. |
| **Deck for a customer** | Title slide top left in the lockup (white on ember or black); small wordmark in every footer; alone on the closing slide | Title slide, in the lockup. Not repeated on every slide. |
| **Dashboard for a customer** | Sidebar foot, 19px high (it is our product) | The workspace slot at the top of the sidebar (`.tc-app__ws-logo`, 32px): their mark or two initials, then their name in semibold |
| **Success story** | Nav and footer | White on the hero media, bottom left; their name in the title and in the fact strip |
| **Voices grid, logo wall on a page** | - | One cell per customer: white on black, or colour on the grey card |
| **Post image** | Small white logo, top left | Named in the title text only; no customer logo on a cover unless they approved it |
| **Article** | Nav and footer | Named in the text |

The lockup (`.tc-lockup`) is: our logo, a small mono "×" at 50%, their logo, on one line with their logo about 1.5 times the height of our type.

```html
<span class="tc-lockup">
  <span data-tc-logo></span>
  <span class="tc-lockup__x">×</span>
  <img class="tc-clogo" src="auerberg-guss.svg" alt="Auerberg Guss">
</span>
```

The design stays ours. A document for a customer does not take on the customer's colours or typeface: their logo is the only element of theirs.

## Naming and facts

- Spell the customer's name the way they do, including capitals and legal form where they use it (the site writes KERN LIEBERS, voestalpine, SUSS MicroTec as those companies do).
- Describe them with the facts of a story: what they make, sites, employees, export share, ERP. Take these from the user or from the customer's own published material, and say which.
- Figures about a customer come from the user or from a source you can name on the page. Estimates are marked "(est.)".
- Material made for the customer themselves (a POV, a value report, their dashboard) may carry their logo. Anything public (a post, a success story, a logo wall) needs the customer's consent first: tell the user.
