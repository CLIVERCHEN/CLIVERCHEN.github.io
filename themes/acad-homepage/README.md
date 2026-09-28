# AcadHomepage for Hugo

This theme is adapted from [Yi Ren's AcadHomepage](https://github.com/RayeRen/acad-homepage.github.io), downloaded on 28 September 2026. The original MIT license is in `LICENSE`.

The upstream Sass source is preserved in `assets/scss/upstream/`. The site's `assets/scss/main.scss` imports the upstream breakpoint/grid helpers, variables, reset, typography, masthead, and sidebar. The corresponding Liquid masthead, sidebar/profile hierarchy, and paper-box pattern have been ported to Hugo templates under the site's `layouts/` directory.

The custom layer refines spacing, type, colors, responsive behavior and paper metadata, and adds photography with a native-dialog lightbox. The original Jekyll crawler, analytics, sample content, jQuery plugins and remote icon fonts are not needed for this Hugo adaptation.
