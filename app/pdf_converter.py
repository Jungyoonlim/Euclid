import PyPDF2

def pdf_to_text(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfFileReader(file)
        text = ""
        for page in range(pdf_reader.numPages):
            text += pdf_reader.getPage(page).extractText()
    return text

    