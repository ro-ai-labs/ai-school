# ai-school.ro Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a bilingual (EN/RO) Jekyll site for ai-school.ro, deployed to GitHub Pages via GitHub Actions, with 3 existing articles published in English.

**Architecture:** Jekyll with jekyll-multiple-languages-plugin for i18n. Custom Sass styling (warm editorial design). GitHub Actions workflow for build+deploy since the i18n plugin is not on the GitHub Pages whitelist. Content lives in `_i18n/en/_posts/` and `_i18n/ro/_posts/`.

**Tech Stack:** Jekyll 4.x, jekyll-multiple-languages-plugin, Sass, GitHub Actions, Google Fonts (Lora + Inter)

---

## File Structure

```
/                              # repo root
├── _config.yml                # Jekyll config: site settings, plugin config, i18n setup
├── Gemfile                    # Ruby dependencies
├── .github/
│   └── workflows/
│       └── deploy.yml         # GitHub Actions: build Jekyll + deploy to Pages
├── _i18n/
│   ├── en.yml                 # English UI strings (nav, footer, buttons, labels)
│   ├── ro.yml                 # Romanian UI strings
│   ├── en/
│   │   └── _posts/
│   │       ├── 2026-03-01-the-gap.md
│   │       ├── 2026-03-15-first-contact.md
│   │       └── 2026-04-01-scope.md
│   └── ro/
│       └── _posts/
│           ├── 2026-03-01-the-gap.md        # placeholder (RO translation)
│           ├── 2026-03-15-first-contact.md  # placeholder (RO translation)
│           └── 2026-04-01-scope.md          # placeholder (RO translation)
├── _layouts/
│   ├── default.html           # Base layout: head, nav, footer, language meta
│   ├── home.html              # Home page layout: hero, featured articles, teaser
│   ├── article.html           # Single article layout: reading time, byline, series nav
│   └── articles.html          # Articles listing layout: card grid
├── _includes/
│   ├── head.html              # <head> tag: meta, fonts, CSS, hreflang
│   ├── nav.html               # Top navigation + language switcher
│   ├── footer.html            # Footer: links, social, copyright
│   ├── article-card.html      # Reusable article card for listings
│   └── language-switcher.html # RO/EN toggle component
├── _sass/
│   ├── _variables.scss        # Color palette, fonts, spacing, breakpoints
│   ├── _base.scss             # Reset, typography, global styles
│   ├── _nav.scss              # Navigation + mobile hamburger
│   ├── _hero.scss             # Home page hero section
│   ├── _article.scss          # Article reading layout + typography
│   ├── _article-card.scss     # Card component for listings
│   └── _footer.scss           # Footer styles
├── assets/
│   └── css/
│       └── main.scss          # Sass entry point (imports all partials)
├── index.html                 # Home page (uses home layout)
├── articles.html              # Articles listing page
└── about.html                 # About page
```

---

### Task 1: Jekyll Project Scaffold

**Files:**
- Create: `Gemfile`
- Create: `_config.yml`
- Create: `assets/css/main.scss`
- Create: `_sass/_variables.scss`
- Create: `index.html`

- [ ] **Step 1: Create Gemfile**

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"

group :jekyll_plugins do
  gem "jekyll-multiple-languages-plugin"
end
```

- [ ] **Step 2: Create _config.yml**

```yaml
title: AI School
description: "Free AI Literacy for Everybody"
url: "https://ai-school.ro"
baseurl: ""

# Languages
languages: ["en", "ro"]
default_lang: "en"
exclude_from_localizations: ["assets", "CNAME"]

# Permalinks
permalink: /articles/:slug/

# Build
markdown: kramdown
sass:
  sass_dir: _sass
  style: compressed

# Exclude from build
exclude:
  - Gemfile
  - Gemfile.lock
  - README.md
  - docs/
  - framework/
  - "AI School/"
  - node_modules/
  - vendor/
```

- [ ] **Step 3: Create Sass variables**

Create `_sass/_variables.scss`:

```scss
// Colors
$color-primary: #D4A843;        // warm amber/gold
$color-bg: #FAF8F5;             // warm off-white
$color-text: #2D2926;           // dark warm gray
$color-accent: #1A6B5A;         // deep teal
$color-accent-secondary: #E07A5F; // soft coral
$color-border: #E8E4DF;         // subtle warm border
$color-text-light: #6B6560;     // lighter text for meta info
$color-bg-card: #FFFFFF;        // card background
$color-nav-bg: #FFFFFF;         // nav background

// Typography
$font-heading: 'Lora', Georgia, 'Times New Roman', serif;
$font-body: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
$font-mono: 'JetBrains Mono', 'Fira Code', monospace;

// Sizing
$content-width: 720px;          // reading width (~65-75 chars)
$site-width: 1200px;            // max site width
$nav-height: 64px;

// Spacing
$space-xs: 0.25rem;
$space-sm: 0.5rem;
$space-md: 1rem;
$space-lg: 2rem;
$space-xl: 3rem;
$space-2xl: 5rem;

