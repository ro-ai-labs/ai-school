#!/usr/bin/env python3
"""Check a built ai-school.ro site for the faults that have bitten it before.

Usage: python3 scripts/check_site.py _site [--projects _data/projects.yml]

Exit code 0 when every check passes, 1 otherwise (one line per failure).
Standard library only, so it runs on a bare CI runner.
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

HOST = "ai-school.ro"
ORIGIN = "https://" + HOST
LANGS = ("en", "ro")
DEFAULT_LANG = "en"
PLACEMENTS = ("home", "article", "about", "footer", "author", "mentorship")
# Single links (a call to action, a profile link) carry these and are not counted.
FREE_PLACEMENTS = ("cta", "profile")
AUTHOR = "Mihai Cvasnievschi"
AUTHOR_PATH = "/mihai-cvasnievschi/"
MENTORSHIP_PATH = "/ai-mentorship/"
LINKEDIN = "https://www.linkedin.com/in/mihaicvasnievschi/"
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
    "assets/img/og-author.png",
    "assets/img/mihai-cvasnievschi.jpg",
    "assets/fonts/inter-latin.woff2",
    "assets/fonts/lora-latin.woff2",
    "llms.txt",
    "llms-full.txt",
    "mihai-cvasnievschi/index.html",
    "ro/mihai-cvasnievschi/index.html",
    "ai-mentorship/index.html",
    "ro/ai-mentorship/index.html",
)
ARTICLE_RE = re.compile(r"^/articles/[^/]+/$")
# JSON-LD ids that mean the same thing on every page. Any other id on this site
# belongs to one page and must start with that page's own URL.
SITE_WIDE_IDS = (ORIGIN + "/#website", ORIGIN + "/#school", ORIGIN + AUTHOR_PATH + "#person")


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
        self.h1 = 0
        self.images = []  # attribute dicts
        self.jsonld = []  # text of each JSON-LD block
        self.text = []  # visible text
        self.in_jsonld = False
        self.hidden = None  # "script" or "style" while inside one
        self.headings = []  # heading levels, in page order
        self.crumbs = []  # text of each step of the visible breadcrumb
        self.in_crumbs = False
        self.in_crumb = False
        self.faq_items = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "head":
            self.in_head = True
        elif tag == "title":
            self.in_title = True
        if "data-untranslated" in a:
            self.untranslated = True
        classes = (a.get("class") or "").split()
        if re.fullmatch(r"h[1-6]", tag):
            self.headings.append(int(tag[1]))
        if tag == "nav" and "breadcrumbs" in classes:
            self.in_crumbs = True
        elif tag == "li" and self.in_crumbs:
            self.crumbs.append("")
            self.in_crumb = True
        if "faq-item" in classes:
            self.faq_items += 1
        if tag == "h1":
            self.h1 += 1
        elif tag == "img":
            self.images.append(a)
        elif tag in ("script", "style"):
            self.hidden = tag
            if a.get("type") == "application/ld+json":
                self.in_jsonld = True
                self.jsonld.append("")
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
        if tag == self.hidden:
            self.hidden = None
            self.in_jsonld = False
        if tag == "li":
            self.in_crumb = False
        elif tag == "nav":
            self.in_crumbs = False
            self.in_crumb = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_crumb:
            self.crumbs[-1] += data
        if self.in_jsonld:
            self.jsonld[-1] += data
        elif self.hidden is None and not self.in_head:
            self.text.append(data)


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
        # Filled while reading pages, compared across languages afterwards.
        self.ro_alternate_on_en = {}  # inner path -> hreflang "ro" URL declared by the English page
        self.ro_pages = {}  # inner path -> True when the Romanian page is a "not translated" placeholder
        self.id_urls = defaultdict(set)  # JSON-LD @id -> every "url" given for it, on any page

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
        length = len(page.meta.get("description", ""))
        if length and not 50 <= length <= 200:
            self.fail("meta", where, f"description is {length} characters (want 50 to 200)")
        if page.meta.get("author") != AUTHOR:
            self.fail("meta", where, f"meta author should be '{AUTHOR}', found {page.meta.get('author')!r}")

        # Page structure
        if page.h1 != 1:
            self.fail("headings", where, f"expected exactly one <h1>, found {page.h1}")
        if page.headings and page.headings[0] != 1:
            self.fail("headings", where, f"the first heading is <h{page.headings[0]}>, not <h1>")
        for above, below in zip(page.headings, page.headings[1:]):
            if below > above + 1:
                self.fail("headings", where, f"heading levels skip from <h{above}> to <h{below}>")
                break
        if page.untranslated and page.meta.get("og:locale") == "ro_RO":
            self.fail("meta", where, "og:locale is ro_RO on a page whose share link is the English article")
        for image in page.images:
            if "alt" not in image:
                self.fail("images", where, f"image without alt text: {image.get('src')}")
            if not (image.get("width") and image.get("height")):
                self.fail("images", where, f"image without width and height: {image.get('src')}")
        if "fonts.googleapis.com" in raw or "fonts.gstatic.com" in raw:
            self.fail("fonts", where, "loads fonts from Google instead of this site")
        self.check_structured_data(where, lang, inner, page)

        # Links
        switchers = []
        series_links = []
        own_links = set()
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
                if own is not None:
                    own_links.add(split_lang(own)[1])
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
                    if placement not in PLACEMENTS + FREE_PLACEMENTS:
                        self.fail("projects", where, f"unknown utm_content '{placement}' on {url}")

        # Every page leads to the author and to the mentorship page
        for target in (AUTHOR_PATH, MENTORSHIP_PATH):
            if target not in own_links:
                self.fail("author_links", where, f"no link to {lang_path(lang, target)}")

        # Language switcher
        other = "ro" if lang == DEFAULT_LANG else DEFAULT_LANG
        expected = lang_path(other, inner)
        if switchers != [expected]:
            self.fail("switcher", where, f"language switcher should link to {expected}, found {switchers}")

        # Canonical and hreflang
        en_url = ORIGIN + lang_path("en", inner)
        ro_url = ORIGIN + lang_path("ro", inner)
        own_url = ORIGIN + where
        if lang == "ro":
            self.ro_pages[inner] = page.untranslated
        else:
            self.ro_alternate_on_en[inner] = page.alternates.get("ro")
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
            elif inner == AUTHOR_PATH:
                wanted.add("author")
            elif inner == MENTORSHIP_PATH:
                wanted.add("mentorship")
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

    def check_structured_data(self, where, lang, inner, page):
        """Search engines and AI assistants read the JSON-LD; it must parse and say who the author is."""
        if not page.jsonld:
            self.fail("structured_data", where, "no JSON-LD block")
            return
        nodes = []
        for block in page.jsonld:
            try:
                data = json.loads(block)
            except ValueError as error:
                self.fail("structured_data", where, f"JSON-LD does not parse: {error}")
                return
            items = data.get("@graph", [data]) if isinstance(data, dict) else data
            nodes.extend(node for node in items if isinstance(node, dict))

        def of_type(name):
            return [n for n in nodes if name in (n["@type"] if isinstance(n.get("@type"), list) else [n.get("@type")])]

        def strings(value):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for item in value.values():
                    yield from strings(item)
            elif isinstance(value, list):
                for item in value:
                    yield from strings(item)

        for value in strings(nodes):
            if "<" in value or "{{" in value or "{%" in value:
                self.fail("structured_data", where, f"markup inside a JSON-LD string: {value[:60]!r}")
            if value.startswith("http://"):
                self.fail("structured_data", where, f"http:// URL in JSON-LD: {value}")
            own = self.own_path(value) if value.startswith("https://") else None
            if own is not None and not self.exists(own):
                self.fail("structured_data", where, f"JSON-LD names a page that does not exist: {value}")

        people = [n for n in of_type("Person") if n.get("name") == AUTHOR]
        if len(people) != 1:
            self.fail("structured_data", where, f"expected one Person node for {AUTHOR}, found {len(people)}")
            return
        person = people[0]
        # One person, one address: the same on English and Romanian pages.
        want_url = ORIGIN + AUTHOR_PATH
        if person.get("url") != want_url:
            self.fail("structured_data", where, f"Person url should be {want_url}, found {person.get('url')}")
        if LINKEDIN not in (person.get("sameAs") or []):
            self.fail("structured_data", where, "Person sameAs does not include the LinkedIn profile")
        for key in ("@id", "jobTitle", "description", "image", "knowsAbout"):
            if not person.get(key):
                self.fail("structured_data", where, f"Person has no {key}")
        if not of_type("WebSite"):
            self.fail("structured_data", where, "no WebSite node")

        own_url = ORIGIN + where
        for node in nodes:
            node_id = node.get("@id")
            if not isinstance(node_id, str):
                continue
            if isinstance(node.get("url"), str):
                self.id_urls[node_id].add(node["url"])
            if node_id.startswith(ORIGIN) and node_id not in SITE_WIDE_IDS and not node_id.startswith(own_url + "#"):
                self.fail("structured_data", where, f"JSON-LD id belongs to another page: {node_id}")

        if page.untranslated:
            if of_type("Article"):
                self.fail("structured_data", where, "an untranslated placeholder is marked up as an Article")
        elif ARTICLE_RE.match(inner):
            articles = of_type("Article")
            if len(articles) != 1:
                self.fail("structured_data", where, f"expected one Article node, found {len(articles)}")
            else:
                article = articles[0]
                for key in ("headline", "description", "image", "inLanguage"):
                    if not article.get(key):
                        self.fail("structured_data", where, f"Article has no {key}")
                if not re.match(r"^\d{4}-\d{2}-\d{2}", str(article.get("datePublished"))):
                    self.fail("structured_data", where, f"Article datePublished is not a date: {article.get('datePublished')}")
                if (article.get("author") or {}).get("@id") != person["@id"]:
                    self.fail("structured_data", where, "Article author is not the Person node")
                if article.get("mainEntityOfPage") != own_url:
                    self.fail("structured_data", where, f"Article mainEntityOfPage should be {own_url}")
        crumbs = of_type("BreadcrumbList")
        items = (crumbs[0].get("itemListElement") or []) if crumbs else []
        if inner != "/" and where not in ("/404.html", "/ro/404.html"):
            if len(items) < 2:
                self.fail("structured_data", where, "no BreadcrumbList with at least two steps")
            elif items[-1].get("item") != own_url:
                self.fail("structured_data", where, f"last breadcrumb should be {own_url}, found {items[-1].get('item')}")
        # What search engines are told must be what the reader sees.
        told = [" ".join(str(item.get("name", "")).split()) for item in items]
        shown = [" ".join(text.split()) for text in page.crumbs]
        if told != shown:
            self.fail("structured_data", where, f"breadcrumb in JSON-LD {told} differs from the one on the page {shown}")
        if page.untranslated:
            return
        if inner == AUTHOR_PATH:
            profiles = of_type("ProfilePage")
            if not profiles or (profiles[0].get("mainEntity") or {}).get("@id") != person["@id"]:
                self.fail("structured_data", where, "no ProfilePage whose mainEntity is the Person node")
        if inner == MENTORSHIP_PATH:
            visible = " ".join(" ".join(page.text).split())
            faqs = of_type("FAQPage")
            questions = (faqs[0].get("mainEntity") or []) if faqs else []
            if len(questions) < 3:
                self.fail("structured_data", where, f"FAQPage needs at least 3 questions, found {len(questions)}")
            if page.faq_items != len(questions):
                self.fail(
                    "structured_data",
                    where,
                    f"{page.faq_items} question(s) on the page but {len(questions)} in the JSON-LD",
                )
            for question in questions:
                name = " ".join(str(question.get("name", "")).split())
                answer = " ".join(str((question.get("acceptedAnswer") or {}).get("text", "")).split())
                if not name or name not in visible:
                    self.fail("structured_data", where, f"FAQ question is not on the page: {name[:70]!r}")
                if not answer or answer not in visible:
                    self.fail("structured_data", where, f"FAQ answer is not on the page as written: {answer[:70]!r}")

    def check_language_pairs(self):
        """An English page may name a Romanian alternate only when that page is a real translation."""
        for inner, declared in sorted(self.ro_alternate_on_en.items()):
            where = lang_path("en", inner)
            ro_url = ORIGIN + lang_path("ro", inner)
            if inner not in self.ro_pages:
                if declared:
                    self.fail("hreflang", where, f"declares a Romanian alternate that was not built: {declared}")
            elif self.ro_pages[inner]:
                if declared:
                    self.fail(
                        "hreflang",
                        where,
                        f"declares {declared} as its Romanian version, but that page is an untranslated placeholder",
                    )
            elif declared != ro_url:
                self.fail("hreflang", where, f"hreflang ro should be {ro_url}, found {declared}")

    def check_shared_ids(self):
        """A thing named by one JSON-LD id has one address, whichever page or language mentions it."""
        for node_id, urls in sorted(self.id_urls.items()):
            if len(urls) > 1:
                self.fail("structured_data", node_id, "has more than one url across pages: " + ", ".join(sorted(urls)))

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
            if re.search(r"(?im)^disallow:\s*/\s*$", text):
                self.fail("files", "/robots.txt", "blocks a crawler from the whole site")
        for rel in ("llms.txt", "ro/llms.txt"):
            llms = self.site / rel
            if not llms.is_file():
                self.fail("files", "/" + rel, "missing")
                continue
            text = llms.read_text(encoding="utf-8", errors="replace")
            if not text.startswith("# ") or AUTHOR not in text or "{{" in text or "<" in text:
                self.fail("files", "/" + rel, "should be plain Markdown that starts with a title and names the author")
            for link in re.findall(r"\]\((https://[^)\s]+)\)", text):
                own = self.own_path(link)
                if own is not None and not self.exists(own):
                    self.fail("files", "/" + rel, f"links to a page that does not exist: {link}")
            if len(re.findall(r"\]\(" + re.escape(ORIGIN) + r"(?:/ro)?/articles/[^/)]+/\)", text)) < 1:
                self.fail("files", "/" + rel, "does not link to any article")
        full = self.site / "llms-full.txt"
        if full.is_file():
            text = full.read_text(encoding="utf-8", errors="replace")
            if AUTHOR not in text or re.search(r"</?[a-zA-Z][a-zA-Z0-9]*[\s>]", text) or "{{" in text:
                self.fail("files", "/llms-full.txt", "should be plain text that names the author")
            if not re.search(r"(?m)^### \S", text):
                self.fail("files", "/llms-full.txt", "article section headings were lost")
        for rel in ("sitemap.xml", "ro/sitemap.xml"):
            sitemap = self.site / rel
            if not sitemap.is_file():
                continue
            locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", sitemap.read_text(encoding="utf-8", errors="replace"))
            if not locs:
                self.fail("files", "/" + rel, "lists no URLs")
            prefix = ORIGIN + ("/ro" if rel.startswith("ro/") else "")
            for path in (AUTHOR_PATH, MENTORSHIP_PATH):
                if prefix + path not in locs:
                    self.fail("files", "/" + rel, f"does not list {prefix + path}")
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
        self.check_language_pairs()
        self.check_shared_ids()
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
