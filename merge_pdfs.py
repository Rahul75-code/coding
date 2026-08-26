from pathlib import Path
from pypdf import PdfReader, PdfWriter

files = [
    Path(r"c:/Users/ASUS/Desktop/office/Rahul_docs/b.tech provisional certificate.pdf"),
    Path(r"c:/Users/ASUS/Desktop/office/Rahul_docs/b. tech marksheet.pdf"),
]
out_file = Path(r"c:/Users/ASUS/Desktop/office/Rahul_docs/merged_documents.pdf")

writer = PdfWriter()
for path in files:
    reader = PdfReader(str(path))
    for page in reader.pages:
        writer.add_page(page)

with out_file.open("wb") as f:
    writer.write(f)

print(out_file)
