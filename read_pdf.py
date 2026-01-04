import PyPDF2

def extract_pdf_text(pdf_path, output_file):
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            with open(output_file, 'w', encoding='utf-8') as out:
                out.write(f"Total Pages: {len(pdf_reader.pages)}\n")
                out.write("=" * 80 + "\n\n")
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    out.write(f"\n--- PAGE {page_num} ---\n\n")
                    text = page.extract_text()
                    out.write(text)
                    out.write("\n\n" + "=" * 80 + "\n")
                    
        print(f"✓ Successfully extracted PDF to {output_file}")
        return True
                
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    pdf_path = "Component 8.pdf"
    output_file = "component8_extracted.txt"
    extract_pdf_text(pdf_path, output_file)
