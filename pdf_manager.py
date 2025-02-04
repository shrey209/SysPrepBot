from pypdf import PdfReader

pdf_file_path = ".\BartoSutton.pdf"

# reader = PdfReader(pdf_file_path)
# num_pages = len(reader.pages)

# print(f"Total Pages: {num_pages}\n")


# page = reader.pages[100]
  
# print(page.extract_text())


def read_page():
    reader=PdfReader(pdf_file_path)
    return reader.pages[100].extract_text()




