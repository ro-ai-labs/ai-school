# Author Promotion and Site Fixes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make ai-school.ro promote its author through four sister projects, and fix the broken navigation, language handling and missing metadata found in the 2026-11-13 review.

**Architecture:** One data file (`_data/projects.yml`) feeds four placements: home cards, article author box, About page, footer row. Internal links are built from `site.baseurl` / `site.baseurl_root` instead of `relative_url`, which returns the first language's path on later language builds. A stdlib Python script checks the built `_site` and runs in CI before deploy.

**Tech Stack:** Jekyll 4.3, jekyll-multiple-languages-plugin, Sass, GitHub Actions, Python 3 (check script only).

**Spec:** `docs/superpowers/specs/2026-11-13-author-promotion-and-fixes-design.md`

## Global Constraints

- No new gems. No JavaScript beyond the existing nav toggle.
- Site copy: plain, warm, no em or en dashes. Romanian copy uses diacritics.
- No promotion inside article bodies. No "book a call" buttons, banners or pop-ups.
- The words "No upsells" / "Fara upsell" appear nowhere in the built site.
- Internal `href`/`src` values are root-relative. Absolute `https://ai-school.ro` URLs appear only in `<head>` metadata, share links, `robots.txt`, `sitemap.xml` and `feed.xml`.
- Outbound project links carry `utm_source=ai-school.ro&utm_medium=site&utm_campaign=<lang>&utm_content=<placement>` with placement one of `home`, `article`, `about`, `footer`.
- English lives at `/…`, Romanian at `/ro/…`. There is no `/en/` path.
- Work happens in `/home/mihai/projects/ai-labs/ai-school` on branch `feat/self-promotion-and-fixes`. No push without Mihai's approval. Commits carry no AI co-author trailers.

## Review Focus

1. A Romanian article is translated later (its `translated: false` flag is removed): cards, series links, canonical and hreflang must switch to the Romanian URL with no template change. Pinned by the canonical check in Task 1, which branches on the notice being present.
2. Site viewed over plain `http://` (true until the certificate is issued): every menu, card and switcher link must work. Pinned by the root-relative check in Task 1.
3. A fifth project is added to `_data/projects.yml`: all four placements show it. Pinned by the per-placement count check in Task 1, which reads the count from the data file.
4. A post with no `series` or `series_order`: no series block, no author-box breakage. Liquid guards in Task 2; no current content exercises it, so it is checked by reading the template.
5. A post with no `excerpt_text`: meta description and card fall back to the first paragraph. Liquid fallback in Tasks 5 and 6; checked by reading the template.

---

## File Structure

| File | Responsibility |
|---|---|
| `scripts/check_site.py` (new) | Assertions over a built `_site` directory |
| `.github/workflows/deploy.yml` | Build on PRs too, run the check, deploy only from `main` |
| `_config.yml` | Exclude `scripts/` from the build |
| `_data/projects.yml` (new) | The four projects: URLs and copy per language |
| `_includes/project-url.html` (new) | One project's outbound URL with UTM parameters |
| `_includes/post-href.html` (new) | A post's href, honoring `translated: false` |
| `_includes/date.html` (new) | A date in the page language |
| `_includes/author-box.html` (new) | "About the author" block for articles |
| `_includes/head.html` | Title, description, canonical, hreflang, Open Graph, icons, feed |
| `_includes/nav.html`, `footer.html`, `language-switcher.html`, `article-card.html` | Root-relative links, footer project row |
| `_layouts/home.html`, `articles.html`, `article.html` | Go-further section, series fix, author box, untranslated notice |
| `about.html`, `_i18n/en/about.md`, `_i18n/ro/about.md` (new) | About page in both languages |
| `_i18n/en.yml`, `_i18n/ro.yml` | UI strings |
| `_i18n/ro/_posts/*.md` | Diacritics, `translated: false` |
| `_i18n/en/_posts/*.md` | On-site links between articles |
| `_sass/_projects.scss`, `_sass/_author-box.scss` (new), existing partials | Styles |
| `assets/img/favicon.svg`, `apple-touch-icon.png`, `og-image.png`, `favicon.ico` (new) | Icons and share image |
| `robots.txt`, `sitemap.xml`, `feed.xml`, `404.html` (new) | Crawl files and error page |

