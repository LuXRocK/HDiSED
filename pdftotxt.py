import pdfplumber

with pdfplumber.open("wytyczne.pdf") as pdf:
    text = ""
    for page in pdf.pages:
        text += page.extract_text() + "\n"

with open("wytyczne.txt", "w", encoding="utf-8") as f:
    f.write(text)