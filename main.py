import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import letter
import io

def change_pdf_background(input_path, output_path, color=(0.9, 0.9, 0.8)):  # Default light cream color
    """
    Change the background color of all pages in a PDF file.

    Args:
        input_path (str): Path to the input PDF file
        output_path (str): Path where the modified PDF will be saved
        color (tuple): RGB color values between 0 and 1 (default: light cream)
    """
    try:
        # Read the original PDF
        reader = PdfReader(input_path)
        writer = PdfWriter()

        # Process each page
        for page_num in range(len(reader.pages)):
            # Get the page
            page = reader.pages[page_num]

            # Get page size
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)

            # Create a background page with desired color
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=(page_width, page_height))

            # Set the background color
            can.setFillColor(Color(color[0], color[1], color[2]))
            can.rect(0, 0, page_width, page_height, fill=True)
            can.save()

            # Move to the beginning of the BytesIO buffer
            packet.seek(0)

            # Create PDF page from the background
            background = PdfReader(packet).pages[0]

            # Merge background with content
            background.merge_page(page)
            writer.add_page(background)

        # Save the modified PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        print(f"Successfully created PDF with modified background: {output_path}")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

def main():
    """
    Main function to handle user input and call the PDF modification function.
    """
    # Get input from user
    input_path = input("Enter the path to your PDF file: ").strip()

    # Validate input file
    if not os.path.exists(input_path):
        print("Error: The specified file does not exist.")
        return

    if not input_path.lower().endswith('.pdf'):
        print("Error: The specified file is not a PDF.")
        return

    # Get color preference
    print("\nEnter RGB values (0-255) for the background color")
    try:
        r = int(input("Red (0-255): ")) / 255
        g = int(input("Green (0-255): ")) / 255
        b = int(input("Blue (0-255): ")) / 255

        # Validate color values
        if not all(0 <= x <= 1 for x in [r, g, b]):
            raise ValueError("Color values must be between 0 and 255")

    except ValueError:
        print("Invalid color values. Using default light cream color.")
        r, g, b = 0.9, 0.9, 0.8

    # Create output filename
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_colored.pdf"

    # Change the background color
    success = change_pdf_background(input_path, output_path, (r, g, b))

    if success:
        print("\nBackground color change completed successfully!")
        print(f"Modified PDF saved as: {output_path}")
    else:
        print("\nFailed to modify the PDF. Please check the input file and try again.")

if __name__ == "__main__":
    main()