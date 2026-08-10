"""Science accuracy review of activemillers case study articles using local Ollama (deepseek-r1:14b).
Reads articles-markdown/*.md, sends each to the local model for a fact-check pass,
writes findings to science-review/<slug>.md and a combined science-review/SUMMARY.md.

Usage: python review_articles_science.py [--model deepseek-r1:14b]
"""
import os, sys, glob, json, argparse, urllib.request, re, time

SITE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD_DIR = os.path.join(SITE_DIR, "articles-markdown")
OUT_DIR = os.path.join(SITE_DIR, "science-review")
os.makedirs(OUT_DIR, exist_ok=True)

OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434").rstrip("/")

SYSTEM_PROMPT = """You are a board-certified pathologist and physician-scientist reviewing medical illustration article copy for scientific accuracy before publication on a professional medical illustration portfolio site (activemillers.com).

Review the article text for:
1. Factual errors in mechanism, pathophysiology, pharmacology, or anatomy
2. Outdated or superseded clinical guidelines (drug names, dosing, first-line therapy)
3. Oversimplifications that cross into being misleading
4. Any claim you are not confident is correct — flag it explicitly rather than staying silent

Do NOT comment on writing style, tone, or prose quality. ONLY comment on scientific/medical accuracy.

Output format — a markdown bullet list. For each issue:
- **Location:** which section/sentence
- **Issue:** what's wrong or questionable
- **Correction:** the accurate version, if you know it

If the article is fully accurate, say exactly: "No accuracy issues found." and nothing else.
Be concise. Do not restate the whole article."""

def call_ollama(model, article_text, timeout=180):
    prompt = f"{SYSTEM_PROMPT}\n\n---ARTICLE---\n\n{article_text}\n\n---END ARTICLE---\n\nYour review:"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 8192}
    }).encode("utf-8")
    req = urllib.request.Request(f"{OLLAMA}/api/generate", data=payload,
                                  headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("response", "")

def strip_think(text):
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="deepseek-r1:14b")
    args = ap.parse_args()

    md_files = sorted(glob.glob(os.path.join(MD_DIR, "*.md")))
    print(f"Reviewing {len(md_files)} articles with {args.model}\n")

    summary_lines = ["# Science Review Summary", "", f"Model: `{args.model}`", ""]

    for i, md_path in enumerate(md_files, 1):
        slug = os.path.splitext(os.path.basename(md_path))[0]
        with open(md_path, "r", encoding="utf-8") as f:
            article_text = f.read()

        title_match = re.search(r"^# (.+)$", article_text, re.MULTILINE)
        title = title_match.group(1) if title_match else slug

        print(f"[{i}/{len(md_files)}] {title}...", flush=True)
        t0 = time.time()
        try:
            raw = call_ollama(args.model, article_text)
            review = strip_think(raw)
        except Exception as e:
            review = f"ERROR: {e}"
        elapsed = time.time() - t0
        print(f"    done in {elapsed:.1f}s")

        out_path = os.path.join(OUT_DIR, f"{slug}.md")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(f"# Science Review: {title}\n\n{review}\n")

        has_issues = "No accuracy issues found" not in review
        flag = "⚠️ ISSUES" if has_issues else "✓ clean"
        summary_lines.append(f"- **{title}** ({flag}) — [{slug}.md]({slug}.md)")

    summary_path = os.path.join(OUT_DIR, "SUMMARY.md")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines) + "\n")

    print(f"\nDone. Reviews in: {OUT_DIR}")
    print(f"Summary: {summary_path}")
