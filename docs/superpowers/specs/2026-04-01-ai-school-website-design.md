# ai-school.ro Website Design Spec

## Overview

A free AI literacy portal hosted on GitHub Pages using Jekyll. Bilingual (English + Romanian), warm editorial design, content-first. Publishes the existing LinkedIn article series as blog posts. Future migration path to WordPress.

## Tech Stack

- **Static site generator:** Jekyll
- **i18n:** jekyll-multiple-languages-plugin
- **Hosting:** GitHub Pages (via GitHub Actions for custom plugin support)
- **Styling:** Custom Sass, no CSS framework (keeps it light and editorial)
- **Fonts:** Serif for headings (editorial feel), clean sans-serif for body

## URL Structure

- `/en/` — English home (default, root `/` redirects here)
- `/ro/` — Romanian home
- `/en/articles/<slug>/` — English article
- `/ro/articles/<slug>/` — Romanian article

## Pages

### Home
- Hero section: mission statement ("Free AI Literacy for Everybody"), warm illustration or abstract visual
- Featured/latest articles grid (3 most recent)
- Brief SPARKS-SIX teaser ("A framework is coming" energy, not full details)
- CTA: Follow/subscribe for updates

### Articles Index
- Blog listing, newest first
- Category/tag filtering
- Each card: title, excerpt, reading time, date, language indicator

### Article Page
- Warm editorial layout optimized for long-form reading
- Language switcher (linking to the same article in the other language)
- Reading time estimate
- Author byline (Mihai Cvasnievschi)
- Related articles at bottom
- Social sharing (LinkedIn primarily)
- Navigation to previous/next article in series

### About
- Brief bio of Mihai Cvasnievschi (AI/ML Architect, 25+ years dev, 10+ years AI)
- The mission: free AI literacy, EU AI Act context
- Link to LinkedIn profile and article series
- GenAI School mention

## Navigation

- **Top nav:** Home | Articles | About | [RO/EN toggle]
- **Footer:** Links, LinkedIn, "Powered by SPARKS-SIX" mention, copyright
- Mobile: hamburger menu with language toggle prominent

## Design Direction

### Warm & Editorial
- Magazine/publication feel, not a docs site or corporate page
- Matches the David Attenborough narrative voice of the articles
- Generous whitespace, readable line lengths (~65-75 characters)
- Warm color palette (not cold corporate blues)
- Subtle textures or accent elements to add warmth
- Typography-driven: strong heading hierarchy, pull quotes for key statements

### Color Palette (starting point)
- Primary: warm amber/gold (#D4A843 range) — knowledge, warmth, illumination
- Background: warm off-white (#FAF8F5) — easy on the eyes for long reading
- Text: dark warm gray (#2D2926) — softer than pure black
- Accent: deep teal (#1A6B5A) — trust, intelligence, complements the warm tones
- Secondary accent: soft coral (#E07A5F) — energy, human warmth

### Typography
- Headings: serif font (e.g., Merriweather, Lora, or similar)
- Body: clean sans-serif (e.g., Inter, Source Sans Pro)
- Code/technical: monospace where needed

## Content Structure

### Collections
- `_posts/` — Blog articles (the LinkedIn series + future articles)
- No framework collection for now

### Article Front Matter
```yaml
---
layout: article
title: "The Gap"
title_ro: "Decalajul"
date: 2026-04-01
author: Mihai Cvasnievschi
reading_time: 12
categories: [ai-literacy, sparks-six]
series: genai-school
series_order: 1
excerpt: "Three years ago, ChatGPT launched..."
excerpt_ro: "Acum trei ani, ChatGPT a fost lansat..."
---
```

### Language File Structure
```
_i18n/
  en.yml      # English UI strings
  ro.yml      # Romanian UI strings
_i18n/en/
  _posts/     # English articles
_i18n/ro/
  _posts/     # Romanian articles (translated)
```

## Bilingual Strategy

- English is the primary/default language
- Each article exists as two separate files (EN and RO)
- UI strings (navigation, footer, "Read more", etc.) in language YAML files
- Language switcher on every page links to the equivalent page in the other language
- SEO: hreflang tags for proper search engine indexing

## GitHub Actions Build

Since jekyll-multiple-languages-plugin is not on the GitHub Pages whitelist, we use a GitHub Actions workflow:
- Trigger on push to main
- Build with Jekyll + plugins
- Deploy to GitHub Pages

## Initial Content

Three articles to publish at launch (English versions exist, Romanian translations needed):
1. "The Gap" (article-1-the-problem.md)
2. "The First-Contact Protocol" (article-2-foundations-first-contact.md)
3. "SCOPE" (article-3-scope.md)

## Future Considerations

- WordPress migration: Markdown content transfers cleanly, URL structure can be preserved
- Framework section: When ready, add as a structured reference section
- Newsletter/RSS: Jekyll has built-in RSS support
- LeetPrompt.ai teaser page
- GenAI School podcast section
