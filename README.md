# Beldangi Fax Machine LC

Company site for Beldangi Fax Machine LC, a one-person studio in Vermont making
**Toad Stool Labs**, a mushroom lab game built in Godot.

Live: https://bahun-ko-ckusi.github.io/BELDANGIFAXMACHINE/

## Files

| File | What it is |
| --- | --- |
| `index.html` | The page: 3D desk hero, the game, work with us, footer |
| `styles.css` | All styling. Colors and type live in the `:root` block |
| `scene.js` | The interactive 3D desk in the hero (three.js, built from primitives) |
| `404.html` | Not-found page |
| `media/` | Gameplay loops (`grow.mp4`, `cut.mp4`, ~1 MB together) and stills, cut from the beta footage on the game site |

No build step. Edit, commit, push — GitHub Pages serves `main` at the repo root.

## The 3D hero

A desk with three objects you can drag to turn and tap to use: the fax machine
prints a sheet, the petri dish fruits a mushroom, the dev screen boots. Three.js
is loaded from jsDelivr at a pinned version; every object is made from primitives,
so there are no model files to download.

It degrades: no WebGL means the canvas is removed and a gameplay still takes its
place, and `prefers-reduced-motion` turns off the idle drift and bobbing while the
objects stay usable. The three buttons under the canvas do everything the 3D
objects do, for keyboard and screen reader users.