---

### Task 1: Build check and CI

**Files:**
- Create: `scripts/check_site.py`
- Modify: `.github/workflows/deploy.yml`, `_config.yml`

**Interfaces:**
- Produces: `python3 scripts/check_site.py <site_dir> [--projects _data/projects.yml]`, exit 0 when all checks pass, exit 1 with one line per failure.

- [ ] **Step 1: Write `scripts/check_site.py`** (stdlib only) with these checks over every `*.html` under `<site_dir>`:
  - `no_en_prefix`: no `href` contains `/en/` on ai-school.ro paths.
  - `root_relative`: outside `<head>`, no `href`/`src` starts with `http://ai-school.ro` or `https://ai-school.ro`, except `linkedin.com/sharing` share URLs.
  - `ro_stays_ro`: on pages under `ro/`, every internal `href` starts with `/ro/`, or is an asset under `/assets/`, or is the language switcher, or is a link marked `data-lang-link="en"`.
  - `switcher`: an English page at `/x/` links to `/ro/x/`; a Romanian page at `/ro/x/` links to `/x/`; both targets exist as files.
  - `internal_targets_exist`: every internal href resolves to a file in `<site_dir>`.
  - `hreflang`: each page has `en` and `x-default` alternates and a canonical; all point at existing files; a Romanian page showing `data-untranslated` has its canonical on the English URL, otherwise on itself.
  - `series_nav`: on `articles/<slug>/` pages no series link points at the page itself.
  - `projects`: N = number of `- id:` entries in the projects file. Home has N links with `utm_content=home`, each article N with `utm_content=article`, About N with `utm_content=about`, every page N with `utm_content=footer`.
  - `meta`: every page has a non-empty `<title>`, `meta[name=description]`, `og:title`, `og:image`.
  - `banned_copy`: no page contains `No upsells`, `Fara upsell`, `Fără upsell`.
  - `files`: `robots.txt`, `sitemap.xml`, `feed.xml`, `404.html`, `assets/img/favicon.svg`, `assets/img/og-image.png` exist.
- [ ] **Step 2: Self-test the script** against a saved copy of the current live site. Expected: FAIL on `no_en_prefix`, `ro_stays_ro`, `switcher`, `series_nav`, `projects`, `meta`, `banned_copy`, `files`.
- [ ] **Step 3: CI.** In `deploy.yml` add `pull_request: branches: ["main"]` to `on:`, add a build step `python3 scripts/check_site.py _site` after the Jekyll build, and put `if: github.event_name != 'pull_request'` on the `deploy` job. Add `scripts/` to `exclude:` in `_config.yml`.
- [ ] **Step 4: Commit** `ci: check the built site and build pull requests`.

### Task 2: Links and language plumbing

**Files:**
- Create: `_includes/post-href.html`, `_includes/date.html`
- Modify: `_includes/nav.html`, `footer.html`, `language-switcher.html`, `article-card.html`, `head.html`, `_layouts/home.html`, `articles.html`, `article.html`, `_i18n/ro/_posts/*.md`

**Interfaces:**
- Produces: `{% include post-href.html post=p %}` → href string with no surrounding whitespace: `{{ site.baseurl_root }}{{ p.url }}` when `p.translated == false`, else `{{ site.baseurl }}{{ p.url }}`.
- Produces: `{% include date.html date=d %}` → `April 1, 2026` in English, `1 aprilie 2026` in Romanian.
- Produces: front matter flag `translated: false` on untranslated posts; attribute `data-untranslated` on the notice element; attribute `data-lang-link="en"` on links that deliberately leave the Romanian site.

