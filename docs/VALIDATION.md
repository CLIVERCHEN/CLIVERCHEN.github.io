# Validation · 28 September 2026

- Hugo Extended 0.154.5 production build completed successfully.
- JavaScript passed `node --check`.
- All 471 internal HTML resource/link references resolved in the production output.
- All 195 photograph records have both thumbnail and large-image derivatives.
- Original photographs are excluded from the published site; the home page's three thumbnails total approximately 175 KB.
- Browser review at desktop size, 390 px, and 320 px: no horizontal content overflow; paper metadata switches to a horizontal row on small screens.
- Browser interactions verified: homepage and gallery lightboxes, next/previous controls, left arrow, Escape, scroll lock, focus restoration, and the 180-photo expandable archive (195 photos available when expanded).
- Browser error/warning log was empty during final checks.
- Native image links work as a progressive fallback. Reduced-motion behavior is included in CSS and the modal-close code; touch swiping is implemented. These two preferences/input modes were reviewed in source, not device-emulated.

The old site is backed up locally. No remote repository or deployed website was modified.

## Photography update · 28 September 2026

- Synced six new files from `src/photography/`, including three selected images.
- Preserved different images sharing the filename `未标题-1.jpg`; gallery now contains 201 unique images, including 18 selected.
- Verified all thumbnail and large-image references resolve in the production build.
- The publishing checkout builds successfully with Hugo Extended 0.154.5 and excludes camera originals and generated build directories from Git.
