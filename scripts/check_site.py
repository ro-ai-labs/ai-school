#!/usr/bin/env python3
"""Check a built ai-school.ro site for the faults that have bitten it before.

Usage: python3 scripts/check_site.py _site [--projects _data/projects.yml]

Exit code 0 when every check passes, 1 otherwise (one line per failure).
Standard library only, so it runs on a bare CI runner.
"""
import argparse
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HOST = "ai-school.ro"
ORIGIN = "https://" + HOST
LANGS = ("en", "ro")
DEFAULT_LANG = "en"
PLACEMENTS = ("home", "article", "about", "footer")
BANNED_COPY = ("no upsells", "fara upsell", "fără upsell")
# ASCII spellings that mean a Romanian string lost its diacritics.
RO_ASCII = re.compile(
    r"\b(Acasa|Citeste|toata lumea|Urmatorul|disponibila|curand|Invata|Stii|Romana)\b",
    re.IGNORECASE,
)
REQUIRED_FILES = (
    "robots.txt",
    "sitemap.xml",
    "ro/sitemap.xml",
    "feed.xml",
    "ro/feed.xml",
    "404.html",
    "favicon.ico",
    "assets/img/favicon.svg",
    "assets/img/apple-touch-icon.png",
    "assets/img/og-image.png",
)
ARTICLE_RE = re.compile(r"^/articles/[^/]+/$")


