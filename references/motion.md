# Motion

Measured from tacto.ai (Nov 2026). The site runs GSAP with ScrollTrigger, Lenis smooth scrolling and Swiper for its sliders. Movement is slow, even and rare: one curve, two durations.

## The inventory (this is all of it)

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
| Page scroll | smoothed (Lenis) | - |
| Agents section | agent cards scroll past a pinned headline and the outline word | tied to scroll |

`assets/tacto.js` implements the first three, the tabs and the rail arrows. The rest is CSS in `tacto.css`.

## Rules

- One curve for everything that moves: `cubic-bezier(0.645, 0.045, 0.355, 1)`. Two durations: 0.2s for hover, 0.6s for anything that travels.
- Things appear once. Scrolling back up does not replay them.
- Movement is short: 24px at most. Large things (bands, panels) only fade.
- With `prefers-reduced-motion`, everything is simply there.
- In a deck, a PDF or an image nothing moves. Do not add slide transitions or build animations to a deck.

## Never

Bounce or overshoot, typing effects, parallax on text, spinning or pulsing icons, animated gradients, confetti, hover lifts with growing shadows, scroll-jacking that stops the reader, counters that keep counting.
