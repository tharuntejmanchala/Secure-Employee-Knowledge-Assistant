from pypdf import PdfReader

filepath = "uploads/Tharun_Tej_Manchala_Resume (1).pdf"

reader = PdfReader(filepath)

text = ""

for page in reader.pages:
    text += page.extract_text()

chunks = []

chunk_size = 1000

for i in range(0, len(text), chunk_size):

    chunk = text[i:i + chunk_size]

    chunks.append(chunk)

print("Number of chunks:", len(chunks))

for index, chunk in enumerate(chunks):
    print("\nChunk", index + 1)
    print(chunk[:100])