class Page(HTMLParser):
    """Collects the parts of one HTML page the checks need."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_head = False
        self.in_title = False
        self.title = ""
        self.meta = {}
        self.canonical = None
        self.alternates = {}
        self.refs = []  # (tag, attribute dict, url, in_head)
        self.untranslated = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "head":
            self.in_head = True
        elif tag == "title":
            self.in_title = True
        if "data-untranslated" in a:
            self.untranslated = True
        if tag == "meta":
            key = a.get("name") or a.get("property")
            if key:
                self.meta[key] = (a.get("content") or "").strip()
        if tag == "link":
            rel = (a.get("rel") or "").lower()
            if rel == "canonical":
                self.canonical = a.get("href")
            elif rel == "alternate" and a.get("hreflang"):
                self.alternates[a["hreflang"]] = a.get("href")
        for attr in ("href", "src"):
            if a.get(attr) is not None:
                self.refs.append((tag, a, a[attr], self.in_head))

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        elif tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def url_path_of(rel):
    """index.html -> /, ro/about/index.html -> /ro/about/, 404.html -> /404.html"""
    rel = rel.as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def split_lang(path):
    """/ro/about/ -> ('ro', '/about/'); /about/ -> ('en', '/about/')"""
    if path == "/ro" or path.startswith("/ro/"):
        return "ro", path[3:] or "/"
    return DEFAULT_LANG, path


def lang_path(lang, inner):
    return inner if lang == DEFAULT_LANG else "/" + lang + inner


class Checker:
    def __init__(self, site_dir, projects_file):
        self.site = site_dir
        self.failures = []
        self.project_count = self.count_projects(projects_file)

    @staticmethod
    def count_projects(projects_file):
        text = projects_file.read_text(encoding="utf-8") if projects_file.is_file() else ""
        return len(re.findall(r"^- id:", text, flags=re.MULTILINE))

    def fail(self, check, where, message):
        self.failures.append(f"FAIL [{check}] {where}: {message}")

    def exists(self, path):
        path = path.split("#")[0].split("?")[0]
        if not path.startswith("/"):
            return False
        target = self.site / path.lstrip("/")
        if path.endswith("/"):
            return (target / "index.html").is_file()
        return target.is_file()

    def own_path(self, url):
        """Path of a URL on this site, or None when it points elsewhere."""
        parts = urlsplit(url)
        if parts.scheme in ("http", "https") and parts.netloc.lower() in (HOST, "www." + HOST):
            return parts.path or "/"
        if not parts.scheme and not parts.netloc and url.startswith("/"):
            return parts.path
        return None

    def check_page(self, file):
        where = url_path_of(file.relative_to(self.site))
        lang, inner = split_lang(where)
        raw = file.read_text(encoding="utf-8", errors="replace")
        page = Page()
        page.feed(raw)

        # Copy rules
        lowered = raw.lower()
        for phrase in BANNED_COPY:
            if phrase in lowered:
                self.fail("banned_copy", where, f"contains '{phrase}'")
        if lang == "ro":
            visible = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
            visible = re.sub(r"<[^>]+>", " ", visible)
            found = sorted({m.group(0) for m in RO_ASCII.finditer(visible)})
            if found:
                self.fail("ro_diacritics", where, "Romanian text without diacritics: " + ", ".join(found))

        # Metadata
        if not page.title.strip():
            self.fail("meta", where, "empty <title>")
        for key in ("description", "og:title", "og:description", "og:image", "og:url", "twitter:card"):
            if not page.meta.get(key):
                self.fail("meta", where, f"missing or empty meta '{key}'")
        if "\n" in page.meta.get("description", ""):
            self.fail("meta", where, "description spans several lines")

        # Links
        switchers = []
        series_links = []
        utm = Counter()
        for tag, attrs, url, in_head in page.refs:
            classes = (attrs.get("class") or "").split()
            parts = urlsplit(url)
            if parts.scheme in ("mailto", "tel", "data") or url.startswith("#") or url == "":
                continue
            own = self.own_path(url)

            if own is not None and (own == "/en" or own.startswith("/en/")):
                self.fail("no_en_prefix", where, f"{url} (English lives at the root, there is no /en/)")
                continue

            if own is None and not parts.scheme and not parts.netloc:
                self.fail("root_relative", where, f"relative link '{url}' (use a root-relative path)")
                continue

            if own is not None and parts.netloc and not in_head:
                self.fail("root_relative", where, f"absolute link to own site in body: {url}")

            if own is not None and not self.exists(own):
                self.fail("internal_targets_exist", where, f"{url} has no file behind it")

            if tag == "a" and not in_head:
                if "lang-toggle" in classes:
                    switchers.append(own)
                if "series-nav-title" in classes:
                    series_links.append(own)
                if (
                    lang == "ro"
                    and own is not None
                    and not own.startswith("/ro/")
                    and not own.startswith("/assets/")
                    and "lang-toggle" not in classes
                    and attrs.get("data-lang-link") != "en"
                ):
                    self.fail("ro_stays_ro", where, f"link leaves the Romanian site: {url}")
                query = parse_qs(parts.query)
                if query.get("utm_source") == [HOST]:
                    placement = (query.get("utm_content") or [""])[0]
                    utm[placement] += 1
                    if query.get("utm_medium") != ["site"]:
                        self.fail("projects", where, f"utm_medium is not 'site' on {url}")
                    if query.get("utm_campaign") != [lang]:
                        self.fail("projects", where, f"utm_campaign is not '{lang}' on {url}")
                    if placement not in PLACEMENTS:
                        self.fail("projects", where, f"unknown utm_content '{placement}' on {url}")

        # Language switcher
        other = "ro" if lang == DEFAULT_LANG else DEFAULT_LANG
        expected = lang_path(other, inner)
        if switchers != [expected]:
            self.fail("switcher", where, f"language switcher should link to {expected}, found {switchers}")

        # Canonical and hreflang
        en_url = ORIGIN + lang_path("en", inner)
        ro_url = ORIGIN + lang_path("ro", inner)
        own_url = ORIGIN + where
        if lang == "ro" and page.untranslated:
            want_canonical = en_url
            if "ro" in page.alternates:
                self.fail("hreflang", where, "untranslated page should not declare a Romanian alternate")
        else:
            want_canonical = own_url
            if lang == "ro" and page.alternates.get("ro") != ro_url:
                self.fail("hreflang", where, f"hreflang ro should be {ro_url}, found {page.alternates.get('ro')}")
        if page.canonical != want_canonical:
            self.fail("hreflang", where, f"canonical should be {want_canonical}, found {page.canonical}")
        for code in ("en", "x-default"):
            if page.alternates.get(code) != en_url:
                self.fail("hreflang", where, f"hreflang {code} should be {en_url}, found {page.alternates.get(code)}")
        for code, url in page.alternates.items():
            own = self.own_path(url or "")
            if own is None or not self.exists(own):
                self.fail("hreflang", where, f"hreflang {code} points at a missing page: {url}")

        # Series navigation
        if ARTICLE_RE.match(inner):
            inner_links = [split_lang(link)[1] for link in series_links if link]
            if inner in inner_links:
                self.fail("series_nav", where, "series navigation links to the article itself")
            if len(inner_links) != len(set(inner_links)):
                self.fail("series_nav", where, "previous and next point at the same article")

        # Project promotion
        if self.project_count == 0:
            self.fail("projects", where, "no projects found in the projects data file")
        else:
            wanted = {"footer"}
            if inner == "/":
                wanted.add("home")
            elif inner == "/about/":
                wanted.add("about")
            elif ARTICLE_RE.match(inner):
                wanted.add("article")
            for placement in PLACEMENTS:
                want = self.project_count if placement in wanted else 0
                if utm[placement] != want:
                    self.fail(
                        "projects",
                        where,
                        f"expected {want} project link(s) with utm_content={placement}, found {utm[placement]}",
                    )

    def check_files(self):
        for rel in REQUIRED_FILES:
            if not (self.site / rel).is_file():
                self.fail("files", "/" + rel, "missing")
        robots = self.site / "robots.txt"
        if robots.is_file():
            text = robots.read_text(encoding="utf-8", errors="replace")
            for sitemap in ("/sitemap.xml", "/ro/sitemap.xml"):
                if f"Sitemap: {ORIGIN}{sitemap}" not in text:
                    self.fail("files", "/robots.txt", f"does not list {ORIGIN}{sitemap}")
        for rel in ("sitemap.xml", "ro/sitemap.xml"):
            sitemap = self.site / rel
            if not sitemap.is_file():
                continue
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap.read_text(encoding="utf-8", errors="replace"))
            if not locs:
                self.fail("files", "/" + rel, "lists no URLs")
            for loc in locs:
                own = self.own_path(loc)
                if own is None or not loc.startswith(ORIGIN) or not self.exists(own):
                    self.fail("files", "/" + rel, f"lists a URL with no page behind it: {loc}")

    def run(self):
        pages = sorted(self.site.rglob("*.html"))
        if not pages:
            self.fail("files", str(self.site), "no HTML pages found; is this a built site?")
        for file in pages:
            self.check_page(file)
        self.check_files()
        return len(pages)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("site_dir", type=Path)
    parser.add_argument("--projects", type=Path, default=Path("_data/projects.yml"))
    args = parser.parse_args()
    if not args.site_dir.is_dir():
        print(f"FAIL [files] {args.site_dir}: not a directory")
        return 1
    checker = Checker(args.site_dir.resolve(), args.projects)
    pages = checker.run()
    for line in checker.failures:
        print(line)
    if checker.failures:
        checks = sorted({line.split("]")[0].split("[")[1] for line in checker.failures})
        print(f"\n{len(checker.failures)} failure(s) across {pages} page(s) in: {', '.join(checks)}")
        return 1
    print(f"OK: {pages} page(s), all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
