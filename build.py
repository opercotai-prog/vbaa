import frontmatter
import markdown
from pathlib import Path
from jinja2 import Template

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
DIST = ROOT / "dist"
TEMPLATE = Template((ROOT / "templates" / "card.html").read_text(encoding="utf-8"))

DIST.mkdir(exist_ok=True)

cards = []
for path in sorted(CONTENT.rglob("*.md")):
    post = frontmatter.load(path)
    md = markdown.Markdown(extensions=["fenced_code"])
    body_html = md.convert(post.content)
    html = TEMPLATE.render(
        title=post.metadata.get("title", path.stem),
        category=path.parent.name,
        description=post.metadata.get("description", ""),
        warnings=post.metadata.get("warnings", []),
        body=body_html,
    )
    out = DIST / f"{path.stem}.html"
    out.write_text(html, encoding="utf-8")
    cards.append({
        "title": post.metadata.get("title", path.stem),
        "description": post.metadata.get("description", ""),
        "file": f"{path.stem}.html",
    })

index_html = "<!DOCTYPE html><html lang='ru'><head><meta charset='utf-8'><title>Справочник макросов</title>"
index_html += "<style>body{font-family:system-ui,sans-serif;max-width:800px;margin:2em auto;padding:0 1em;line-height:1.5}</style></head><body>"
index_html += "<h1>Справочник макросов</h1><ul>"
for c in cards:
    index_html += f'<li><a href="{c["file"]}"><b>{c["title"]}</b></a> — {c["description"]}</li>'
index_html += "</ul></body></html>"
(DIST / "index.html").write_text(index_html, encoding="utf-8")

print(f"Собрано карточек: {len(cards)}")
