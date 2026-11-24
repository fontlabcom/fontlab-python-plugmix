---
this_file: src_docs/md/licence.md
---

# Licence and attribution

The repository retains Apache-2.0 terms and the Apache-2.0/MIT source-specific attribution in its NOTICE. The Extensions pack and compatibility package retain their own source history; the website does not add a new grant for upstream implementation bodies.

- [Download the exact repository LICENSE](assets/LICENSE).
- [Download the exact repository NOTICE](assets/NOTICE).

The site loads theme CSS and JavaScript from the FontLab CDN using fly-january 0.4.0 or later (remote theme assets). The theme wheel includes the same [Apache 2.0 licence](assets/LICENSE) as Plugmix. The MaterialX frontend retains its bundled third-party licences and notices.


## Current English browser payload

The [browser-component record](assets/current-frontend-notices.json) binds the retained MaterialX 10.1.8 browser assets to exact upstream notices, package archives and source maps. Product terms above remain unchanged.

The [English-only omission manifest](assets/english-search-omissions.json) binds all 35 unused lunr-languages 1.20.0 helpers, including Wordcut and TinySegmenter. The build rejects theme/search-language, corpus, vendor-set/hash and local HTML-reference drift before removing them. Seven core MaterialX assets retain their original bytes. Fly rescales the two MaterialX stylesheets to its root font size.

The main source map retains 211 preferred sources, including 128 exact NPM source matches; the worker map retains 13 sources, including Lunr 2.3.9. The exact clipboard distribution embeds its dependencies; select, good-listener and delegate retain their upstream README MIT link and Zeno Rocha attribution, without invented standalone licence text or dates. CSS maps retain source names without embedded source bodies.

Material Design icons retain the Pictogrammers notice and Apache 2.0 icon terms or specifically stated underlying terms; code is MIT. Font Awesome Free retains Fonticons attribution and CC-BY 4.0 terms. Octicons retains GitHub's MIT notice; Lucide retains ISC and inherited notices. Of 45 observed ordered SVG path tuples, 43 match installed MaterialX icon path tuples exactly, including `fontawesome/solid/caret-down.svg` used by `--md-version-icon`. Its unchanged CSS header identifies Font Awesome Free 7.1.0, Copyright 2025 Fonticons, Inc., and CC-BY-4.0 icon terms; the full Font Awesome notice remains available below. The official Font Awesome 7.1.0 NPM caret SVG has different raw path bytes from the installed icon and CSS. The two unmatched Lucide focus/download tuples retain their pinned SCSS attribution. No unchanged-primary SVG, whole-geometry or optimizer-recipe equivalence is claimed.

The browser loads the menu from FontLab, fonts from Adobe Fonts and Google Fonts, and PhotoSwipe 5.4.4 from jsDelivr. The site includes no font binaries. The table retains the original notices and their provenance, including those from the earlier FontLab theme.

| Component / retained terms | Version | Exact full notice or upstream README licence section |
| --- | --- | --- |
| clipboard | 2.0.11 | [LICENSE.txt](assets/current-frontend/clipboard/LICENSE.txt) |
| tiny-emitter | 2.1.0 | [LICENSE.txt](assets/current-frontend/tiny-emitter/LICENSE.txt) |
| escape-html | 1.0.3 | [LICENSE.txt](assets/current-frontend/escape-html/LICENSE.txt) |
| focus-visible | 5.2.1 | [LICENSE.md.txt](assets/current-frontend/focus-visible/LICENSE.md.txt) |
| rxjs | 7.8.2 | [LICENSE.txt.txt](assets/current-frontend/rxjs/LICENSE.txt.txt) |
| tslib | 2.7.0 | [LICENSE.txt.txt](assets/current-frontend/tslib/LICENSE.txt.txt); [CopyrightNotice.txt.txt](assets/current-frontend/tslib/CopyrightNotice.txt.txt) |
| lunr | 2.3.9 | [LICENSE.txt](assets/current-frontend/lunr/LICENSE.txt) |
| material-design-color | 2.3.2 | [LICENSE.txt](assets/current-frontend/material-design-color/LICENSE.txt) |
| @mdi/svg | 7.4.47 | [LICENSE.txt](assets/current-frontend/@mdi-svg/LICENSE.txt) |
| @fortawesome/fontawesome-free | 7.1.0 | [LICENSE.txt.txt](assets/current-frontend/@fortawesome-fontawesome-free/LICENSE.txt.txt) |
| @primer/octicons | 19.25.0 | [LICENSE.txt](assets/current-frontend/@primer-octicons/LICENSE.txt) |
| lucide-static | 1.11.0 | [LICENSE.txt](assets/current-frontend/lucide-static/LICENSE.txt) |
| select | 1.1.2 | [readme.md.txt](assets/current-frontend/select/readme.md.txt) |
| good-listener | 1.2.2 | [readme.md.txt](assets/current-frontend/good-listener/readme.md.txt) |
| delegate | 3.2.0 | [readme.md.txt](assets/current-frontend/delegate/readme.md.txt) |
| MaterialX10.1.8 | retained terms | [materialx-10.1.8-LICENSE.txt](assets/current-frontend/retained/materialx-10.1.8-LICENSE.txt) |
| Retained corresponding terms | retained terms | [apache-2.0.txt.txt](assets/current-frontend/retained/apache-2.0.txt.txt) |
| Retained corresponding terms | retained terms | [cc-by-4.0.txt.txt](assets/current-frontend/retained/cc-by-4.0.txt.txt) |
| Retained corresponding terms | retained terms | [w3c-focus-visible.txt.txt](assets/current-frontend/retained/w3c-focus-visible.txt.txt) |
| Retained corresponding terms | retained terms | [mit-basecoat-css.txt.txt](assets/current-frontend/retained/mit-basecoat-css.txt.txt) |
| Retained corresponding terms | retained terms | [mit-daisyui.txt.txt](assets/current-frontend/retained/mit-daisyui.txt.txt) |
| Retained corresponding terms | retained terms | [mit-tailwindcss.txt.txt](assets/current-frontend/retained/mit-tailwindcss.txt.txt) |
| Retained corresponding terms | retained terms | [ofl-roboto.txt.txt](assets/current-frontend/retained/ofl-roboto.txt.txt) |
| Retained corresponding terms | retained terms | [ofl-robotomono.txt.txt](assets/current-frontend/retained/ofl-robotomono.txt.txt) |