// Breakpoints
$bp-mobile: 600px;
$bp-tablet: 900px;
$bp-desktop: 1200px;
```

- [ ] **Step 4: Create Sass entry point**

Create `assets/css/main.scss`:

```scss
---
---

@import "variables";
@import "base";
@import "nav";
@import "hero";
@import "article";
@import "article-card";
@import "footer";
```

- [ ] **Step 5: Create minimal index.html to verify build**

```html
---
layout: default
---

<h1>AI School</h1>
<p>Coming soon.</p>
```

- [ ] **Step 6: Verify Jekyll builds locally**

Run:
```bash
cd "/mnt/c/Users/xbox1/OneDrive/AI Labs/ai-school"
bundle install
bundle exec jekyll build
```
Expected: Build succeeds, `_site/` directory created with `index.html`.

- [ ] **Step 7: Commit**

```bash
git add Gemfile _config.yml _sass/_variables.scss assets/css/main.scss index.html
git commit -m "feat: scaffold Jekyll project with i18n plugin and Sass variables"
```

---

### Task 2: GitHub Actions Deploy Workflow

**Files:**
- Create: `.github/workflows/deploy.yml`

- [ ] **Step 1: Create deploy workflow**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Jekyll to GitHub Pages

on:
  push:
    branches: ["main"]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          submodules: false

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.3'
          bundler-cache: true

      - name: Build with Jekyll
        run: bundle exec jekyll build
        env:
          JEKYLL_ENV: production

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/deploy.yml
git commit -m "ci: add GitHub Actions workflow for Jekyll Pages deploy"
```

---

### Task 3: i18n Language Files

**Files:**
- Create: `_i18n/en.yml`
- Create: `_i18n/ro.yml`

- [ ] **Step 1: Create English UI strings**

Create `_i18n/en.yml`:

```yaml
global:
  site_title: "AI School"
  site_description: "Free AI Literacy for Everybody"
  language_name: "English"
  language_code: "en"
  switch_language: "Ro"

nav:
  home: "Home"
  articles: "Articles"
  about: "About"

hero:
  title: "Free AI Literacy for Everybody"
  subtitle: "Learn to work with AI effectively, responsibly, and on your own terms. No paywalls. No upsells. Just practical knowledge."
  cta: "Read the Articles"

articles:
  title: "Articles"
  read_more: "Read article"
  minutes_read: "min read"
  published: "Published"
  series_label: "Part of the GenAI School series"
  all_articles: "All Articles"
  related: "Related Articles"
  previous: "Previous in series"
  next: "Next in series"
  share: "Share this article"

about:
  title: "About"

footer:
  tagline: "Free AI literacy, powered by the SPARKS-SIX framework."
  follow: "Follow on LinkedIn"
  copyright: "AI School. All content is free to use and share."
  built_with: "Built with care in Bucharest."
```

- [ ] **Step 2: Create Romanian UI strings**

Create `_i18n/ro.yml`:

```yaml
global:
  site_title: "AI School"
  site_description: "AI Literacy gratuit pentru toata lumea"
  language_name: "Romana"
  language_code: "ro"
  switch_language: "En"

nav:
  home: "Acasa"
  articles: "Articole"
  about: "Despre"

hero:
  title: "AI Literacy gratuit pentru toata lumea"
  subtitle: "Invata sa lucrezi cu AI eficient, responsabil si in termenii tai. Fara paywall. Fara upsell. Doar knowledge practic."
  cta: "Citeste Articolele"

articles:
  title: "Articole"
  read_more: "Citeste articolul"
  minutes_read: "min lectura"
  published: "Publicat"
  series_label: "Parte din seria GenAI School"
  all_articles: "Toate Articolele"
  related: "Articole Similare"
  previous: "Anteriorul din serie"
  next: "Urmatorul din serie"
  share: "Share this article"

about:
  title: "Despre"

footer:
  tagline: "AI literacy gratuit, powered by framework-ul SPARKS-SIX."
  follow: "Follow pe LinkedIn"
  copyright: "AI School. Tot content-ul este free to use and share."
  built_with: "Built with care in Bucharest."
```

- [ ] **Step 3: Commit**

```bash
git add _i18n/en.yml _i18n/ro.yml
git commit -m "feat: add bilingual UI strings (EN/RO)"
```

---

### Task 4: Base Layout + Includes (HTML Structure)

**Files:**
- Create: `_includes/head.html`
- Create: `_includes/nav.html`
- Create: `_includes/footer.html`
- Create: `_includes/language-switcher.html`
- Create: `_layouts/default.html`

- [ ] **Step 1: Create head include**

Create `_includes/head.html`:

```html
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% if page.title %}{{ page.title }} | {% endif %}{% t global.site_title %}</title>
<meta name="description" content="{% if page.excerpt %}{{ page.excerpt | strip_html | truncatewords: 30 }}{% else %}{% t global.site_description %}{% endif %}">

<!-- Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Lora:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">

<!-- CSS -->
<link rel="stylesheet" href="{{ '/assets/css/main.css' | relative_url }}">

<!-- hreflang for SEO -->
{% for lang in site.languages %}
<link rel="alternate" hreflang="{{ lang }}" href="{{ site.url }}/{{ lang }}{{ page.url }}" />
{% endfor %}
<link rel="alternate" hreflang="x-default" href="{{ site.url }}/en{{ page.url }}" />
```

