import json
from pathlib import Path

root = Path(__file__).parent
exts = {".png", ".jpg", ".jpeg", ".webp"}
items = []
for p in sorted((root / "images").rglob("*")):
    if p.suffix.lower() not in exts or p.parent == root / "images":
        continue
    name, _, brand = p.stem.partition(" - ")
    items.append({
        "name": name.strip(),
        "type": p.parent.name.replace("_", "/"),
        "image": p.relative_to(root).as_posix(),
        "brand": brand.strip(),
        "day": "",
    })

(root / "items.js").write_text("const ITEMS = " + json.dumps(items, indent=2, ensure_ascii=False) + ";\n", encoding="utf-8")
print(f"Wrote {len(items)} items to items.js")
