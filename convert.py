import os
from PIL import Image
import fitz  # PyMuPDF
from PyPDF2 import PdfReader
from tqdm import tqdm

mult = 2
png_resolution = (2480 * mult, 3508 * mult)  # Adjust the resolution as needed
pdf_resolution = (2480 * mult, 3508 * mult)  # A4 size at 300 DPI

# Create a directory to store the PNG images
os.makedirs("png_images", exist_ok=True)

print("Export images very hd mmmmm nice nice")
# Convert each PDF to a PNG image
for i in tqdm(range(1,67)):
    pdf_path = f"PDF/{i}.pdf"
    png_path = f"png_images/{i}.png"
    
    # Open the PDF file and convert it to a PNG image
    pdf_document = fitz.open(pdf_path)
    page = pdf_document.load_page(0)  # Load the first page
    pix = page.get_pixmap(matrix=fitz.Matrix(mult, mult))  # Render the page to an image
    pix.save(png_path)

# Create a new PDF document
print("Creating new document")
pdf_images = []
for i in tqdm(range(1, 67)):
    png_path = f"png_images/{i}.png"
    
    # Open the PNG image and convert it to RGB mode
    image = Image.open(png_path).convert("RGB")
    
    # Scale the image to A4 size while maintaining the aspect ratio
    image.thumbnail(pdf_resolution)
    
    # Create a new blank image with A4 size and paste the scaled image at the center
    background = Image.new("RGB", pdf_resolution, (255, 255, 255))
    background.paste(image, ((pdf_resolution[0] - image.width) // 2, (pdf_resolution[1] - image.height) // 2))
    
    pdf_images.append(background)


import io
# Save the images as a PDF file
print("Saving proofing draft")
pdf_images[0].save("Inception24-DraftProof7.pdf", "PDF", resolution=100.0, save_all=True, append_images=pdf_images[1:])

# Calculate the total number of pages
total_pages = len(pdf_images)

# Create a function to generate a blank page
def create_blank_page(size=(2480 * mult, 3508 * mult)):
    return Image.new('RGB', size, color=(255, 255, 255))

# Insert a blank page at the second position
blank_page_1 = create_blank_page()
pdf_images.insert(1, blank_page_1)

# Insert a blank page at the second to last position
if total_pages > 1:  # Ensure there's more than one page to avoid index out of range error
    blank_page_2 = create_blank_page()
    pdf_images.insert(total_pages, blank_page_2)

# Now, save the images as a PDF file
with io.BytesIO() as output_pdf:
    print("Saving indd draft to bytes")
    pdf_images[0].save(output_pdf, "PDF", resolution=100.0, save_all=True, append_images=pdf_images[1:])
    
    # Write the BytesIO object to a file
    print("Dumping bytes to mem")
    with open("Inception24-Draft7.pdf", "wb") as f_out:
        f_out.write(output_pdf.getvalue())