- [ ] **Step 2: Create language switcher include**

Create `_includes/language-switcher.html`:

```html
<div class="language-switcher">
  {% if site.lang == "en" %}
    <a href="{{ site.url }}/ro{{ page.url }}" class="lang-toggle" aria-label="Switch to Romanian">
      <span class="lang-current">En</span>
      <span class="lang-separator">/</span>
      <span class="lang-other">Ro</span>
    </a>
  {% else %}
    <a href="{{ site.url }}/en{{ page.url }}" class="lang-toggle" aria-label="Switch to English">
      <span class="lang-current">Ro</span>
      <span class="lang-separator">/</span>
      <span class="lang-other">En</span>
    </a>
  {% endif %}
</div>
```

- [ ] **Step 3: Create nav include**

Create `_includes/nav.html`:

```html
<nav class="site-nav" role="navigation" aria-label="Main navigation">
  <div class="nav-inner">
    <a href="{{ '/' | relative_url }}" class="nav-logo">
      <span class="nav-logo-text">AI School</span>
    </a>

    <button class="nav-toggle" aria-label="Toggle menu" aria-expanded="false">
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
      <span class="nav-toggle-bar"></span>
    </button>

    <div class="nav-links">
      <a href="{{ '/' | relative_url }}" class="nav-link">{% t nav.home %}</a>
      <a href="{{ '/articles/' | relative_url }}" class="nav-link">{% t nav.articles %}</a>
      <a href="{{ '/about/' | relative_url }}" class="nav-link">{% t nav.about %}</a>
      {% include language-switcher.html %}
    </div>
  </div>
</nav>
```

- [ ] **Step 4: Create footer include**

Create `_includes/footer.html`:

```html
<footer class="site-footer" role="contentinfo">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-logo">AI School</span>
      <p class="footer-tagline">{% t footer.tagline %}</p>
    </div>

    <div class="footer-links">
      <a href="{{ '/' | relative_url }}">{% t nav.home %}</a>
      <a href="{{ '/articles/' | relative_url }}">{% t nav.articles %}</a>
      <a href="{{ '/about/' | relative_url }}">{% t nav.about %}</a>
    </div>

    <div class="footer-social">
      <a href="https://www.linkedin.com/in/mihaicvasnievschi/" target="_blank" rel="noopener" aria-label="LinkedIn">
        {% t footer.follow %}
      </a>
    </div>

    <div class="footer-bottom">
      <p>&copy; {{ site.time | date: '%Y' }} {% t footer.copyright %}</p>
      <p class="footer-built">{% t footer.built_with %}</p>
    </div>
  </div>
</footer>
```

- [ ] **Step 5: Create default layout**

Create `_layouts/default.html`:

```html
<!DOCTYPE html>
<html lang="{{ site.lang }}">
<head>
  {% include head.html %}
</head>
<body>
  {% include nav.html %}

  <main class="site-main">
    {{ content }}
  </main>

  {% include footer.html %}

  <script>
    // Mobile nav toggle
    document.querySelector('.nav-toggle').addEventListener('click', function() {
      const expanded = this.getAttribute('aria-expanded') === 'true';
      this.setAttribute('aria-expanded', !expanded);
      document.querySelector('.nav-links').classList.toggle('nav-links--open');
    });
  </script>
</body>
</html>
```

- [ ] **Step 6: Verify build**

```bash
bundle exec jekyll build
```
Expected: Build succeeds with layouts and includes resolved.

- [ ] **Step 7: Commit**

```bash
git add _includes/ _layouts/default.html
git commit -m "feat: add base layout with nav, footer, language switcher, and head includes"
```

---

### Task 5: Sass Styling (Warm Editorial Design)

**Files:**
- Create: `_sass/_base.scss`
- Create: `_sass/_nav.scss`
- Create: `_sass/_hero.scss`
- Create: `_sass/_article.scss`
- Create: `_sass/_article-card.scss`
- Create: `_sass/_footer.scss`

- [ ] **Step 1: Create base styles**

Create `_sass/_base.scss`:

```scss
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html {
  font-size: 18px;
  scroll-behavior: smooth;

  @media (max-width: $bp-mobile) {
    font-size: 16px;
  }
}

body {
  font-family: $font-body;
  color: $color-text;
  background-color: $color-bg;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

h1, h2, h3, h4, h5, h6 {
  font-family: $font-heading;
  font-weight: 700;
  line-height: 1.3;
  color: $color-text;
}

h1 { font-size: 2.4rem; margin-bottom: $space-lg; }
h2 { font-size: 1.8rem; margin-top: $space-xl; margin-bottom: $space-md; }
h3 { font-size: 1.4rem; margin-top: $space-lg; margin-bottom: $space-sm; }

a {
  color: $color-accent;
  text-decoration: none;
  transition: color 0.2s ease;

  &:hover {
    color: darken($color-accent, 10%);
    text-decoration: underline;
  }
}

p {
  margin-bottom: $space-md;
}

blockquote {
  border-left: 3px solid $color-primary;
  padding: $space-md $space-lg;
  margin: $space-lg 0;
  font-family: $font-heading;
  font-style: italic;
  font-size: 1.1rem;
  color: $color-text-light;
  background: rgba($color-primary, 0.06);
  border-radius: 0 4px 4px 0;
}

img {
  max-width: 100%;
  height: auto;
}

hr {
  border: none;
  border-top: 1px solid $color-border;
  margin: $space-xl 0;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: $space-lg 0;
  font-size: 0.9rem;

  th, td {
    padding: $space-sm $space-md;
    border: 1px solid $color-border;
    text-align: left;
  }

  th {
    background: rgba($color-primary, 0.08);
    font-weight: 600;
  }
}

.container {
  max-width: $site-width;
  margin: 0 auto;
  padding: 0 $space-lg;
}

.content-width {
  max-width: $content-width;
  margin: 0 auto;
}
```

- [ ] **Step 2: Create nav styles**

Create `_sass/_nav.scss`:

```scss
.site-nav {
  position: sticky;
  top: 0;
  z-index: 100;
  background: $color-nav-bg;
  border-bottom: 1px solid $color-border;
  height: $nav-height;
}

.nav-inner {
  max-width: $site-width;
  margin: 0 auto;
  padding: 0 $space-lg;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.nav-logo {
  text-decoration: none;

  &:hover { text-decoration: none; }
}

.nav-logo-text {
  font-family: $font-heading;
  font-size: 1.3rem;
  font-weight: 700;
  color: $color-text;
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: $space-lg;
}

.nav-link {
  font-size: 0.9rem;
  font-weight: 500;
  color: $color-text-light;
  text-decoration: none;
  transition: color 0.2s ease;

  &:hover {
    color: $color-text;
    text-decoration: none;
  }
}

// Language switcher
.language-switcher {
  margin-left: $space-md;
}

.lang-toggle {
  display: inline-flex;
  align-items: center;
  padding: $space-xs $space-sm;
  border: 1px solid $color-border;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
  color: $color-text;
  text-decoration: none;

  &:hover {
    border-color: $color-primary;
    text-decoration: none;
  }
}

.lang-current {
  font-weight: 600;
}

.lang-separator {
  margin: 0 2px;
  color: $color-border;
}

.lang-other {
  color: $color-text-light;
}

// Mobile hamburger
.nav-toggle {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: $space-sm;
}

.nav-toggle-bar {
  display: block;
  width: 22px;
  height: 2px;
  background: $color-text;
  transition: transform 0.2s ease;
}

@media (max-width: $bp-mobile) {
  .nav-toggle {
    display: flex;
  }

  .nav-links {
    display: none;
    position: absolute;
    top: $nav-height;
    left: 0;
    right: 0;
    background: $color-nav-bg;
    flex-direction: column;
    padding: $space-lg;
    border-bottom: 1px solid $color-border;
    gap: $space-md;
  }

  .nav-links--open {
    display: flex;
  }

  .language-switcher {
    margin-left: 0;
  }
}
```

- [ ] **Step 3: Create hero styles**

Create `_sass/_hero.scss`:

```scss
.hero {
  padding: $space-2xl 0;
  text-align: center;

  @media (max-width: $bp-mobile) {
    padding: $space-xl 0;
  }
}

.hero-inner {
  max-width: 680px;
  margin: 0 auto;
  padding: 0 $space-lg;
}

.hero-badge {
  display: inline-block;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: $color-accent;
  margin-bottom: $space-md;
}

.hero-title {
  font-family: $font-heading;
  font-size: 2.8rem;
  font-weight: 700;
  line-height: 1.2;
  color: $color-text;
  margin-bottom: $space-lg;

  @media (max-width: $bp-mobile) {
    font-size: 2rem;
  }
}

.hero-subtitle {
  font-size: 1.15rem;
  line-height: 1.7;
  color: $color-text-light;
  margin-bottom: $space-xl;
}

.hero-cta {
  display: inline-block;
  padding: $space-sm $space-lg;
  background: $color-accent;
  color: #fff;
  font-weight: 600;
  font-size: 1rem;
  border-radius: 6px;
  text-decoration: none;
  transition: background 0.2s ease, transform 0.15s ease;

  &:hover {
    background: darken($color-accent, 8%);
    color: #fff;
    text-decoration: none;
    transform: translateY(-1px);
  }
}
```

- [ ] **Step 4: Create article reading styles**

Create `_sass/_article.scss`:

