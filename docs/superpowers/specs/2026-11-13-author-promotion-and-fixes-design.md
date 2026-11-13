# ai-school.ro: author promotion and site fixes

Date: 2026-11-13. Approved by Mihai in conversation the same day.

## Intent

AI School should also promote its author. Today the site names Mihai once on the About page and links only to LinkedIn. It never mentions his other projects, and several things on the live site are broken, which makes it a poor place to send people.

After this change, a reader who finishes an article knows who wrote it and has an obvious next step into one of four projects:

| Project | What it is | Reader it serves |
|---|---|---|
| Let's Talk AI (lets-talk-ai.ro) | Free monthly AI mixer in Bucharest | Wants to talk about AI in person |
| AI Labs (ai-labs.ro) | AI strategy and workshops for companies | Wants this for their team |
| AI Leaders Romania (ai-leaders.ro) | Network of AI practitioners | Has an AI decision to make |
| Ship It With AI (ship-it-with.ai) | Free field manual on AI coding agents | Builds software with AI |

## Goals

- Every page links to the four projects. The home page and every article give them real space.
- The author is visible: a bio on every article and a fuller About page.
- The live site has no broken navigation in either language.
- Shared links (LinkedIn first) show a title, description and image.

## Non-goals

- Translating the three articles into Romanian. Until then, Romanian cards are marked "in English" and link to the English article.
- Adding links back to ai-school.ro from the four project sites. Those are other repositories.
- New articles, a newsletter, analytics, a photo of the author.

## Anti-goals

- No promotion inside the article text. The lessons stay free of pitches.
- No "book a call" banners, pop-ups or nav buttons. AI School is a free school first.
- No claim on the site that stops being true. "No upsells" is removed because two of the four projects are commercial.

## Approaches considered

1. **Footer links only.** Smallest change, but four small links at the bottom of a page do not promote anyone. Rejected as too weak.
2. **Sales calls to action** (a "Book a call" button in the nav, banners inside articles). Strongest push, but it contradicts the free-school promise and the voice of the articles. Rejected.
3. **"Who is behind this and where to go next"** (chosen). Promotion sits around the articles, never inside them, and is framed as honest attribution: who writes this, and what else he does. Each project is matched to a reason a reader might want it.

## Design

**One source for the four projects.** `_data/projects.yml` holds each project's name, role of the author, per-language URL, and per-language copy. Every placement reads from it, so a change is made once.

**Placements.**

- Home: a "Go further" section under the articles, one card per project (reader's need, project name, two sentences, link).
- Article: an "About the author" box after the text, before the series navigation. Short bio, the four projects as one line each, LinkedIn.
- About: bio first, then mission and SPARKS-SIX as today, then "What else Mihai does" with the four projects and his role in each. Written in both languages.
- Footer: a row "Also by Mihai Cvasnievschi" with the four names, on every page.

**Links.** Language-aware (ai-labs.ro/ro/, lets-talk-ai.ro/ro/, ai-leaders.ro/en/, ship-it-with.ai/ro/). Each carries `utm_source=ai-school.ro&utm_medium=site&utm_campaign=<lang>&utm_content=<placement>`, the same convention ai-labs.ro already uses.

**Wording.** Hero and About: "No upsells" becomes "No sign-up". Everything on AI School itself stays free and the copy keeps saying so.

**Fixes.**

- Internal links are built from `site.baseurl` so Romanian pages stay in Romanian. (`relative_url` returns the English path on Romanian pages under the multi-language plugin.)
- Language switcher uses root-relative paths: English at `/…`, Romanian at `/ro/…`.
- `hreflang` and canonical tags point at real URLs. Untranslated Romanian articles declare the English article as canonical.
- Series navigation computes previous and next correctly.
- Untranslated Romanian articles are listed in `_data/untranslated.yml`, which both language builds read. Cards and series links for them go to the English article and carry an "in English" tag. The Romanian placeholder page says so plainly and links across.
- Romanian UI strings get diacritics and lose the stray English. Dates on Romanian pages use Romanian month names.
- Page titles and descriptions: home gets a descriptive title, articles use their written excerpt.
- Open Graph and Twitter tags on every page, with a 1200×630 share image.
- Favicon, `robots.txt`, `sitemap.xml` per language, Atom feed per language, a custom 404 page.
- Articles link to each other on the site instead of on LinkedIn.
- Gold label text is darkened to meet 4.5:1 contrast. Card dates no longer wrap. The home heading says "Latest articles" and links to the full list.

## Constraints

- Jekyll 4 with jekyll-multiple-languages-plugin, built by GitHub Actions. No new gems.
- Site copy follows the articles' voice: plain, warm, no dashes.
- Facts about the four projects come from their live sites as read on 2026-11-13.

## Needs Mihai's separate approval

- GitHub Pages settings: re-save the custom domain to trigger the HTTPS certificate, turn on "Enforce HTTPS", and switch the Pages source to GitHub Actions so the failing branch build stops running.
- Pushing to `main`, which deploys.

## Left to the builder

Exact CSS, the favicon and share image artwork, and the Romanian phrasing, all within the existing warm editorial style.
