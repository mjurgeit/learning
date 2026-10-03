"""Etsy listing generator + validator.

Config (JSON/dict):
{"product": "Weekly Budget Planner", "product_type": "printable PDF",
 "primary_keywords": ["budget planner printable", ...],      # ordered by priority
 "extra_tags": ["debt payoff"], "attributes": ["A4", "US Letter"],
 "audience": "...", "benefits": [...], "includes": [...], "how_to": [...],
 "ai_used": false, "faq": [["Q","A"]], "shop_policy": "..."}

Limits enforced (Etsy): title <=140 chars, 13 tags, each tag <=20 chars.
Heuristic warnings (blog-claim, not Etsy-verified): first 40 chars carry weight, repeated words,
ALL CAPS, special characters.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field

TITLE_MAX, TAG_MAX_LEN, TAG_COUNT = 140, 20, 13
AI_NOTICE = ("AI DISCLOSURE: Generative AI tools were used to help create parts of this product "
             "(designs/text). The design, selection and editing were done by the seller.")
TAG_ALLOWED = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 '\-]*$")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def build_title(keywords: list[str], max_len: int = TITLE_MAX, sep: str = ", ") -> str:
    """Greedily join keyword phrases (priority order) with commas, never exceeding max_len and never
    cutting a phrase mid-way. Skips phrases whose words are already all present."""
    out: list[str] = []
    seen_words: set[str] = set()
    for kw in keywords:
        kw = _norm(kw)
        words = {w.lower() for w in kw.split()}
        if not kw or words <= seen_words:
            continue
        cand = sep.join(out + [kw])
        if len(cand) <= max_len:
            out.append(kw)
            seen_words |= words
    return sep.join(out)


def _title_case(s: str) -> str:
    small = {"a", "an", "the", "of", "for", "and", "to", "in", "on", "with"}
    acronyms = {"pdf", "svg", "png", "diy", "kdp", "ai", "usa", "us", "uk", "a4", "a5", "tpt", "adhd", "jpg", "csv"}
    out = []
    for i, w in enumerate(s.split(" ")):
        core = w.strip(",").lower()
        if core in acronyms:
            out.append(w.upper().replace("A4", "A4"))
        elif i and core in small:
            out.append(w)
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def build_tags(keywords: list[str], extra: list[str] | None = None, attributes: list[str] | None = None) -> list[str]:
    """Pick up to 13 unique tags <=20 chars. Longer phrases are trimmed to their first words that fit
    (whole words only); duplicates are removed case-insensitively."""
    tags: list[str] = []
    seen: set[str] = set()
    for src in list(keywords) + list(extra or []) + list(attributes or []):
        src = _norm(re.sub(r"[^A-Za-z0-9 '\-]", " ", src))
        if not src:
            continue
        words, t = src.split(" "), ""
        for w in words:
            nxt = f"{t} {w}".strip()
            if len(nxt) <= TAG_MAX_LEN:
                t = nxt
            else:
                break
        key = t.lower()
        if t and key not in seen:
            tags.append(t.lower())
            seen.add(key)
        if len(tags) == TAG_COUNT:
            break
    return tags


def build_description(cfg: dict) -> str:
    p = cfg["product"]
    L: list[str] = []
    L.append(f"{p.upper()} - {cfg.get('product_type', 'instant digital download')}")
    if cfg.get("hook"):
        L += ["", cfg["hook"]]
    if cfg.get("benefits"):
        L += ["", "WHY YOU'LL LOVE IT"] + [f"- {b}" for b in cfg["benefits"]]
    if cfg.get("includes"):
        L += ["", "WHAT'S INCLUDED"] + [f"- {b}" for b in cfg["includes"]]
    if cfg.get("attributes"):
        L += ["", "SIZES / FORMATS: " + ", ".join(cfg["attributes"])]
    if cfg.get("how_to"):
        L += ["", "HOW IT WORKS"] + [f"{i}. {s}" for i, s in enumerate(cfg["how_to"], 1)]
    L += ["", "IMPORTANT: This is a DIGITAL product. No physical item will be shipped. "
              "Colors may vary slightly between screens and printers."]
    if cfg.get("ai_used"):
        L += ["", AI_NOTICE]
    if cfg.get("shop_policy"):
        L += ["", cfg["shop_policy"]]
    L += ["", "TERMS: Personal use only unless a commercial licence is stated. No resale or redistribution of the files."]
    if cfg.get("faq"):
        L += ["", "FAQ"]
        for q, a in cfg["faq"]:
            L += [f"Q: {q}", f"A: {a}"]
    return "\n".join(L)


def validate(title: str, tags: list[str], description: str = "", ai_used: bool = False) -> Report:
    r = Report()
    if not title:
        r.errors.append("title is empty")
    if len(title) > TITLE_MAX:
        r.errors.append(f"title is {len(title)} chars (max {TITLE_MAX})")
    if len(tags) > TAG_COUNT:
        r.errors.append(f"{len(tags)} tags (max {TAG_COUNT})")
    if len(tags) < TAG_COUNT:
        r.warnings.append(f"only {len(tags)}/{TAG_COUNT} tags used")
    low = [t.lower() for t in tags]
    for t in tags:
        if len(t) > TAG_MAX_LEN:
            r.errors.append(f"tag '{t}' is {len(t)} chars (max {TAG_MAX_LEN})")
        if not t.strip():
            r.errors.append("empty tag")
        elif not TAG_ALLOWED.match(t):
            r.errors.append(f"tag '{t}' has disallowed characters")
        if low.count(t.lower()) > 1:
            r.errors.append(f"duplicate tag '{t}'")
    r.errors = list(dict.fromkeys(r.errors))
    words = re.findall(r"[a-z0-9']+", title.lower())
    for w in set(words):
        if len(w) > 3 and words.count(w) > 3:
            r.warnings.append(f"word '{w}' repeated {words.count(w)}x in title (looks like stuffing)")
    if title and title.upper() == title and len(title) > 10:
        r.warnings.append("title is ALL CAPS")
    if sum(title.count(c) for c in "&%:") > 1:
        r.warnings.append("more than one of & % : in title (blog-claim: Etsy may reject)")
    if len(title) < 60:
        r.warnings.append("title shorter than 60 chars; unused keyword space")
    if ai_used and not re.search(r"\bAI\b|artificial intelligence", description, re.I):
        r.errors.append("ai_used is true but description lacks an AI disclosure")
    if ai_used:
        r.warnings.append("Also tick Etsy's AI-generated checkbox and choose 'Designed by a seller'.")
    return r


def generate(cfg: dict) -> dict:
    kws = cfg["primary_keywords"]
    title = cfg.get("title") or _title_case(build_title(kws + [cfg["product"]]))
    tags = cfg.get("tags") or build_tags(kws, cfg.get("extra_tags"), cfg.get("attributes"))
    desc = build_description(cfg)
    rep = validate(title, tags, desc, bool(cfg.get("ai_used")))
    return {"title": title, "tags": tags, "description": desc, "errors": rep.errors,
            "warnings": rep.warnings, "ok": rep.ok, "title_len": len(title)}


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Generate/validate an Etsy listing from a JSON config")
    ap.add_argument("config")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    res = generate(json.load(open(a.config, encoding="utf-8")))
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"TITLE ({res['title_len']}/{TITLE_MAX}):\n{res['title']}\n\nTAGS ({len(res['tags'])}/{TAG_COUNT}):")
        print(", ".join(res["tags"]))
        print("\nDESCRIPTION:\n" + res["description"])
        for e in res["errors"]:
            print("ERROR:", e)
        for w in res["warnings"]:
            print("WARN:", w)
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