```scss
.article-header {
  text-align: center;
  padding: $space-xl 0 $space-lg;
  max-width: $content-width;
  margin: 0 auto;
}

.article-meta {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $space-md;
  font-size: 0.85rem;
  color: $color-text-light;
  margin-bottom: $space-md;
}

.article-meta-separator {
  color: $color-border;
}

.article-series-badge {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: $color-primary;
  margin-bottom: $space-sm;
}

.article-title {
  font-size: 2.4rem;
  line-height: 1.2;
  margin-bottom: $space-md;

  @media (max-width: $bp-mobile) {
    font-size: 1.8rem;
  }
}

.article-excerpt {
  font-size: 1.15rem;
  color: $color-text-light;
  font-family: $font-heading;
  font-style: italic;
}

// Article body
.article-body {
  max-width: $content-width;
  margin: 0 auto;
  padding: 0 $space-lg $space-2xl;

  h2 {
    margin-top: $space-2xl;
  }

  // Pull quotes
  blockquote {
    margin: $space-xl (-$space-md);

    @media (max-width: $bp-mobile) {
      margin: $space-lg 0;
    }
  }

  // Links in body
  a {
    text-decoration: underline;
    text-underline-offset: 2px;

    &:hover {
      color: $color-accent;
    }
  }
}

// Article footer (share, series nav)
.article-footer {
  max-width: $content-width;
  margin: 0 auto;
  padding: 0 $space-lg $space-2xl;
}

.article-share {
  display: flex;
  align-items: center;
  gap: $space-md;
  padding: $space-lg 0;
  border-top: 1px solid $color-border;
  font-size: 0.9rem;
  color: $color-text-light;
}

.article-share-link {
  display: inline-flex;
  align-items: center;
  padding: $space-xs $space-sm;
  border: 1px solid $color-border;
  border-radius: 4px;
  font-size: 0.85rem;
  color: $color-text;

  &:hover {
    border-color: $color-accent;
    text-decoration: none;
  }
}

// Series navigation
.series-nav {
  display: flex;
  justify-content: space-between;
  gap: $space-lg;
  padding: $space-lg 0;
  border-top: 1px solid $color-border;
  margin-top: $space-lg;
}

.series-nav-item {
  flex: 1;

  &--next {
    text-align: right;
  }
}

.series-nav-label {
  font-size: 0.8rem;
  color: $color-text-light;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: $space-xs;
}

.series-nav-title {
  font-family: $font-heading;
  font-weight: 600;
  font-size: 1rem;
}
```

- [ ] **Step 5: Create article card styles**

Create `_sass/_article-card.scss`:

```scss
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: $space-lg;
  padding: $space-lg 0;

  @media (max-width: $bp-mobile) {
    grid-template-columns: 1fr;
  }
}

.article-card {
  background: $color-bg-card;
  border: 1px solid $color-border;
  border-radius: 8px;
  padding: $space-lg;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;

  &:hover {
    border-color: $color-primary;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  }
}

.article-card-series {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: $color-primary;
  margin-bottom: $space-sm;
}

.article-card-title {
  font-family: $font-heading;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: $space-sm;

  a {
    color: $color-text;
    text-decoration: none;

    &:hover {
      color: $color-accent;
      text-decoration: none;
    }
  }
}

.article-card-excerpt {
  font-size: 0.9rem;
  color: $color-text-light;
  line-height: 1.6;
  margin-bottom: $space-md;
  flex-grow: 1;
}

.article-card-meta {
  display: flex;
  align-items: center;
  gap: $space-sm;
  font-size: 0.8rem;
  color: $color-text-light;
}

.article-card-read {
  margin-left: auto;
  font-weight: 600;
  color: $color-accent;
  font-size: 0.85rem;
}
```

- [ ] **Step 6: Create footer styles**

Create `_sass/_footer.scss`:

```scss
.site-footer {
  background: $color-text;
  color: rgba(255, 255, 255, 0.7);
  padding: $space-2xl 0 $space-lg;
  margin-top: $space-2xl;
}

.footer-inner {
  max-width: $site-width;
  margin: 0 auto;
  padding: 0 $space-lg;
}

.footer-brand {
  margin-bottom: $space-xl;
}

.footer-logo {
  font-family: $font-heading;
  font-size: 1.4rem;
  font-weight: 700;
  color: #fff;
  display: block;
  margin-bottom: $space-sm;
}

.footer-tagline {
  font-size: 0.9rem;
  max-width: 400px;
}

.footer-links {
  display: flex;
  gap: $space-lg;
  margin-bottom: $space-lg;

  a {
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;

    &:hover {
      color: #fff;
      text-decoration: none;
    }
  }
}

.footer-social {
  margin-bottom: $space-xl;

  a {
    display: inline-flex;
    align-items: center;
    padding: $space-xs $space-md;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 4px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.85rem;

    &:hover {
      border-color: $color-primary;
      color: #fff;
      text-decoration: none;
    }
  }
}

.footer-bottom {
  padding-top: $space-lg;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.8rem;

  p {
    margin-bottom: $space-xs;
  }
}

.footer-built {
  font-style: italic;
}
```

- [ ] **Step 7: Verify build**

