import sys
import fitz  # PyMuPDF
import os

def extract_data_from_pdf(pdf_path):
    """
    Extracts text and images from a specified PDF file.

    Args:
        pdf_path (str): The file path to the PDF.

    Returns:
        str: The extracted text, or an error message if extraction fails.
    """
    try:
        # Create a directory to store images, named after the PDF
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        image_dir = f"images_from_{base_name}"
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        
        print(f"Images will be saved in: '{image_dir}/'")
        
        # Open the PDF file
        doc = fitz.open(pdf_path)
            
        # Get the number of pages
        num_pages = doc.page_count
        print(f"Total pages found: {num_pages}")
            
        # Initialize an empty string to store all the text
        full_text = ""
        image_count = 0
            
        # Loop through each page and extract text and images
        for page_num in range(num_pages):
            page = doc.load_page(page_num)
            
            # --- Extract Text ---
            text = page.get_text()
            if text:
                full_text += text
                full_text += f"\n--- End of Page {page_num + 1} ---\n"
            else:
                print(f"No text found on page {page_num + 1}")

            # --- Extract Images ---
            image_list = page.get_images(full=True)
            
            if image_list:
                print(f"Found {len(image_list)} images on page {page_num + 1}")
                for img_index, img in enumerate(image_list):
                    # Get the XREF of the image
                    xref = img[0]
                    
                    # Extract the image bytes
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    
                    # Save the image
                    image_filename = f"{image_dir}/page{page_num+1}_img{img_index+1}.{image_ext}"
                    with open(image_filename, "wb") as img_file:
                        img_file.write(image_bytes)
                    image_count += 1

        doc.close()

        if not full_text and image_count == 0:
            return "No extractable text or images found in the PDF."
        
        print(f"\nTotal images extracted: {image_count}")
        return full_text

    except FileNotFoundError:
        return f"Error: The file '{pdf_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"

# --- How to use this script ---
# 1. Save this code as a Python file (e.g., extract_pdf_text.py).
# 2. Make sure you have PyMuPDF installed (see how_to_run.md).
# 3. Place the PDF you want to read in the same directory as this script.
# 4. Change 'your_file.pdf' to the actual name of your PDF file.
# 5. Run the script from your terminal: python extract_pdf_text.py
if __name__ == "__main__":
    # --- IMPORTANT ---
    # Change this to the name of your PDF file
    pdf_file_name = 'my_report.pdf'
    
    print(f"Attempting to extract data from: {pdf_file_name}...\n")
    
    # Call the function and store the result
    extracted_data = extract_data_from_pdf(pdf_file_name)
    
    # Print the extracted text
    print("\n--- Extracted Text ---")
    print(extracted_data)
    print("------------------------")

    # Optional: Save the extracted text to a .txt file
    try:
        output_filename = f"extracted_text_from_{pdf_file_name.replace('.pdf', '')}.txt"
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(extracted_data)
        print(f"\nSuccessfully saved extracted text to: {output_filename}")
    except Exception as e:
        print(f"Could not save text to file: {e}")