# Motion

Two sources. The everyday motion is measured from tacto.ai (Nov 2026): slow, even and rare, one curve, two durations. The scroll scenes are read from Tacto's Atoms & Bits site (atomsandbits.ai, Nov 2026), where one page tells one story as you scroll.

Contents: Everyday motion · Rules · Scroll scenes · When a page gets a scene · Building one · Looking at it · Never

## Everyday motion (every page has this, and most pages have only this)

| What | How | Timing |
|---|---|---|
| Content entering the view | rises about 24px and fades in, once (`tc-reveal`) | 0.6s, slow start and slow stop (`--tc-ease`, GSAP power3.inOut) |
| Groups (cards in a grid, counters) | the same, one after another (`data-tc-stagger`) | 0.08s apart |
| Counters | count up from 0 once when they scroll in (`data-tc-count`) | 1.2s, same curve |
| Button hover | black turns orange, text turns black; the large button loses its shadow | 0.2s |
| Nav link hover | underline | instant |
| Link and footer hover | colour only | 0.2s |
| Card and tile hover (when it is a link) | fades to 60% | 0.2s |
| Glass button hover | darkens and shrinks to 98% | 0.2s |
| Logo cell hover | fill lightens | 0.3s |
| Tabs | the active pill moves; panes cross-fade | 0.6s |
| Logo marquee | runs left at constant speed, never stops | 20 to 25s per loop |
| Slider (impact card) | the card content and the background photograph change together; bullets show the position | 0.6s |
| Dropdown menus | the white panel opens below the nav bar | 0.2 to 0.6s |

`assets/tacto.js` implements the first three, the tabs and the rail arrows. The rest is CSS in `tacto.css`.

## Rules

- One curve for everything that moves: `cubic-bezier(0.645, 0.045, 0.355, 1)`. Two durations: 0.2s for hover, 0.6s for anything that travels.
- Things appear once. Scrolling back up does not replay them.
- Movement is short: 24px at most. Large things (bands, panels) only fade.
- With `prefers-reduced-motion`, everything is simply there.
- In a deck, a PDF or an image nothing moves. Do not add slide transitions or build animations to a deck.
- Only `transform` and `opacity` move. Never animate size, position or colour of a layout box.

## Scroll scenes

What the Atoms & Bits page does, and what `assets/tacto-scroll.js` and `assets/tacto-3d.js` give you:

| Pattern | On their page | Here |
|---|---|---|
| A pinned stage with chapters | the stage stays while "Atoms", "Bits", "Connect", "Explore" follow each other | `data-tc-scene` with `data-tc-step` chapters |
| One object carries the story | a metal star turns, breaks into pieces and comes back | a `tc-part` with `data-explode="scroll"`: it comes apart as the scene advances |
| A pinned list | the speaker names stay, the current one is orange | `tc-scene__list` |
| Giant type that drifts | "Atoms & Bits" crosses the first screen | `tc-giant tc-cross` with `data-tc-progress` |
| A huge number arriving | "25%" fills the screen | `tc-figure tc-swell` with `data-tc-progress` |
| Background that moves slower | the machined-metal picture behind the agenda | `tc-drift` with `data-tc-progress` |
| Text | rises 24px and fades, once | `tc-reveal`, as everywhere |

The page's own scrolling is never taken over: no smoothed scrolling, no snapping, no scroll speed changes. A scene only decides what is shown at each point of the reader's own scroll.

## When a page gets a scene

A scene is the exception. Use one when all of this is true:

- The page tells one story with a beginning and an end: a launch, an event, an explainer, the opening of a prototype. Not a page people come to for reference.
- There is one thing to show changing: an assembly coming apart, a process in four stages, a number growing. If you cannot name it in five words, there is no scene.
- The reader has time. Not on a pricing page, a form, a login, a long article.

And then:

- **One scene per page**, three to five chapters, one screen of scrolling per chapter (`--tc-screens: 4`). Never two scenes in a row.
- Chapters are short: a mono count, a headline of about five words, two lines of text.
- Everything outside the scene stays calm: reveals and nothing else. One `tc-cross` or `tc-swell` on the page is plenty.
- **Never in the product screen** (`.tc-app`): a dashboard does not animate on scroll. There a 3D part turns and can be exploded by a button.
- Never in a deck, a document, an email or a cover.
- When in doubt, leave it out. A page with good type and one still picture beats a page that moves for no reason.

## Building one

```html
<section class="tc-scene--black" data-tc-scene style="--tc-screens: 4">
  <div class="tc-scene__stage">
    <div class="tc-scene__steps">
      <div class="tc-scene__step" data-tc-step>
        <span class="tc-scene__count">01 / 04</span>
        <h2 class="tc-display">It ships as one unit.</h2>
        <p class="tc-text-19 tc-muted">Two lines that say what the reader is looking at.</p>
      </div>
      <!-- three more steps -->
    </div>
    <div class="tc-part" data-tc-part="unit" data-status="false" data-theme="dark" data-explode="scroll" data-turn="-0.5"
         data-dust data-highlight="Housing|Gear|Cover" data-highlight-from="0.76"></div>
    <span class="tc-scene__bar"></span>
  </div>
</section>
<script src="tacto-scroll.js"></script>
```

- `tc-scene__stage` is the pinned screen: two columns (text, object). `--solo` for one column.
- The script sets `--p` (0 to 1) on the scene and `.is-active` on the current step. Anything else you want to tie to the scene can read `--p` in CSS (`transform: scale(calc(1 + var(--p) * 0.2))`) or listen to the scene's `tc:progress` event.
- `tc-scene__bar` is the thin orange line that shows how far the scene has come.
- While a scene holds the screen the nav fades out, so the stage is clear. It comes back when the scene ends.
- On the object: `data-dust` lets fine specks (white, a few orange and blue) spread as it comes apart, which is the Atoms & Bits feeling of something dissolving into bits. `data-highlight="Housing|Gear|Cover"` with `data-highlight-from="0.76"` turns the named parts orange from that point on: when the last chapter says "the three that cost too much", the picture must show which three.
- Chapter headlines are large (`tc-display`) and white; the two lines under them are lighter, not smaller.
- After a black scene, one flat orange section (`tc-section--orange`, black type) is the strongest change of key the page has. Use it once, for the one number or sentence the story was leading to.
- `tc-scene--black` for a scene on black. On the grey page leave it off and drop `data-theme="dark"`.
- Things outside a scene that should move with the page get `data-tc-progress` and one of `tc-drift`, `tc-cross`, `tc-swell`.
- Movement is eased towards the scroll position, so it never jumps and never lags more than a moment.

**The still version is the page.** With reduced motion, without the script, in a screenshot and in `tacto_check.py`, a scene is an ordinary section: the chapters stand under each other beside the object, which rests half apart. Write and lay out the chapters so that this reads well. Then the moving version is a bonus, not a risk.

Template: `assets/templates/scroll-story.html`.

## Looking at it

A plain screenshot shows the still version. To see the moving page at a given scroll position:

```bash
TC_MOTION=1 scripts/shoot.sh out.html step2.png 1440 900 1800
```

The last number is how many px the page is scrolled down. Take one picture per chapter (the scene starts where the hero ends; each chapter is one screen further) and read every one: is the right chapter shown, is the object in frame, does nothing sit on top of the text. Do the same at phone width: `TC_MOTION=1 scripts/shoot.sh out.html phone.png 500 900 1800`.

## Never

Bounce or overshoot, typing effects, parallax on text that is meant to be read, spinning or pulsing icons, animated gradients, confetti, hover lifts with growing shadows, scroll-jacking that stops or slows the reader, counters that keep counting, a second scene because the first one worked, motion in the product screen beyond a turning part.