```bash
bundle exec jekyll build
```
Expected: Build succeeds, CSS compiled at `_site/assets/css/main.css`.

- [ ] **Step 8: Commit**

```bash
git add _sass/
git commit -m "feat: add warm editorial Sass styles (base, nav, hero, article, cards, footer)"
```

---

### Task 6: Page Layouts (Home, Articles, Article)

**Files:**
- Create: `_layouts/home.html`
- Create: `_layouts/articles.html`
- Create: `_layouts/article.html`
- Create: `_includes/article-card.html`

- [ ] **Step 1: Create article card include**

Create `_includes/article-card.html`:

```html
<article class="article-card">
  {% if include.post.series %}
  <span class="article-card-series">{{ include.post.series }}</span>
  {% endif %}
  <h3 class="article-card-title">
    <a href="{{ include.post.url }}">{{ include.post.title }}</a>
  </h3>
  <p class="article-card-excerpt">{{ include.post.excerpt | strip_html | truncatewords: 30 }}</p>
  <div class="article-card-meta">
    <time>{{ include.post.date | date: "%B %-d, %Y" }}</time>
    {% if include.post.reading_time %}
    <span>{{ include.post.reading_time }} {% t articles.minutes_read %}</span>
    {% endif %}
    <span class="article-card-read">{% t articles.read_more %} &rarr;</span>
  </div>
</article>
```

- [ ] **Step 2: Create home layout**

Create `_layouts/home.html`:

```html
---
layout: default
---

<section class="hero">
  <div class="hero-inner">
    <span class="hero-badge">GenAI School</span>
    <h1 class="hero-title">{% t hero.title %}</h1>
    <p class="hero-subtitle">{% t hero.subtitle %}</p>
    <a href="{{ '/articles/' | relative_url }}" class="hero-cta">{% t hero.cta %}</a>
  </div>
</section>

<section class="container">
  <h2>{% t articles.all_articles %}</h2>
  <div class="articles-grid">
    {% assign posts = site.posts | sort: "date" | reverse %}
    {% for post in posts limit:3 %}
      {% include article-card.html post=post %}
    {% endfor %}
  </div>
</section>

{{ content }}
```

- [ ] **Step 3: Create articles listing layout**

Create `_layouts/articles.html`:

```html
---
layout: default
---

<div class="container">
  <div class="content-width" style="padding-top: 3rem;">
    <h1>{% t articles.title %}</h1>
  </div>

  <div class="articles-grid">
    {% assign posts = site.posts | sort: "date" | reverse %}
    {% for post in posts %}
      {% include article-card.html post=post %}
    {% endfor %}
  </div>
</div>
```

- [ ] **Step 4: Create article layout**

Create `_layouts/article.html`:

```html
---
layout: default
---

<article>
  <header class="article-header">
    {% if page.series %}
    <span class="article-series-badge">{% t articles.series_label %}</span>
    {% endif %}
    <h1 class="article-title">{{ page.title }}</h1>
    <div class="article-meta">
      <span>{{ page.author }}</span>
      <span class="article-meta-separator">&middot;</span>
      <time>{{ page.date | date: "%B %-d, %Y" }}</time>
      {% if page.reading_time %}
      <span class="article-meta-separator">&middot;</span>
      <span>{{ page.reading_time }} {% t articles.minutes_read %}</span>
      {% endif %}
    </div>
    {% if page.excerpt_text %}
    <p class="article-excerpt">{{ page.excerpt_text }}</p>
    {% endif %}
  </header>

  <div class="article-body">
    {{ content }}
  </div>

  <footer class="article-footer">
    <div class="article-share">
      <span>{% t articles.share %}</span>
      <a href="https://www.linkedin.com/sharing/share-offsite/?url={{ site.url }}{{ page.url }}" target="_blank" rel="noopener" class="article-share-link">LinkedIn</a>
    </div>

    {% assign sorted_posts = site.posts | sort: "series_order" %}
    {% if page.series and page.series_order %}
    <nav class="series-nav">
      <div class="series-nav-item">
        {% for post in sorted_posts %}
          {% if post.series == page.series and post.series_order == page.series_order | minus: 1 %}
            <div class="series-nav-label">{% t articles.previous %}</div>
            <a href="{{ post.url }}" class="series-nav-title">{{ post.title }}</a>
          {% endif %}
        {% endfor %}
      </div>
      <div class="series-nav-item series-nav-item--next">
        {% for post in sorted_posts %}
          {% if post.series == page.series and post.series_order == page.series_order | plus: 1 %}
            <div class="series-nav-label">{% t articles.next %}</div>
            <a href="{{ post.url }}" class="series-nav-title">{{ post.title }}</a>
          {% endif %}
        {% endfor %}
      </div>
    </nav>
    {% endif %}
  </footer>
</article>
```

- [ ] **Step 5: Commit**

```bash
git add _layouts/home.html _layouts/articles.html _layouts/article.html _includes/article-card.html
git commit -m "feat: add home, articles listing, and article detail layouts"
```

---

### Task 7: Page Files (Home, Articles, About)

