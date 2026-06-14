from pypdf import PdfReader

filepath = "uploads/Tharun_Tej_Manchala_Resume (1).pdf"

reader = PdfReader(filepath)

text = ""

for page in reader.pages:
    text += page.extract_text()

print(text)