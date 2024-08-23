# labchip_pdf_splitter
Tool to split the pdf file from a LabChip system into one-file-per-page, each named based on OCR-ing the footer. 

Part of the pain of doing this is that our LabChip's PDF output does not contain text that can be parsed extract_text(), so OCR is needed. To make things easiest, this code just parses the footer. I had to set the dpi=300 or the accuracy of the OCR was horrible. 300 dpi seems to be pretty solid.

This needs you to install "tesseract", which is probably a yum/apt/brew/etc process. There doesn't appear to be any config of that module. I just did a `brew install tesseract` on my mac, and it worked. https://tesseract-ocr.github.io/tessdoc/Installation.html

"This project made use of coding assistance and support from an AI developed by OpenAI, integrated with PyMuPDF and pytesseract for processing PDF documents."