- [ ] **Step 1:** Replace every `{{ '/path/' | relative_url }}` for pages with `{{ site.baseurl }}/path/`; the stylesheet and icons use `{{ site.baseurl_root }}/assets/…`.
- [ ] **Step 2:** Language switcher: English → `{{ site.baseurl_root }}/ro{{ page.url }}`, Romanian → `{{ site.baseurl_root }}{{ page.url }}`.
- [ ] **Step 3:** Series navigation: assign `prev_order` / `next_order` with `minus: 1` / `plus: 1` before the loop and compare against those; links use `post-href.html`. Wrap the block so it renders nothing without `page.series_order`.
- [ ] **Step 4:** Add `translated: false` to the three Romanian posts. In `article.html`, when `page.translated == false`, render a notice with `data-untranslated` and a `data-lang-link="en"` link to `{{ site.baseurl_root }}{{ page.url }}`. Cards for such posts link through `post-href.html`, carry `data-lang-link="en"` and show the `articles.in_english` tag.
- [ ] **Step 5:** Dates everywhere go through `date.html`.
- [ ] **Step 6: Commit** `fix: keep navigation inside the current language`.

### Task 3: Strings

**Files:**
- Modify: `_i18n/en.yml`, `_i18n/ro.yml`, `_i18n/ro/_posts/*.md`

**Interfaces:**
- Produces keys used by later tasks: `global.home_title`, `articles.latest`, `articles.view_all`, `articles.in_english`, `articles.untranslated_notice`, `articles.read_in_english`, `projects.title`, `projects.intro`, `projects.about_title`, `projects.about_intro`, `projects.footer_title`, `author.title`, `author.bio`, `author.more`, `author.linkedin`, `about.connect_title`, `about.connect_text`, `about.connect_link`, `notfound.title`, `notfound.text`, `notfound.cta`.

- [ ] **Step 1:** Hero subtitle: "No upsells." → "No sign-up." (`Fără cont.` in Romanian).
- [ ] **Step 2:** Rewrite `ro.yml` with diacritics and Romanian wording for the strings that were left in English (share, copyright, built-with, follow).
- [ ] **Step 3:** Romanian post titles, excerpts and placeholder text get diacritics.
- [ ] **Step 4: Commit** `fix: Romanian diacritics and wording`.

### Task 4: Projects and author

**Files:**
- Create: `_data/projects.yml`, `_includes/project-url.html`, `_includes/author-box.html`, `_i18n/en/about.md`, `_i18n/ro/about.md`, `_sass/_projects.scss`, `_sass/_author-box.scss`
- Modify: `_layouts/home.html`, `_layouts/article.html`, `_includes/footer.html`, `about.html`, `assets/css/main.scss`, `_sass/_footer.scss`

**Interfaces:**
- Produces: `_data/projects.yml`, a list in display order (`lets-talk-ai`, `ai-labs`, `ai-leaders`, `ship-it-with-ai`). Each entry: `id`, `name`, and maps keyed by `en` / `ro`: `url`, `role`, `need`, `blurb`, `tagline`, `cta`.
- Produces: `{% include project-url.html project=p placement="home" %}` → `<url>?utm_source=ai-school.ro&amp;utm_medium=site&amp;utm_campaign=<lang>&amp;utm_content=<placement>`.

- [ ] **Step 1:** Write `_data/projects.yml`. URLs: lets-talk-ai.ro `/` and `/ro/`; ai-labs.ro `/` and `/ro/`; ai-leaders.ro `/en/` and `/`; ship-it-with.ai `/` and `/ro/`. Roles: Founder and co-organizer; Founder; Founder; Author.
- [ ] **Step 2:** Home: section `.projects` after the articles: heading `projects.title`, intro `projects.intro`, one `.project-card` per entry (`need`, `name`, `blurb`, `cta` link).
- [ ] **Step 3:** Article: `author-box.html` between the article body and the share row: `author.title`, `author.bio`, `author.more`, a list of name + `tagline` links, LinkedIn link.
- [ ] **Step 4:** Footer: row titled `projects.footer_title` with the four names.
- [ ] **Step 5:** About: `about.html` renders `{% tf about.md %}`, then `projects.about_title`, `projects.about_intro`, a list of name, `role`, `blurb`, link, then the connect paragraph. Front matter `title_key: nav.about`.
- [ ] **Step 6:** Styles in the existing palette; cards reuse the article-card look; grid `repeat(auto-fit, minmax(240px, 1fr))`.
- [ ] **Step 7: Commit** `feat: promote the author's projects across the site`.

