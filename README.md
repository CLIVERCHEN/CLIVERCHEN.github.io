# Keru Chen's academic homepage

An [AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io) adaptation for Hugo, with publications, brief paper summaries, news and photography.

## Preview

Requires Hugo Extended 0.128 or newer. The current environment has 0.154.5.

```sh
hugo server --bind 127.0.0.1 --port 1313
```

Open http://localhost:1313/. Build the site with `hugo`; the output is `public/`.

## Edit content

- `content/_index.md`: introduction and research interests.
- `data/news.yaml`: news with an ISO `YYYY-MM` date and an optional emoji. Entries are automatically displayed newest first. Verify the event month before adding an entry; conference appearance and acceptance are different events.
- `data/publications.yaml`: titles, authors, venues, one-sentence TL;DRs, and paper links.
- `layouts/index.html`: education and reviewer service.
- `scripts/prepare_photos.py`: curated photo order, captions and homepage selection.
- `docs/CONTENT_SOURCES.md`: factual sources and venue/year corrections.

To regenerate the photo derivatives after adding photographs, install Pillow in your Python environment and run `python3 scripts/prepare_photos.py`. Existing derivatives are reused when the original is unchanged. Originals are retained under `static/img/photography/`; only web derivatives are published. The gallery includes 18 selected photographs and a collapsible archive. The lightbox supports arrow keys, Escape, swipe, and reduced motion, and links still open the image when JavaScript is unavailable.

## Previous site

The previous Hugo layouts, content, configuration and instructions are preserved in `.legacy-hugo-20260928/`. They are not part of the active build. The original `barks` theme remains on disk but is no longer selected. This workspace was not a Git checkout when the redesign began.

The adapted template's license and provenance are under `themes/acad-homepage/`.
