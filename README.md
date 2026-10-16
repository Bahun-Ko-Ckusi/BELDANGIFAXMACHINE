# Beldangi Fax Machine LC

Website for Beldangi Fax Machine LC, an independent game studio in Vermont making
**Toadstool**.

Live: https://beldangifaxmachine.com (custom domain, `CNAME` file)

## Pages

| File | What it is |
| --- | --- |
| `index.html` | Studio title, Toadstool, screenshots, contact |
| `terms.html` | Terms of Service for Toadstool and this site |
| `privacy.html` | Privacy Policy |
| `404.html` | Not-found page |
| `styles.css` | All styling. Brand colours match the Toadstool site (`:root` at the top) |
| `media/` | Real gameplay: `world.mp4` (giant-mushroom field), `grow.mp4` and `cut.mp4` (lab loops), and stills |

No build step. Edit, commit, push. GitHub Pages serves `main` at the repo root.

When the terms or privacy policy change, update the "Last updated" date at the top
of that page.

## Legal pages

`terms.html` and `privacy.html` on this site and on the Toadstool site are generated
from one script, so the two never say different things. Edit the text in
`tools/build_legal.py`, then run it from your home folder:

```
python3 BELDANGIFAXMACHINE/tools/build_legal.py TOADSTOOLLINK BELDANGIFAXMACHINE
```

and commit both repos. Update `UPDATED` at the top of the script whenever the text changes.
