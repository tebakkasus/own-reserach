import fitz  # PyMuPDF
import sys

doc = fitz.open(r"d:\tm\05_Own_Research\Papers_PDF\PIIS1201971222006440.pdf")
print(f"Total pages: {len(doc)}")

# Extract all text to a file
out_path = r"d:\tm\05_Own_Research\Papers_PDF\PIIS1201971222006440_text.txt"
with open(out_path, "w", encoding="utf-8") as f:
    for i, page in enumerate(doc):
        text = page.get_text()
        f.write(f"\n\n{'='*60}\n PAGE {i+1}\n{'='*60}\n")
        f.write(text)

print(f"Text extracted to: {out_path}")

# Print full text to stdout in utf-8 safe way
with open(out_path, "r", encoding="utf-8") as f:
    content = f.read()

# Print in chunks - avoid encoding issues
content_bytes = content.encode("utf-8", errors="replace").decode("ascii", errors="replace")
print(content_bytes[:15000])
