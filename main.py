import os
from pdf_processor import setup_openai_api, read_pdf, extract_data_from_pdf
from csv_maker import save_to_csv

def main():
    setup_openai_api()
    
    # Get user input for data fields to extract
    print("Enter the data fields you want to extract (comma-separated):")
    data_fields = [field.strip() for field in input().split(',')]
    
    # Get user input for PDF files
    print("Enter the paths to the PDF files (comma-separated):")
    pdf_files = [path.strip() for path in input().split(',')]
    
    extracted_data = []
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            print(f"File not found: {pdf_file}")
            continue
        
        pdf_text = read_pdf(pdf_file)
        data = extract_data_from_pdf(pdf_text, data_fields)
        extracted_data.append(data)
    
    if extracted_data:
        output_file = "extracted_data.csv"
        save_to_csv(extracted_data, output_file)
        print(f"Data has been extracted and saved to {output_file}")
    else:
        print("No data was extracted.")

if __name__ == "__main__":
    main()