**Files:**
- Modify: `index.html`
- Create: `articles.html`
- Create: `about.html`

- [ ] **Step 1: Update index.html to use home layout**

Replace the contents of `index.html`:

```html
---
layout: home
---
```

- [ ] **Step 2: Create articles listing page**

Create `articles.html`:

```html
---
layout: articles
---
```

- [ ] **Step 3: Create about page**

Create `about.html`:

```html
---
layout: default
title: About
---

<div class="content-width" style="padding: 3rem 1rem 5rem;">
  <h1>{% t about.title %}</h1>

  <p>AI School is a free AI literacy initiative created by <strong>Mihai Cvasnievschi</strong>, an AI/ML Architect with 25+ years of software development experience and over 10 years building production AI systems.</p>

  <h2>The Mission</h2>

  <p>30% of European workers use AI daily. Only 15% have received any training. The EU AI Act now mandates AI literacy for organisations deploying AI systems, with enforcement beginning in 2026.</p>

  <p>AI School exists to close that gap. Everything here is free: the articles, the framework, the methodology. No paywalls, no paid tiers, no upsells. The value speaks for itself.</p>

  <h2>SPARKS-SIX</h2>

  <p>Our articles are grounded in the SPARKS-SIX framework: a six-pillar methodology for working effectively and responsibly with any AI tool. The framework is being released publicly through our article series.</p>

  <h2>Connect</h2>

  <p>Follow the journey on <a href="https://www.linkedin.com/in/mihaicvasnievschi/" target="_blank" rel="noopener">LinkedIn</a>, where the original article series is published.</p>
</div>
```

- [ ] **Step 4: Commit**

```bash
git add index.html articles.html about.html
git commit -m "feat: add home, articles, and about pages"
```

---

### Task 8: Content Migration (English Articles)

**Files:**
- Create: `_i18n/en/_posts/2026-03-01-the-gap.md`
- Create: `_i18n/en/_posts/2026-03-15-first-contact.md`
- Create: `_i18n/en/_posts/2026-04-01-scope.md`

For each article, extract the body text (after "## Article Text" and before "## Verified Sources"), strip the LinkedIn metadata section, and add Jekyll front matter.

- [ ] **Step 1: Migrate Article 1 (The Gap)**

Create `_i18n/en/_posts/2026-03-01-the-gap.md`:

Front matter:
```yaml
---
layout: article
title: "The Gap"
date: 2026-03-01
author: Mihai Cvasnievschi
reading_time: 12
categories: [ai-literacy]
series: GenAI School
series_order: 1
excerpt_text: "Three years ago, ChatGPT launched and changed how we work. Today, 30% of European workers use AI daily. Only 15% have received any training."
---
```

Body: Copy everything from `## Article Text` line (exclusive) through the line before `## Verified Sources` from `framework/articles/article-1-the-problem.md`. Strip the horizontal rules (`---`) that act as LinkedIn section separators, converting them to empty lines instead. Keep all markdown links intact.

- [ ] **Step 2: Migrate Article 2 (First-Contact)**

Create `_i18n/en/_posts/2026-03-15-first-contact.md`:

Front matter:
```yaml
---
layout: article
title: "The First-Contact Protocol"
date: 2026-03-15
author: Mihai Cvasnievschi
reading_time: 10
categories: [ai-literacy]
series: GenAI School
series_order: 2
excerpt_text: "For a year, Maria used ChatGPT to rewrite emails. Then one Tuesday, she stopped asking it to do things for her. She asked it to help her think."
---
```

Body: Same extraction process as Article 1 from `framework/articles/article-2-foundations-first-contact.md`.

- [ ] **Step 3: Migrate Article 3 (SCOPE)**

Create `_i18n/en/_posts/2026-04-01-scope.md`:

Front matter:
```yaml
---
layout: article
title: "The Most Important AI Skill Nobody Teaches: Knowing When to Say No"
date: 2026-04-01
author: Mihai Cvasnievschi
reading_time: 14
categories: [ai-literacy]
series: GenAI School
series_order: 3
excerpt_text: "Thursday morning, 8:47 AM. Maria's coffee was already cold. She was about to learn the most important AI skill nobody teaches."
---
```

Body: Same extraction process from `framework/articles/article-3-scope.md`.

- [ ] **Step 4: Verify build with posts**

```bash
bundle exec jekyll build
ls _site/en/articles/
```
Expected: Three article directories exist under `_site/en/articles/`.

- [ ] **Step 5: Commit**

```bash
git add _i18n/en/_posts/
git commit -m "feat: migrate 3 English articles (The Gap, First-Contact, SCOPE)"
```

---

### Task 9: Romanian Placeholder Articles

**Files:**
- Create: `_i18n/ro/_posts/2026-03-01-the-gap.md`
- Create: `_i18n/ro/_posts/2026-03-15-first-contact.md`
- Create: `_i18n/ro/_posts/2026-04-01-scope.md`

- [ ] **Step 1: Create Romanian placeholder for Article 1**