### Task 5: Metadata, icons, crawl files

**Files:**
- Create: `assets/img/favicon.svg`, `assets/img/apple-touch-icon.png`, `assets/img/og-image.png`, `favicon.ico`, `robots.txt`, `sitemap.xml`, `feed.xml`, `404.html`
- Modify: `_includes/head.html`, `articles.html`, `index.html`, `_config.yml`

**Interfaces:**
- Consumes: `title_key` front matter (Task 4), `translated` flag (Task 2).

- [ ] **Step 1:** Title: `<page title> | AI School`; home uses `global.home_title`. A page's title is `title_key` translated when present, else `title`.
- [ ] **Step 2:** Description: `excerpt_text`, else first paragraph, else site description; stripped and escaped onto one line.
- [ ] **Step 3:** Canonical `{{ site.url }}{{ site.baseurl }}{{ page.url }}` (English URL when `translated == false`). hreflang `en` and `x-default` → English URL; `ro` → Romanian URL, omitted when `translated == false`.
- [ ] **Step 4:** Open Graph and Twitter: `og:type` (`article` for posts), title, description, url, site_name, locale, image `{{ site.url }}/assets/img/og-image.png` with width 1200 and height 630, `twitter:card=summary_large_image`.
- [ ] **Step 5:** Icons: SVG favicon (gold spark on the teal accent), 180px touch icon, `favicon.ico`. Share image 1200×630 in the site's fonts and colours.
- [ ] **Step 6:** `robots.txt` (allow all, both sitemaps), per-language `sitemap.xml` and Atom `feed.xml` that skip untranslated posts, `404.html` with `permalink: /404.html`.
- [ ] **Step 7: Commit** `feat: share previews, icons, sitemap, feed and 404 page`.

### Task 6: Content and visual polish

**Files:**
- Modify: `_i18n/en/_posts/2026-03-15-first-contact.md`, `2026-04-01-scope.md`, `_includes/article-card.html`, `_layouts/home.html`, `_sass/_variables.scss`, `_article-card.scss`, `_article.scss`, `_nav.scss`

- [ ] **Step 1:** Replace the seven LinkedIn links to "The Gap" and "The First-Contact Protocol" with `{{ site.baseurl }}/articles/the-gap/` and `{{ site.baseurl }}/articles/first-contact/`. The GDPval LinkedIn link stays.
- [ ] **Step 2:** Cards show `excerpt_text` when present.
- [ ] **Step 3:** Add `$color-primary-text` at 4.5:1 or better on white and on `#FAF8F5`; use it for the series labels. Language separator uses `$color-text-light`.
- [ ] **Step 4:** Card meta items do not wrap mid-item; the row wraps as a whole.
- [ ] **Step 5:** Home heading uses `articles.latest` with an `articles.view_all` link.
- [ ] **Step 6: Commit** `fix: on-site article links, contrast and card layout`.

### Task 7: Verify

- [ ] **Step 1:** `bundle exec jekyll build` exits 0.
- [ ] **Step 2:** `python3 scripts/check_site.py _site` prints `OK` and exits 0.
- [ ] **Step 3:** Screenshots of home, an article and About in both languages at 1280px and 390px, read for layout faults.
- [ ] **Step 4:** After Mihai approves: GitHub Pages settings (certificate, Enforce HTTPS, Actions source), then merge to `main`.
