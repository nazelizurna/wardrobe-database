import csv
from pathlib import Path

root = Path(__file__).parent
csv_path = root / "wardrobe.csv"
cols = ["image", "name", "type", "brand", "color", "day"]
delim, rows = ",", []

if csv_path.exists():
    text = csv_path.read_text(encoding="utf-8-sig")
    head = text.splitlines()[0] if text else ""
    delim = ";" if head.count(";") > head.count(",") else ","
    rows = list(csv.DictReader(text.splitlines(), delimiter=delim))

known = {r["image"] for r in rows}
added = 0
for p in sorted((root / "images").rglob("*")):
    rel = p.relative_to(root).as_posix()
    if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and p.parent != root / "images" and rel not in known:
        rows.append({"image": rel, "name": p.stem.replace("-", " ").replace("_", " "),
                     "type": p.parent.name.replace("_", "/"), "brand": "", "color": "", "day": ""})
        added += 1

with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=delim, extrasaction="ignore")
    w.writeheader()
    w.writerows(rows)
print(f"Added {added} new rows, {len(rows)} total in wardrobe.csv")