Create `_i18n/ro/_posts/2026-03-01-the-gap.md`:

```yaml
---
layout: article
title: "Decalajul"
date: 2026-03-01
author: Mihai Cvasnievschi
reading_time: 12
categories: [ai-literacy]
series: GenAI School
series_order: 1
excerpt_text: "Acum trei ani, ChatGPT a fost lansat si a schimbat modul in care lucram. Astazi, 30% din workerii europeni folosesc AI zilnic. Doar 15% au primit orice fel de training."
---

Traducerea acestui articol va fi disponibila in curand. Pana atunci, puteti citi versiunea in engleza.

Translation of this article coming soon. In the meantime, you can read the English version.
```

- [ ] **Step 2: Create Romanian placeholder for Article 2**

Create `_i18n/ro/_posts/2026-03-15-first-contact.md`:

```yaml
---
layout: article
title: "Protocolul de Prim-Contact"
date: 2026-03-15
author: Mihai Cvasnievschi
reading_time: 10
categories: [ai-literacy]
series: GenAI School
series_order: 2
excerpt_text: "Timp de un an, Maria a folosit ChatGPT sa rescrie email-uri. Apoi, intr-o marti, a incetat sa ii ceara sa faca lucruri pentru ea. I-a cerut sa o ajute sa gandeasca."
---

Traducerea acestui articol va fi disponibila in curand. Pana atunci, puteti citi versiunea in engleza.

Translation of this article coming soon. In the meantime, you can read the English version.
```

- [ ] **Step 3: Create Romanian placeholder for Article 3**

Create `_i18n/ro/_posts/2026-04-01-scope.md`:

```yaml
---
layout: article
title: "Cel Mai Important Skill de AI pe care Nimeni nu il Preda: Sa Stii Cand sa Spui Nu"
date: 2026-04-01
author: Mihai Cvasnievschi
reading_time: 14
categories: [ai-literacy]
series: GenAI School
series_order: 3
excerpt_text: "Joi dimineata, 8:47 AM. Cafeaua Mariei era deja rece. Ea era pe punctul de a invata cel mai important skill de AI pe care nimeni nu il preda."
---

Traducerea acestui articol va fi disponibila in curand. Pana atunci, puteti citi versiunea in engleza.

Translation of this article coming soon. In the meantime, you can read the English version.
```

- [ ] **Step 4: Verify build**

```bash
bundle exec jekyll build
ls _site/ro/articles/
```
Expected: Three article directories under `_site/ro/articles/`.

- [ ] **Step 5: Commit**

```bash
git add _i18n/ro/_posts/
git commit -m "feat: add Romanian placeholder articles for translation"
```

---

### Task 10: Root Redirect + CNAME + Final Verification

**Files:**
- Create: `CNAME`
- Modify: `_config.yml` (if needed)

- [ ] **Step 1: Create CNAME file**

Create `CNAME`:

```
ai-school.ro
```

- [ ] **Step 2: Verify the root redirect works**

The jekyll-multiple-languages-plugin automatically generates `/en/` and `/ro/` prefixed URLs when `default_lang` is `"en"`. The root `/` should serve the English version by default. Verify:

```bash
bundle exec jekyll build
cat _site/index.html | head -20
```
Expected: The home page content renders at root.

- [ ] **Step 3: Full local preview**

```bash
bundle exec jekyll serve
```
Expected: Site runs at `http://localhost:4000`. Verify:
- Home page loads with hero, article cards
- `/articles/` shows all 3 articles
- `/about/` shows about page
- Language switcher toggles between `/en/` and `/ro/` URLs
- Individual articles render with proper typography
- Mobile nav hamburger works
- Footer renders correctly

- [ ] **Step 4: Commit and push**

```bash
git add CNAME
git commit -m "feat: add CNAME for ai-school.ro custom domain"
git push origin main
```

- [ ] **Step 5: Configure GitHub Pages**

In the GitHub repo settings (Settings > Pages):
- Source: GitHub Actions
- Custom domain: ai-school.ro
- Enforce HTTPS: enabled

After DNS is configured (A records pointing to GitHub Pages IPs + CNAME for www), the site will be live at https://ai-school.ro.

---

## Summary

| Task | What it builds | Depends on |
|------|---------------|------------|
| 1 | Jekyll scaffold (Gemfile, config, Sass vars) | Nothing |
| 2 | GitHub Actions deploy workflow | Nothing |
| 3 | i18n language files (EN/RO UI strings) | Nothing |
| 4 | Base layout + includes (HTML structure) | Task 1, 3 |
| 5 | Sass styling (full editorial design) | Task 1 |
| 6 | Page layouts (home, articles, article) | Task 4, 5 |
| 7 | Page files (index, articles, about) | Task 6 |
| 8 | English article content migration | Task 6 |
| 9 | Romanian placeholder articles | Task 6 |
| 10 | CNAME + final verification | All above |

**Parallel opportunities:** Tasks 1, 2, 3 can run in parallel. Tasks 5 and 3 can run in parallel. Tasks 8 and 9 can run in parallel.
